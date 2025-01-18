from src.lexer import Lexer
from src.ast import Program, Statement, Assignment, Identifier, Expression, Integer, String, Bool, Float, PlusOperation, \
    MinusOperation
from typing import Optional
from src.token import Token, TokenType

"""
program -> statement*
statement -> assignment | if_statement | while_statement | for_statement | function_def | return_statement | expression
assignment -> identifier "=" expression

expression -> logical_expr
logical_expr -> comparison_expr (("and" | "or") comparison_expr)*
comparison_expr -> arithmetic_expr ((">" | "<" | ">=" | "<=" | "==" | "!=") arithmetic_expr)*
arithmetic_expr -> term (("+" | "-") term)*
term -> factor (("*" | "/") factor)*
factor -> identifier | literal | "(" expression ")" | function_call | array_literal | map_literal | set_literal

literal -> NUMBER | STRING | BOOLEAN | NULL
array_literal -> "[" (expression ("," expression)*)? "]"
map_literal -> "{" (STRING ":" expression ("," STRING ":" expression)*)? "}"
set_literal -> "{" (expression ("," expression)*)? "}"

function_call -> identifier "(" (expression ("," expression)*)? ")"
function_def -> "def" identifier "(" (identifier ("," identifier)*)? ")" ":" block

if_statement -> "if" expression ":" block ("elif" expression ":" block)* ("else" ":" block)?
while_statement -> "while" expression ":" block
for_statement -> "for" assignment ";" expression ";" assignment ":" block

block -> INDENT statement+ DEDENT
return_statement -> "return" expression?
"""

class Parser:
    def __init__(self, sequence: list[Token]):
        self.sequence = sequence
        self.index = 0
        self.errors = []

    def parse(self) -> Program:
        statements = []
        while self._current_token is not None and self._current_token.type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                statements.append(statement)
            self._advance_token()

        return Program(statements)
    
    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None

        if self._current_token.type == TokenType.IDENTIFIER and self._next_token.type == TokenType.ASSIGN:
            return self._parse_assignment_statement()
        
    def _parse_assignment_statement(self) -> Optional[Assignment]:
        # Parse identifier of assigment
        if not self._expect_one_of([TokenType.IDENTIFIER], self._current_token):
            return None
        identifier = Identifier(self._current_token, self._current_token.literal)
        self._advance_token()

        # Get assigment token
        if not self._expect_one_of([TokenType.ASSIGN], self._current_token):
            return None
        assignment_token = self._current_token
        self._advance_token()

        # Parse expression to assign
        value = self._parse_expression()

        return Assignment(assignment_token, identifier, value)
    
    def _parse_expression(self) -> Expression:
        while self._current_token.type != TokenType.NEWLINE:
            expr = self._parse_comparison_expression()
            self._advance_token()
            return expr
        pass

    def _expect_one_of(self, token_types: list[TokenType], token: Token) -> bool:
        if self._current_token.type not in token_types:
            self.errors.append(f"Expected any of {token_types}, got {token.type} instead")
            return False

        return True

    @property
    def _current_token(self) -> Optional[Token]:
        if self.index < len(self.sequence):
            return self.sequence[self.index]
        return None

    @property
    def _next_token(self) -> Optional[Token]:
        if self.index + 1 < len(self.sequence):
            return self.sequence[self.index + 1]
        return None

    def _advance_token(self) -> None:
        self.index += 1

    def _parse_comparison_expression(self):
        return self._parse_arithmetic_expression()

    def _parse_arithmetic_expression(self):
        term = self._parse_term()

        if self._current_token.type == TokenType.PLUS:
            token = self._current_token
            self._advance_token()
            second_term = self._parse_term()
            return PlusOperation(token, term, second_term)

        if self._current_token.type == TokenType.MINUS:
            token = self._current_token
            self._advance_token()
            second_term = self._parse_term()
            return MinusOperation(token, term, second_term)

        return term

    def _parse_term(self):
        return self._parse_factor()

    def _parse_factor(self):
        if self._current_token.type == TokenType.IDENTIFIER:
            factor = Identifier(self._current_token, self._current_token.literal)
            self._advance_token()
            return factor

        if self._current_token.type == TokenType.NUMBER:
            number = Integer(self._current_token, int(self._current_token.literal))
            self._advance_token()
            return number

        if self._current_token.type == TokenType.STRING:
            string = String(self._current_token, self._current_token.literal)
            self._advance_token()
            return string

        if self._current_token.type == TokenType.BOOLEAN:
            val = True if self._current_token.literal == 'true' else False
            b = Bool(self._current_token, val)
            self._advance_token()
            return b

        if self._current_token.type == TokenType.FLOAT:
            val = Float(self._current_token, float(self._current_token.literal))
            self._advance_token()
            return val


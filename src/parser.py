from src.lexer import Lexer
from src.ast import Program, Statement, Assignment, Identifier, Expression
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

    def parse(self) -> Program:
        statements = []
        while self._current_token() is not None and self._current_token().type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                statements.append(statement)
            self._advance_token()

        return Program(statements)
    
    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token() is not None

        if self._current_token().type == TokenType.IDENTIFIER:
            return self._parse_identifier_statement()
    

    def _parse_identifier_statement(self) -> Optional[Statement]:
        assert self._next_token() is not None
        self._assert_expected_tokens([TokenType.ASSIGN], self._next_token())
        
        if self._next_token() == TokenType.ASSIGN:
            return self._parse_assignment_statement()
        
    def _parse_assignment_statement(self) -> Optional[Assignment]:
        identifier = Identifier(self._current_token(), self._current_token().literal)
        self._advance_token()
        self._assert_expected_tokens([TokenType.ASSIGN], self._current_token())
        assignment_token = self._current_token()
        self._advance_token()
        value = self._parse_expression()
        return Assignment(assignment_token, identifier, value)
    
    def _parse_expression(self) -> Expression:
        while self._current_token() is not None and self._current_token().type != TokenType.NEWLINE:
            self._advance_token()
        return None

    def _assert_expected_tokens(self, token_types: list[TokenType], token: Token) -> None:
        if token.type not in token_types:
            raise ValueError(f"Expected any of {token_types}, got {token.type} instead")

    def _add_error(self, message: str) -> None:
        self.errors.append(message)

    def _current_token(self) -> Optional[Token]:
        if self.index < len(self.sequence):
            return self.sequence[self.index]
        return None

    def _next_token(self) -> None:
        if self.index + 1 < len(self.sequence):
            return self.sequence[self.index + 1]
        return None
    
    def _advance_token(self) -> None:
        self.index += 1

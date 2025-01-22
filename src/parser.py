from src.lexer import Lexer
from src.ast import *
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
factor -> unary_expr | elemental_expr
unary_expr -> ("-") elemental_expr
elemental_expr -> identifier | literal | "(" expression ")" | function_call | array_literal | map_literal | set_literal

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

ComparisonOperators = {
    TokenType.LESS: LessOperation,
    TokenType.LESS_EQ: LessOrEqualOperation,
    TokenType.EQUAL: EqualOperation,
    TokenType.GREATER: GreaterOperation,
    TokenType.GREATER_EQ: GreaterOrEqualOperation,
    TokenType.NOT_EQUAL: NotEqualOperation,
}

PrefixOperators = {
    TokenType.MINUS: NegativeOperation,
    TokenType.NOT: NotOperation,
}

TermOperators = {
    TokenType.MUL: MultiplicationOperation,
    TokenType.DIV: DivisionOperation,
}

ArithmeticOperators = {
    TokenType.PLUS: PlusOperation,
    TokenType.MINUS: MinusOperation,
}

LogicalOperators = {
    TokenType.AND: AndOperation,
    TokenType.OR: OrOperation,
}

class Parser:
    def __init__(self, sequence: list[Token]):
        self.sequence = sequence
        self.index = 0
        self.errors = []

    def parse(self) -> Program:
        statements = []
        while self._current_token is not None and self._current_token.type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is None:
                self._advance_token()
            else:
                statements.append(statement)


        return Program(statements)
    
    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        if self._current_token.type in [TokenType.NEWLINE, TokenType.EOF]:
            return None

        if self._current_token.type == TokenType.IDENTIFIER and self._next_token.type == TokenType.ASSIGN:
            return self._parse_assignment_statement()

        self._expect_one_of([TokenType.IDENTIFIER])
        
    def _parse_assignment_statement(self) -> Optional[Assignment]:
        # Parse identifier
        assert self._current_token.type == TokenType.IDENTIFIER
        identifier = Identifier(self._current_token, self._current_token.literal)
        self._advance_token()

        assert self._current_token.type == TokenType.ASSIGN
        assignment_token = self._current_token
        self._advance_token()

        # Parse expression to assign
        value = self._parse_expression()
        if value is None:
            return None

        return Assignment(assignment_token, identifier, value)

    def _parse_expression(self) -> Optional[Expression]:
        expr = self._parse_logical_expression()
        return expr
    
    def _parse_logical_expression(self) -> Optional[Expression]:
        first_expr = self._parse_comparison_expression()
        if first_expr is None:
            return None

        while first_expr is not None and self._current_token.type in LogicalOperators.keys():
            token = self._current_token
            self._advance_token()
            second_expr = self._parse_comparison_expression()
            if second_expr is None:
                return None
            first_expr = LogicalOperators[token.type](token, first_expr, second_expr)

        return first_expr

    def _expect_one_of(self, token_types: list[TokenType]) -> bool:
        if self._current_token.type not in token_types:
            ls = ', '.join([t.name for t in token_types])
            self.errors.append(f"Expected {ls}, got {self._current_token.type.name} instead in position {self._current_token.pos}")
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

    def _parse_comparison_expression(self) -> Optional[Expression]:
        first = self._parse_arithmetic_expression()
        if first is None:
            return None

        while first is not None and self._current_token.type in ComparisonOperators.keys():
            token = self._current_token
            comparison_operator = ComparisonOperators[token.type]
            self._advance_token()
            second_expr = self._parse_arithmetic_expression()
            if second_expr is None:
                return None
            first = comparison_operator(token, first, second_expr)

        return first

    def _parse_arithmetic_expression(self) -> Optional[Expression]:
        term = self._parse_term()
        if term is None:
            return None

        while term is not None and self._current_token.type in ArithmeticOperators.keys():
            token = self._current_token
            self._advance_token()
            second_term = self._parse_term()
            if second_term is None:
                return None
            term = ArithmeticOperators[token.type](token, term, second_term)

        return term

    def _parse_term(self) -> Optional[Expression]:
        factor = self._parse_unary_expression()
        if factor is None:
            return None

        while factor is not None and self._current_token.type in TermOperators.keys():
            token = self._current_token
            self._advance_token()
            second_factor = self._parse_unary_expression()
            if second_factor is None:
                return None
            factor = TermOperators[token.type](token, factor, second_factor)

        return factor

    def _parse_unary_expression(self) -> Optional[Expression]:
        if self._current_token.type not in PrefixOperators.keys():
            return self._parse_elemental_expression()

        tokens = [self._current_token]
        self._advance_token()

        while self._current_token.type in PrefixOperators.keys():
            tokens.append(self._current_token)
            self._advance_token()

        expr = self._parse_expression()
        if expr is None:
            return None

        while tokens:
            token = tokens.pop()
            expr = PrefixOperators[token.type](token, expr)

        return expr

    def _parse_elemental_expression(self) -> Optional[Expression]:
        if self._current_token.type == TokenType.LPAREN:
            return self._parse_paren_grou_expression()

        if self._current_token.type == TokenType.IDENTIFIER and self._next_token.type == TokenType.LPAREN:
            return self._parse_function_call()

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
        
        self._expect_one_of([TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.FLOAT])
        return None

    def _parse_function_call(self) -> Optional[Expression]:
        token = self._current_token
        identifier = Identifier(self._current_token, self._current_token.literal)
        self._advance_token()
        assert self._current_token.type == TokenType.LPAREN
        self._advance_token()
        arguments = []
        while self._current_token.type != TokenType.RPAREN:
            expr = self._parse_expression()
            if expr is None:
                return None
            arguments.append(expr)

            if self._current_token.type in [TokenType.COMMA]:
                self._advance_token()
                continue

        self._advance_token()
        return FunctionCall(token, identifier, arguments)

    def _parse_paren_grou_expression(self) -> Optional[Expression]:
        assert self._current_token.type == TokenType.LPAREN
        self._advance_token()

        expr = self._parse_expression()
        if expr is None:
            return None

        if self._current_token.type != TokenType.RPAREN:
            self._expect_one_of([TokenType.RPAREN])
            return None

        self._advance_token()
        return expr
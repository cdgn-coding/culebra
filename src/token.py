from enum import Enum, auto, unique
from typing import NamedTuple

@unique
class TokenType(Enum):
    # Single-character tokens
    ASSIGN  = auto()
    COMMA   = auto()
    LPAREN  = auto()
    RPAREN  = auto()
    LBRACE  = auto()
    RBRACE  = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    # Indentation
    INDENT   = auto()
    DEDENT   = auto()

    # Literals
    IDENTIFIER = auto()
    NUMBER     = auto()
    STRING     = auto()
    FLOAT      = auto()

    # Data Structures
    ARRAY      = auto()
    MAP        = auto()
    SET        = auto()

    # Keywords
    FUNCTION = auto()
    IF       = auto()
    ELSE     = auto()
    RETURN   = auto()
    ELSEIF   = auto()
    WHILE    = auto()
    FOR      = auto()
    BREAK    = auto()
    CONTINUE = auto()
    PRINT    = auto()
    PRINTLN  = auto()

    # Operators
    PLUS     = auto()
    MINUS    = auto()
    MUL      = auto()
    DIV      = auto()

    # Comparison operators
    EQUAL    = auto()
    NOT_EQUAL = auto()
    NEG      = auto()
    LESS     = auto()
    GREATER  = auto()
    LESS_EQ  = auto()
    GREATER_EQ = auto()

    # Logical operators
    AND      = auto()
    OR       = auto()

    # Expressions
    FUNCTION_CALL = auto()

    # End of file
    EOF      = auto()

    # Errors
    ILLEGAL_CHARACTER = auto()

    WHITESPACE = auto()

class Token:
    type: TokenType
    literal: str

    def __init__(self, type: TokenType, literal: str):
        self.type = type
        self.literal = literal

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.literal == other.literal

    def __str__(self):
        return f"Token({self.type}, {self.literal})"

    def __repr__(self):
        return f"Token({self.type}, {self.literal})"

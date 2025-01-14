from unittest import TestCase
from src.lexer import Lexer
from src.token import Token, TokenType
class TestLexer(TestCase):
    def test_illegal_character(self):
        code = "$@?"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected: List[Token] = [
            Token(TokenType.ILLEGAL_CHARACTER, "$"),
            Token(TokenType.ILLEGAL_CHARACTER, "@"),
            Token(TokenType.ILLEGAL_CHARACTER, "?"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_number(self):
        code = "123"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(tokens)
        expected = [
            Token(TokenType.NUMBER, "123"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

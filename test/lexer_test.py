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
        
        expected = [
            Token(TokenType.NUMBER, "123"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_empty_input(self):
        lexer = Lexer("")
        tokens = lexer.tokenize()
        expected = [
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_single_char_tokens(self):
        input_code = "(){}[],"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.LBRACKET, "["),
            Token(TokenType.RBRACKET, "]"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_assignment(self):
        input_code = "x = 10"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_arithmetic_operators(self):
        input_code = "+-*/"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.MUL, "*"),
            Token(TokenType.DIV, "/"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_comparison_operators(self):
        input_code = "== != < > <= >="
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.EQUAL, "=="),
            Token(TokenType.NOT_EQUAL, "!="),
            Token(TokenType.LESS, "<"),
            Token(TokenType.GREATER, ">"),
            Token(TokenType.LESS_EQ, "<="),
            Token(TokenType.GREATER_EQ, ">="),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_literals(self):
        input_code = '123 someIdentifier "string literal" 3.14'
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.NUMBER, "123"),
            Token(TokenType.IDENTIFIER, "someIdentifier"),
            Token(TokenType.STRING, '"string literal"'),
            Token(TokenType.FLOAT, "3.14"),
            Token(TokenType.EOF, "")
        ]
        
        
        self.assertEqual(tokens, expected)

    def test_keyword_if_else(self):
        input_code = "if else elif"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IF, "if"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.ELSEIF, "elif"),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_conditional_statement(self):
        source = """
if x > 10:
\tprint("x es mayor que 10")
elif x == 10:
\tprint("x es igual a 10")
else:
\tprint("x es menor que 10")"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            Token(TokenType.IF, "if"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.GREATER, ">"),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, '"x es mayor que 10"'),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.ELSEIF, "elif"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.EQUAL, "=="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, '"x es igual a 10"'),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, '"x es menor que 10"'),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.EOF, ""),
        ]

        
        

        self.assertEqual(expected, tokens)

    def test_indentation(self):
        source = """
def test():
\tx = 1
\ty = 2
\tz = 3
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            Token(TokenType.FUNCTION_DEFINITION, "def"),
            Token(TokenType.IDENTIFIER, "test"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.IDENTIFIER, "z"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.EOF, ""),
        ]        
        
        self.assertEqual(expected, tokens)

    def test_space_indentation(self):
        source = """
def test():
    x = 1
        y = 2
    z = 3
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            Token(TokenType.FUNCTION_DEFINITION, "def"),
            Token(TokenType.IDENTIFIER, "test"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.INDENT, 2),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "z"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.EOF, ""),
        ]
        
        
        
        self.assertEqual(expected, tokens)

    def test_line_comment(self):
        source = "x = 10  # This is a comment\ny = 20"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "20"),
            Token(TokenType.EOF, "")
        ]
        
        self.assertEqual(tokens, expected)
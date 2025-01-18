from unittest import TestCase
from src.lexer import Lexer
from src.token import Token, TokenType

class TestLexer(TestCase):
    def test_illegal_character(self):
        code = "$@?"
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        expected: List[Token] = [
            Token(TokenType.ILLEGAL_CHARACTER, "$"),
            Token(TokenType.ILLEGAL_CHARACTER, "@"),
            Token(TokenType.ILLEGAL_CHARACTER, "?"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_number(self):
        code = "123"
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        
        expected = [
            Token(TokenType.NUMBER, "123"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_empty_input(self):
        lexer = Lexer()
        tokens = lexer.tokenize("")
        expected = [
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_single_char_tokens(self):
        input_code = "(){}[],"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

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
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_arithmetic_operators(self):
        input_code = "+-*/"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

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
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

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
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

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
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.IF, "if"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.ELIF, "elif"),
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
        
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IF, "if"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.GREATER, ">"),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, '"x es mayor que 10"'),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.ELIF, "elif"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.EQUAL, "=="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, '"x es igual a 10"'),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
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
        
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.FUNCTION_DEFINITION, "def"),
            Token(TokenType.IDENTIFIER, "test"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "z"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.EOF, ""),
        ]

    def test_space_indentation(self):
        source = """
def test():
    x = 1
        y = 2
    z = 3
"""
        
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.FUNCTION_DEFINITION, "def"),
            Token(TokenType.IDENTIFIER, "test"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 2),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 1),
            Token(TokenType.IDENTIFIER, "z"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.INDENT, 0),
            Token(TokenType.EOF, ""),
        ]

    def test_line_comment(self):
        source = "x = 10  # This is a comment\ny = 20"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "20"),
            Token(TokenType.EOF, "")
        ]

        self.assertEqual(tokens, expected)

    def test_multiline_string(self):
        source = '"""This is a\nmultiline string"""\nx = 1'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.STRING, '"""This is a\nmultiline string"""'),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.EOF, "")
        ]

        print(tokens)
        print(expected)
        self.assertEqual(tokens, expected)

    def test_boolean_literals(self):
        source = "true false"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.BOOLEAN, "false"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_for_loop_syntax(self):
        source = "for i = 0; i < 10; i = i + 1:"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.FOR, "for"),
            Token(TokenType.IDENTIFIER, "i"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.IDENTIFIER, "i"),
            Token(TokenType.LESS, "<"),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.IDENTIFIER, "i"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENTIFIER, "i"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_mixed_data_types(self):
        source = '[1, "text", 3.14, true, {1, 2}]'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.LBRACKET, "["),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.STRING, '"text"'),
            Token(TokenType.COMMA, ","),
            Token(TokenType.FLOAT, "3.14"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.RBRACKET, "]"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_eof(self):
        source = ""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_identifier_patterns(self):
        source = "variable123 _private num1 1invalid my_var_2"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "variable123"),
            Token(TokenType.IDENTIFIER, "_private"),
            Token(TokenType.IDENTIFIER, "num1"),
            Token(TokenType.INVALID_IDENTIFIER, "1invalid"),
            Token(TokenType.IDENTIFIER, "my_var_2"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_longest_possible_token_for(self):
        source = "for_identifier_not_keyworkd"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "for_identifier_not_keyworkd"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

    def test_longest_possible_token_if(self):
        source = "if_identifier_not_keyworkd"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "if_identifier_not_keyworkd"),
            Token(TokenType.EOF, "")
        ]
        self.assertEqual(tokens, expected)

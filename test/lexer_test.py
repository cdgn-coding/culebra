import unittest.mock
from typing import List
from unittest import TestCase
from culebra.lexer import Lexer
from culebra.token import Token, TokenType

class TestLexer(TestCase):
    def test_illegal_character(self):
        code = "$@?"
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        expected: List[Token] = [
            Token(TokenType.ILLEGAL_CHARACTER, "$", unittest.mock.ANY),
            Token(TokenType.ILLEGAL_CHARACTER, "@", unittest.mock.ANY),
            Token(TokenType.ILLEGAL_CHARACTER, "?", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_number(self):
        code = "123"
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        
        expected = [
            Token(TokenType.NUMBER, "123", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_empty_input(self):
        lexer = Lexer()
        tokens = lexer.tokenize("")
        expected = [
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_single_char_tokens(self):
        input_code = "(){}[],"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.LBRACE, "{", unittest.mock.ANY),
            Token(TokenType.RBRACE, "}", unittest.mock.ANY),
            Token(TokenType.LBRACKET, "[", unittest.mock.ANY),
            Token(TokenType.RBRACKET, "]", unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)

    def test_assignment(self):
        input_code = "x = 10"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "10", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)

    def test_and_or_tokens(self):
        input_code = "true and or false"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.BOOLEAN, "true", unittest.mock.ANY),
            Token(TokenType.AND, "and", unittest.mock.ANY),
            Token(TokenType.OR, "or", unittest.mock.ANY),
            Token(TokenType.BOOLEAN, "false", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)


    def test_arithmetic_operators(self):
        input_code = "+-*/"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.PLUS, "+", unittest.mock.ANY),
            Token(TokenType.MINUS, "-", unittest.mock.ANY),
            Token(TokenType.MUL, "*", unittest.mock.ANY),
            Token(TokenType.DIV, "/", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_comparison_operators(self):
        input_code = "== != < > <= >="
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.EQUAL, "==", unittest.mock.ANY),
            Token(TokenType.NOT_EQUAL, "!=", unittest.mock.ANY),
            Token(TokenType.LESS, "<", unittest.mock.ANY),
            Token(TokenType.GREATER, ">", unittest.mock.ANY),
            Token(TokenType.LESS_EQ, "<=", unittest.mock.ANY),
            Token(TokenType.GREATER_EQ, ">=", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)

    def test_literals(self):
        input_code = '123 someIdentifier "string literal" 3.14'
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.NUMBER, "123", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "someIdentifier", unittest.mock.ANY),
            Token(TokenType.STRING, '"string literal"', unittest.mock.ANY),
            Token(TokenType.FLOAT, "3.14", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        
        
        self.assertEqual(tokens, expected)

    def test_keyword_if_else(self):
        input_code = "if else elif"
        lexer = Lexer()
        tokens = lexer.tokenize(input_code)

        expected = [
            Token(TokenType.IF, "if", unittest.mock.ANY),
            Token(TokenType.ELSE, "else", unittest.mock.ANY),
            Token(TokenType.ELIF, "elif", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
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
            Token(TokenType.IF, "if", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.GREATER, ">", unittest.mock.ANY),
            Token(TokenType.NUMBER, "10", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "print", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.STRING, '"x es mayor que 10"', unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.ELIF, "elif", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.EQUAL, "==", unittest.mock.ANY),
            Token(TokenType.NUMBER, "10", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "print", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.STRING, '"x es igual a 10"', unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.ELSE, "else", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "print", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.STRING, '"x es menor que 10"', unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY),
        ]

        self.assertEqual(tokens, expected)

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
            Token(TokenType.FUNCTION_DEFINITION, "def", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "test", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "y", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "z", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "3", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY),
        ]
        self.assertEqual(tokens, expected)

    def test_nested_indentation(self):
        source = """
def test():
\tif x > 0:
\t\tprint("positive")
\telse:
\t\tprint("negative")
"""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.FUNCTION_DEFINITION, "def", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "test", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IF, "if", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.GREATER, ">", unittest.mock.ANY),
            Token(TokenType.NUMBER, "0", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "print", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.STRING, '"positive"', unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.ELSE, "else", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "print", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.STRING, '"negative"', unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY),
        ]
        self.assertEqual(tokens, expected)

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
            Token(TokenType.FUNCTION_DEFINITION, "def", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "test", unittest.mock.ANY),
            Token(TokenType.LPAREN, "(", unittest.mock.ANY),
            Token(TokenType.RPAREN, ")", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "y", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "z", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "3", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY),
        ]
        self.assertEqual(tokens, expected)

    def test_line_comment(self):
        source = "x = 10  # This is a comment\ny = 20"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "10", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "y", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "20", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)

    def test_multiline_string(self):
        source = '"""This is a\nmultiline string"""\nx = 1'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.STRING, '"""This is a\nmultiline string"""', unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]

        self.assertEqual(tokens, expected)

    def test_boolean_literals(self):
        source = "true false"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.BOOLEAN, "true", unittest.mock.ANY),
            Token(TokenType.BOOLEAN, "false", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_for_loop_syntax(self):
        source = "for i = 0; i < 10; i = i + 1:"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.FOR, "for", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "i", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "0", unittest.mock.ANY),
            Token(TokenType.SEMICOLON, ";", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "i", unittest.mock.ANY),
            Token(TokenType.LESS, "<", unittest.mock.ANY),
            Token(TokenType.NUMBER, "10", unittest.mock.ANY),
            Token(TokenType.SEMICOLON, ";", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "i", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "i", unittest.mock.ANY),
            Token(TokenType.PLUS, "+", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.COLON, ":", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_mixed_data_types(self):
        source = '[1, "text", 3.14, true, {1, 2}]'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.LBRACKET, "[", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.STRING, '"text"', unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.FLOAT, "3.14", unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.BOOLEAN, "true", unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.LBRACE, "{", unittest.mock.ANY),
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.COMMA, ",", unittest.mock.ANY),
            Token(TokenType.NUMBER, "2", unittest.mock.ANY),
            Token(TokenType.RBRACE, "}", unittest.mock.ANY),
            Token(TokenType.RBRACKET, "]", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_eof(self):
        source = ""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_identifier_patterns(self):
        source = "variable123 _private num1 1invalid my_var_2"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "variable123", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "_private", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "num1", unittest.mock.ANY),
            Token(TokenType.INVALID_IDENTIFIER, "1invalid", unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "my_var_2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_longest_possible_token_for(self):
        source = "for_identifier_not_keyworkd"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "for_identifier_not_keyworkd", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_longest_possible_token_if(self):
        source = "if_identifier_not_keyworkd"
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "if_identifier_not_keyworkd", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_simple_indentation(self):
        source = """
x
    y
z
"""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "y", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "z", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_multiple_dedents(self):
        source = """
x1
    x2
        x3
    x4
x5
"""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.IDENTIFIER, "x1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x3", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x4", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x5", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_end_of_file_dedents(self):
        source = """
x1
    x2
        x3
"""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.IDENTIFIER, "x1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x3", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_multiple_explicit_dedents(self):
        source = """
x1
    x2
        x3
x4
"""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        expected = [
            Token(TokenType.IDENTIFIER, "x1", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 1, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x2", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.INDENT, 2, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x3", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.DEDENT, None, unittest.mock.ANY),
            Token(TokenType.IDENTIFIER, "x4", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_comparison(self):
        code = "1 > 2 >= 3 <= 4 < 5 == 6 != 7"
        lexer = Lexer()
        tokens = lexer.tokenize(code)

        expected = [
            Token(TokenType.NUMBER, "1", unittest.mock.ANY),
            Token(TokenType.GREATER, ">", unittest.mock.ANY),
            Token(TokenType.NUMBER, "2", unittest.mock.ANY),
            Token(TokenType.GREATER_EQ, ">=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "3", unittest.mock.ANY),
            Token(TokenType.LESS_EQ, "<=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "4", unittest.mock.ANY),
            Token(TokenType.LESS, "<", unittest.mock.ANY),
            Token(TokenType.NUMBER, "5", unittest.mock.ANY),
            Token(TokenType.EQUAL, "==", unittest.mock.ANY),
            Token(TokenType.NUMBER, "6", unittest.mock.ANY),
            Token(TokenType.NOT_EQUAL, "!=", unittest.mock.ANY),
            Token(TokenType.NUMBER, "7", unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_string_with_escaped_quotes(self):
        source = 'x = "Hello \\"World\\""'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY),
            Token(TokenType.ASSIGN, "=", unittest.mock.ANY),
            Token(TokenType.STRING, '"Hello \\"World\\""', unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_string_with_escape_sequences(self):
        source = '"\\n\\t\\\\"'  # String containing \n, \t, and \
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.STRING, '"\\n\\t\\\\"', unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_triple_quoted_string_with_escapes(self):
        source = '"""This is a \\"triple\\" quoted string\\n"""'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.STRING, '"""This is a \\"triple\\" quoted string\\n"""', unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_mixed_quotes_in_strings(self):
        source = '"Contains \'single\' quotes"'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        expected = [
            Token(TokenType.STRING, '"Contains \'single\' quotes"', unittest.mock.ANY),
            Token(TokenType.NEWLINE, "\n", unittest.mock.ANY),
            Token(TokenType.EOF, "", unittest.mock.ANY)
        ]
        self.assertEqual(tokens, expected)

    def test_unterminated_string(self):
        source = '"This string never ends...'
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        self.assertIn(Token(TokenType.ILLEGAL_CHARACTER, '"', unittest.mock.ANY), tokens)

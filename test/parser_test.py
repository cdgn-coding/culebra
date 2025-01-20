from typing import cast
from unittest import TestCase, skip
from src.parser import Parser
from src.lexer import Lexer
from src.ast import Program, Assignment, Identifier
from src.token import TokenType, Token


class TestParser(TestCase):
    def test_parse_empty_program(self):
        source = ""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        self.assertTrue(isinstance(program, Program))

    def test_parse_assignment(self):
        source = "x = 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        self.assertTrue(isinstance(program, Program))
        self.assertEqual(len(program.statements), 1)

        expected_identifier = Identifier(Token(TokenType.IDENTIFIER, "x"), "x")
        actual_identifier = cast(Assignment, program.statements[0]).identifier
        self.assertEqual(repr(expected_identifier), repr(actual_identifier))

    def test_parse_literal_expression(self):
        source = "x = 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(len(program.statements), 1)

        actual_assignment = cast(Assignment, program.statements[0])
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.NUMBER 1', repr(actual_assignment))

    def test_parse_literal_expressions_by_data_type(self):
        sources = [
            "x = 1",
            "x = 1.0",
            'x = "1.0"',
            "x = true",
            "x = false",
        ]

        expected = [
            "TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.NUMBER 1",
            "TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.FLOAT 1.0",
            'TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.STRING "1.0"',
            "TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.BOOLEAN True",
            "TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.BOOLEAN False",
        ]

        for source, exp in zip(sources, expected):
            sequence = Lexer().tokenize(source)
            parser = Parser(sequence)
            program = parser.parse()
            self.assertTrue(isinstance(program, Program))
            self.assertEqual(exp, repr(program))

    def test_parse_plus_expression(self):
        source = "x = 1 + 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.PLUS TokenType.NUMBER 1 + TokenType.NUMBER 1', repr(program))

    def test_parse_minus_expression(self):
        source = "x = 1 - 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.MINUS TokenType.NUMBER 1 - TokenType.NUMBER 1', repr(program))

    def test_parse_multiplication_expressions(self):
        source = "x = 1 * 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.MUL TokenType.NUMBER 1 * TokenType.NUMBER 2', repr(program))

    def test_parse_division_expressions(self):
        source = "x = 1 / 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.DIV TokenType.NUMBER 1 / TokenType.NUMBER 2', repr(program))

    def test_parse_recursive_arithmetic(self):
        source = "x = 2 + 3 * 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.PLUS TokenType.NUMBER 2 + TokenType.MUL TokenType.NUMBER 3 * TokenType.NUMBER 2', repr(program))

    def test_parse_multiple_recursive_arithmetic(self):
        source = "x = 2 + 3 * 2\ny = 1.0 + 1.0 / 2.0"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual("\n".join([
            "TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.PLUS TokenType.NUMBER 2 + TokenType.MUL TokenType.NUMBER 3 * TokenType.NUMBER 2",
            "TokenType.ASSIGN TokenType.IDENTIFIER y = TokenType.PLUS TokenType.FLOAT 1.0 + TokenType.DIV TokenType.FLOAT 1.0 / TokenType.FLOAT 2.0"]), repr(program)
        )

    def test_parse_all_arithmetic_operations(self):
        source = "x = 1 + 2 * 3 + 4 / 5"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('TokenType.ASSIGN TokenType.IDENTIFIER x = TokenType.PLUS TokenType.PLUS '
 'TokenType.NUMBER 1 + TokenType.MUL TokenType.NUMBER 2 * TokenType.NUMBER 3 + '
 'TokenType.DIV TokenType.NUMBER 4 / TokenType.NUMBER 5', repr(program))
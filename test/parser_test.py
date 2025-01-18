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

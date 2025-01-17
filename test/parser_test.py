from unittest import TestCase
from src.parser import Parser
from src.lexer import Lexer
from src.ast import Program

class TestParser(TestCase):
    def test_parse_empty_program(self):
        source = ""
        lexer = Lexer()
        parser = Parser(lexer)
        program = parser.parse(source)

        self.assertTrue(isinstance(program, Program))

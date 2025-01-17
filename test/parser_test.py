from unittest import TestCase, skip
from src.parser import Parser
from src.lexer import Lexer
from src.ast import Program, AssignmentStatement, Identifier

class TestParser(TestCase):
    def test_parse_empty_program(self):
        source = ""
        lexer = Lexer()
        parser = Parser(lexer)
        program = parser.parse(source)

        self.assertTrue(isinstance(program, Program))

    @skip("Not implemented")
    def test_parse_assignment(self):
        source = "x = 1;"
        lexer = Lexer()
        parser = Parser(lexer)
        program = parser.parse(source)

        self.assertTrue(isinstance(program, Program))
        self.assertEqual(len(program.statements), 1)
        self.assertTrue(isinstance(program.statements[0], AssignmentStatement))
        self.assertEqual(program.statements[0].identifier.value, "x")
        self.assertEqual(program.statements[0].value.value, "1")
        

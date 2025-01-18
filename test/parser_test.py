from unittest import TestCase, skip
from src.parser import Parser
from src.lexer import Lexer
from src.ast import Program, Assignment, Identifier

class TestParser(TestCase):
    def test_parse_empty_program(self):
        source = ""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        self.assertTrue(isinstance(program, Program))

    def test_parse_incomplete_assignment(self):
        source = "x"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        
        with self.assertRaises(ValueError) as context:
            program = parser.parse()
            
        self.assertEqual(str(context.exception), "Expected any of [<TokenType.ASSIGN: 1>], got TokenType.EOF instead")

    def test_parse_assignment(self):
        source = "x = 1;"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        self.assertTrue(isinstance(program, Program))
        self.assertEqual(len(program.statements), 1)
        self.assertTrue(isinstance(program.statements[0], Assignment))
        self.assertEqual(program.statements[0].identifier.value, "x")
        self.assertEqual(program.statements[0].value.value, "1")
        

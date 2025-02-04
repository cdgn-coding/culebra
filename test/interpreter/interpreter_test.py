from unittest import TestCase

from culebra.interpreter.interpreter import Interpreter
from culebra.lexer import Lexer
from culebra.parser import Parser


class TestParser(TestCase):
    def test_basic_assignment(self):
        source = """a = 1"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(1, interpreter.root_environment.get('a'))
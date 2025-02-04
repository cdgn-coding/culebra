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

    def test_reuse_variable(self):
        source = """
a = 1
b = a
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(1, interpreter.root_environment.get('b'))

    def test_basic_arithmetic(self):
        source = """
a = 1 + 2
b = 1 * 2
c = 1 - 2
d = 1 / 2
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(3, interpreter.root_environment.get('a'))
        self.assertEqual(2, interpreter.root_environment.get('b'))
        self.assertEqual(-1, interpreter.root_environment.get('c'))
        self.assertEqual(1/2, interpreter.root_environment.get('d'))

    def test_composite_arithmetic(self):
        source = """
a = 1 + 2 * 2 + 5 / 5
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(1 + 2 * 2 + 5 / 5, interpreter.root_environment.get('a'))

    def test_composite_arithmetic_with_negative_numbers(self):
        source = """
a = 1 + 2 * 2 + 5 / 5 + -1
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(1 + 2 * 2 + 5 / 5 + -1, interpreter.root_environment.get('a'))

    def test_basic_comparison(self):
        source = """
a = 1 >= 1
b = 1 > 1
c = 1 < 1
d = 1 <= 1
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(True, interpreter.root_environment.get('a'))
        self.assertEqual(False, interpreter.root_environment.get('b'))
        self.assertEqual(False, interpreter.root_environment.get('c'))
        self.assertEqual(True, interpreter.root_environment.get('d'))

    def test_literals(self):
        source = """
a = true
b = false
c = 1
d = 1.0
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(True, interpreter.root_environment.get('a'))
        self.assertEqual(False, interpreter.root_environment.get('b'))
        self.assertEqual(1, interpreter.root_environment.get('c'))
        self.assertEqual(1.0, interpreter.root_environment.get('d'))

    def test_logical_operations(self):
        source = """
a = true or false
b = true or true
c = false or false
d = true and false
e = true and true
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(True, interpreter.root_environment.get('a'))
        self.assertEqual(True, interpreter.root_environment.get('b'))
        self.assertEqual(False, interpreter.root_environment.get('c'))
        self.assertEqual(False, interpreter.root_environment.get('d'))
        self.assertEqual(True, interpreter.root_environment.get('e'))

    def test_basic_if(self):
        source = """
a = 1
if true:
    a = 2
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(2, interpreter.root_environment.get('a'))

    def test_basic_else(self):
        source = """
a = 1
if false:
    a = 2
else:
    a = 3
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(3, interpreter.root_environment.get('a'))

    def test_basic_elif(self):
        source = """
a = 1
if false:
    a = 2
elif true:
    a = 3
else:
    a = 4
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(3, interpreter.root_environment.get('a'))

    def test_if_all_false(self):
        source = """
a = 1
if false:
    a = 2
elif false:
    a = 3
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(1, interpreter.root_environment.get('a'))

    def test_while_loop(self):
        source = """
a = 0
while a < 10:
    a = a + 1
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(10, interpreter.root_environment.get('a'))

    def test_for(self):
        source = """
a = 1
for i = 0; i < 10; i = i + 1:
    a = a * 2
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(2 ** 10, interpreter.root_environment.get('a'))

    def test_function_definition_and_call_no_arguments_scope_access(self):
        source = """
a = 1
def fn():
    a = 10
fn()
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(10, interpreter.root_environment.get('a'))
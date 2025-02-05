from unittest import TestCase

from culebra.interpreter.interpreter import Interpreter
from culebra.lexer import Lexer
from culebra.parser import Parser


class TestTuringCompleteness(TestCase):
    def test_fibonacci(self):
        # This test computes the 7th Fibonacci number using recursion.
        # Expected: fib(7) should be 13 if fib(0)=0 and fib(1)=1.
        source = """
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
result = fib(7)
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(13, interpreter.root_environment.get('result'))

    def test_nested_loops(self):
        # This test uses nested for-loops to count the number of iterations.
        # Expected: A 5 by 5 nested loop will run 25 iterations.
        source = """
a = 0
for i = 0; i < 5; i = i + 1:
    for j = 0; j < 5; j = j + 1:
        a = a + 1
result = a
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(25, interpreter.root_environment.get('result'))

    def test_while_factorial(self):
        # This test computes factorial using a while loop.
        # Expected: 5! should be 120.
        source = """
a = 1
n = 5
while n > 0:
    a = a * n
    n = n - 1
result = a
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(120, interpreter.root_environment.get('result'))

    def test_exponentiation(self):
        # This test computes exponentiation recursively.
        # Expected: 2^8 should be 256.
        source = """
def power(a, b):
    if b == 0:
        return 1
    return a * power(a, b - 1)
result = power(2, 8)
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter(program)
        interpreter.evaluate()

        self.assertEqual(256, interpreter.root_environment.get('result'))

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

        interpreter = Interpreter()
        interpreter.evaluate(program)

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

        interpreter = Interpreter()
        interpreter.evaluate(program)

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

        interpreter = Interpreter()
        interpreter.evaluate(program)

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

        interpreter = Interpreter()
        interpreter.evaluate(program)

        self.assertEqual(256, interpreter.root_environment.get('result'))

    def test_ackermann_multiple_cases(self):
        # This test verifies the Ackermann function for multiple input cases.
        # It calculates:
        # a0 = ack(0, 3) = 3 + 1 = 4
        # a1 = ack(1, 3) = ack(0, ack(1,2)) = ack(0,4) = 5
        # a2 = ack(2, 1) = ack(1, ack(2, 0)) = ack(1,3) = 5
        # a3 = ack(2, 2) = 7
        # Then, the composite result is computed as:
        # result = a0*1000 + a1*100 + a2*10 + a3
        # Expected result = 4*1000 + 5*100 + 5*10 + 7 = 4557
        source = """
def ack(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))
a0 = ack(0, 3)
a1 = ack(1, 3)
a2 = ack(2, 1)
a3 = ack(2, 2)
result = a0 * 1000 + a1 * 100 + a2 * 10 + a3
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.evaluate(program)

        self.assertEqual(4557, interpreter.root_environment.get('result'))

    def test_higher_order_function(self):
        # This test verifies that functions are first-class and can be passed as arguments.
        # The apply_twice function applies a given function twice to an argument.
        # For example, apply_twice(increment, 3) should yield 5.
        source = """
def apply_twice(fn, x):
    return fn(fn(x))
def increment(n):
    return n + 1
result = apply_twice(increment, 3)
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.evaluate(program)

        self.assertEqual(5, interpreter.root_environment.get('result'))

    def test_brainfuck_interpreter(self):
        source = """
def find_matching_bracket(current_pos, direction, code):
    count = 0
    if direction > 0:
        char_open = "["
        char_close = "]"
    else:
        char_open = "]"
        char_close = "["
    pos = current_pos + direction
    while pos >= 0 and pos < len(code):
        if code[pos] == char_open:
            count = count + 1
        elif code[pos] == char_close:
            count = count - 1
            if count < 0:
                return pos
        pos = pos + direction
    return -1

def brainfuck(code):
    tape = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pointer = 0
    output = ""
    code_pos = 0
    while code_pos < len(code):
        command = code[code_pos]
        if command == ">":
            pointer = pointer + 1
            if pointer >= len(tape):
                pointer = 0
        elif command == "<":
            pointer = pointer - 1
            if pointer < 0:
                pointer = len(tape) - 1
        elif command == "+":
            tape[pointer] = tape[pointer] + 1
            if tape[pointer] > 255:
                tape[pointer] = 0
        elif command == "-":
            tape[pointer] = tape[pointer] - 1
            if tape[pointer] < 0:
                tape[pointer] = 255
        elif command == ".":
            # Convert number to character and append to output
            output = output + chr(tape[pointer])
        elif command == "[":
            if tape[pointer] == 0:
                code_pos = find_matching_bracket(code_pos, 1, code)
                if code_pos < 0:
                    return "Error: Unmatched ["
        elif command == "]":
            if tape[pointer] != 0:
                code_pos = find_matching_bracket(code_pos, -1, code)
                if code_pos < 0:
                    return "Error: Unmatched ]"
        code_pos = code_pos + 1
    return output

# Test the interpreter with "Hello, World!"
program = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."

result = brainfuck(program)
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()

        self.assertEqual(False, parser.has_error, parser.last_error)

        interpreter = Interpreter()
        interpreter.evaluate(program)

        self.assertEqual("Hello World!\n", interpreter.root_environment.get('result'))


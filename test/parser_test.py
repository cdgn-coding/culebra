import unittest.mock
from typing import cast
from unittest import TestCase, skip
from culebra.parser import Parser
from culebra.lexer import Lexer
from culebra.ast import Program, Assignment, Identifier, LiteralValue
from culebra.token import TokenType, Token


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

        expected_identifier = Identifier(Token(TokenType.IDENTIFIER, "x", unittest.mock.ANY), "x")
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
        self.assertEqual('Assignment(Identifier(x), Integer(1))', repr(actual_assignment))

    def test_parse_literal_expressions_by_data_type(self):
        sources = [
            "x = 1",
            "x = 1.0",
            'x = "1.0"',
            "x = true",
            "x = false",
        ]

        expected = [
            "Assignment(Identifier(x), Integer(1))",
            "Assignment(Identifier(x), Float(1.0))",
            'Assignment(Identifier(x), String(1.0))',
            "Assignment(Identifier(x), Bool(True))",
            "Assignment(Identifier(x), Bool(False))",
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
        self.assertEqual('Assignment(Identifier(x), PlusOperation(Integer(1), Integer(1)))', repr(program))

    def test_parse_minus_expression(self):
        source = "x = 1 - 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), MinusOperation(Integer(1), Integer(1)))', repr(program))

    def test_parse_multiplication_expressions(self):
        source = "x = 1 * 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), MultiplicationOperation(Integer(1), Integer(2)))', repr(program))

    def test_parse_division_expressions(self):
        source = "x = 1 / 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), DivisionOperation(Integer(1), Integer(2)))', repr(program))

    def test_parse_recursive_arithmetic(self):
        source = "x = 2 + 3 * 2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), PlusOperation(Integer(2), '
 'MultiplicationOperation(Integer(3), Integer(2))))', repr(program))

    def test_parse_multiple_recursive_arithmetic(self):
        source = "x = 2 + 3 * 2\ny = 1.0 + 1.0 / 2.0"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual("\n".join([
            'Assignment(Identifier(x), PlusOperation(Integer(2), MultiplicationOperation(Integer(3), Integer(2))))',
            'Assignment(Identifier(y), PlusOperation(Float(1.0), DivisionOperation(Float(1.0), Float(2.0))))']), repr(program)
        )

    def test_parse_all_arithmetic_operations(self):
        source = "x = 1 + 2 * 3 + 4 / 5"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), PlusOperation(PlusOperation(Integer(1), '
 'MultiplicationOperation(Integer(2), Integer(3))), '
 'DivisionOperation(Integer(4), Integer(5))))', repr(program))

    def test_and_expression(self):
        source = "x = true and false"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(
            'Assignment(Identifier(x), AndOperation(Bool(True), Bool(False)))', repr(program))

    def test_identifier_factor(self):
        source = "x = x + 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), PlusOperation(Identifier(x), Integer(1)))', repr(program))


    def test_comparison_operators(self):
        source = "x = 2 >= 1"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Assignment(Identifier(x), GreaterOrEqualOperation(Integer(2), Integer(1)))', repr(program))

    def test_negative_numbers(self):
        source = "x = -2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        self.assertEqual('Assignment(Identifier(x), NegativeOperation(Integer(2)))', repr(program))


    def test_sum_negative_numbers(self):
        source = "x = -2 + -2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(x), NegativeOperation(PlusOperation(Integer(2), NegativeOperation(Integer(2)))))'
        self.assertEqual(expected, repr(program))

    def test_sum_not_unary(self):
        source = "x = not true"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(x), NotOperation(Bool(True)))'
        self.assertEqual(expected, repr(program))

    def test_function_call(self):
        source = "x = print()"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(x), FunctionCall(Identifier(print), []))'
        self.assertEqual(expected, repr(program))

    def test_function_as_statement(self):
        source = """
a = 1
def fn():
    a = 10
fn()
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(a), Integer(1))\nFunctionDefinition(Identifier(fn), [], [Assignment(Identifier(a), Integer(10))])\nFunctionCall(Identifier(fn), [])'
        self.assertEqual(expected, repr(program))

    def test_function_call_with_arguments(self):
        source = "x = print(1, 2, 3)"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(x), FunctionCall(Identifier(print), [Integer(1), Integer(2), Integer(3)]))'
        self.assertEqual(expected, repr(program))

    def test_function_call_with_arguments_error(self):
        source = "x = print(1, 2, 3"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Expected COMMA, RPAREN, got NEWLINE instead in position 17', str(parser.last_error))

    def test_parentheses(self):
        source = "x = 2 * (1+1)"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual(None, parser.last_error)
        expected = 'Assignment(Identifier(x), MultiplicationOperation(Integer(2), PlusOperation(Integer(1), Integer(1))))'
        self.assertEqual(expected, repr(program))

    def test_parentheses_error(self):
        source = "x = 2 * (1+2"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertTrue(isinstance(program, Program))
        self.assertEqual('Expected RPAREN, got NEWLINE instead in position 12', str(parser.last_error))

    def test_expected_identifier_or_literal_error(self):
        source = "x = +"
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        _ = parser.parse()

        self.assertEqual('Expected IDENTIFIER, NUMBER, STRING, BOOLEAN, FLOAT, got PLUS instead in position 4', str(parser.last_error))
    def test_function_definition(self):
        source = """
def sum(x, y):
    return x + y
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'FunctionDefinition(Identifier(sum), [Identifier(x), Identifier(y)], [ReturnStatement(PlusOperation(Identifier(x), Identifier(y)))])'
        self.assertEqual(expected, repr(program))

    def test_function_definition_ignored_newlines(self):
        source = """
def sum(x, y):



    return x + y
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'FunctionDefinition(Identifier(sum), [Identifier(x), Identifier(y)], [ReturnStatement(PlusOperation(Identifier(x), Identifier(y)))])'
        self.assertEqual(expected, repr(program))

    def test_if_statement(self):
        source = """
if true:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'Conditional(Bool(True)) Then [Identifier(pass)]'
        self.assertEqual(expected, repr(program))

    def test_if_statement_else(self):
        source = """
if true:
    pass
else:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'Conditional(Bool(True)) Then [Identifier(pass)] Else [Conditional(Bool(True)) Then [Identifier(pass)]]'
        self.assertEqual(expected, repr(program))

    def test_if_statement_elif(self):
        source = """
if true:
    pass
elif false:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'Conditional(Bool(True)) Then [Identifier(pass)] Else [Conditional(Bool(False)) Then [Identifier(pass)]]'
        self.assertEqual(expected, repr(program))

    def test_if_statement_else_elif(self):
        source = """
if true:
    pass
elif true:
    pass
else:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'Conditional(Bool(True)) Then [Identifier(pass)] Else [Conditional(Bool(True)) Then [Identifier(pass)] Else [Conditional(Bool(True)) Then [Identifier(pass)]]]'
        self.assertEqual(expected, repr(program))

    def test_elif_after_else(self):
        source = """
if true:
    pass
else:
    pass
elif true:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        parser.parse()
        self.assertEqual('Expected IDENTIFIER, NUMBER, STRING, BOOLEAN, FLOAT, got ELIF instead in position 33', str(parser.last_error))

    def test_else_after_else(self):
        source = """
if true:
    pass
else:
    pass
else:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        parser.parse()
        self.assertEqual('Expected IDENTIFIER, NUMBER, STRING, BOOLEAN, FLOAT, got ELSE instead in position 33', str(parser.last_error))

    def test_while(self):
        source = """
while true:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'While(Bool(True)) Then [Identifier(pass)]'
        self.assertEqual(expected, repr(program))

    def test_for(self):
        source = """
for i = 0; i < 10; i = i + 1:
    pass
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'For(Assignment(Identifier(i), Integer(0)); LessOperation(Identifier(i), Integer(10)); Assignment(Identifier(i), PlusOperation(Identifier(i), Integer(1)))) Then [Identifier(pass)]'
        self.assertEqual(expected, repr(program))

    def test_recursion_with_arguments(self):
        source = """
def fn(a):
    if a > 2:
        return a * fn(a - 1)
    return a
result = fn(4)
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'FunctionDefinition(Identifier(fn), [Identifier(a)], [Conditional(GreaterOperation(Identifier(a), Integer(2))) Then [ReturnStatement(MultiplicationOperation(Identifier(a), FunctionCall(Identifier(fn), [MinusOperation(Identifier(a), Integer(1))])))], ReturnStatement(Identifier(a))])\nAssignment(Identifier(result), FunctionCall(Identifier(fn), [Integer(4)]))'
        self.assertEqual(expected, repr(program))

    def test_string_escape_sequences(self):
        test_cases = [
            ('"hello\\nworld"', "hello\nworld"),
            ('"hello\\tworld"', "hello\tworld"),
            ('"hello\\\\world"', "hello\\world"),
            ('"hello\\"world\\""', 'hello"world"'),
            ('"\\r\\n\\f\\b"', '\r\n\f\b'),
            ('"no\\escape\\here"', 'no\\escape\\here'),
            ('"""multi\\nline\\n"""', 'multi\nline\n'),
        ]

        for source, expected in test_cases:
            sequence = Lexer().tokenize(source)
            parser = Parser(sequence)
            program = parser.parse()
            self.assertEqual(len(program.statements), 1)
            
            expr_stmt = program.statements[0]
            self.assertIsInstance(expr_stmt, LiteralValue)
            
            string_literal = expr_stmt.value
            self.assertIsInstance(string_literal, str)
            self.assertEqual(string_literal, expected)

    def test_assigment_of_array(self):
        source = """
tape = [0,0,0,0]
"""
        sequence = Lexer().tokenize(source)
        parser = Parser(sequence)
        program = parser.parse()
        self.assertEqual(False, parser.has_error)
        expected = 'Assignment(Identifier(tape), Array([Integer(0), Integer(0), Integer(0), Integer(0)]))'
        self.assertEqual(expected, repr(program))

    def test_array_literals(self):
        test_cases = [
            ("[1,2,3]", "Array([Integer(1), Integer(2), Integer(3)])"),
            ("[]", "Array([])"),
            ("[1.0, true, \"hello\"]", "Array([Float(1.0), Bool(True), String(hello)])"),
            ("[[1,2],[3,4]]", "Array([Array([Integer(1), Integer(2)]), Array([Integer(3), Integer(4)])])")
        ]

        for source, expected in test_cases:
            sequence = Lexer().tokenize(source)
            parser = Parser(sequence)
            program = parser.parse()
            self.assertEqual(False, parser.has_error)
            self.assertEqual(expected, repr(program.statements[0]))

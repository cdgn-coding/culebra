from unittest import TestCase
from llvmlite import binding as llvm
from src.compiler import Compiler
from src.token import Token, TokenType
from src.ast import Program, Assignment, Identifier, Integer, PlusOperation

class TestCompiler(TestCase):
    def test_compiler_success(self):
        # Create module and compile
        src = "x = 1 + 2"
        compiler = Compiler(src)
        result, engine = compiler.execute_jit()

        # Main method should return 0
        self.assertEqual(result, 0)

        # x should be 3
        actual_value = compiler.get_symbol_value(engine, "x")
        self.assertEqual(3, actual_value)

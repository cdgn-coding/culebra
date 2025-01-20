from unittest import TestCase
from llvmlite import binding as llvm
from src.compiler import Compiler
from src.token import Token, TokenType
from src.ast import Program, Assignment, Identifier, Integer, PlusOperation

class TestCompiler(TestCase):
    @staticmethod
    def create_test_ast():
        # Create AST for: x = 1 + 1
        one = Integer(Token(TokenType.NUMBER, "1"), 1)
        x_ident = Identifier(Token(TokenType.IDENTIFIER, "x"), "x")
        plus_op = PlusOperation(Token(TokenType.PLUS, "+"), one, one)
        assignment = Assignment(Token(TokenType.ASSIGN, "="), x_ident, plus_op)
        return Program([assignment])

    def test_compiler_execution(self):
        # Initialize LLVM execution engine
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Create module and compile
        ast = self.create_test_ast()
        compiler = Compiler(ast)
        ir_output = compiler.compile()
        
        # Create execution engine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Create module from IR
        mod = llvm.parse_assembly(ir_output)
        mod.verify()
        
        # Add module to execution engine
        engine = llvm.create_mcjit_compiler(mod, target_machine)
        
        # Get function pointer and execute
        func_ptr = engine.get_function_address("main")
        
        # Create Python callable with int64 return type
        from ctypes import CFUNCTYPE, c_int64
        cfunc = CFUNCTYPE(c_int64)(func_ptr)
        
        # Execute and verify result
        result = cfunc()
        self.assertEqual(result, 2)  # Verify 1 + 1 = 2
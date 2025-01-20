from typing import Optional

from llvmlite import ir
from llvmlite import binding as llvm

from src.ast import Program, Assignment, Integer, DivisionOperation, MultiplicationOperation, MinusOperation, \
    PlusOperation, Identifier, Float
from src.lexer import Lexer
from src.parser import Parser


class Compiler:
    def __init__(self, source: str):
        self.lexer = Lexer()
        self.seq = self.lexer.tokenize(source)
        self.parser = Parser(self.seq)
        self.ast = self.parser.parse()

        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create module and builder
        self.module = ir.Module(name="main")

        # Create symbol table for global scope
        self.symbol_table = {}
        
        # Setup main function to return i64 instead of void
        func_type = ir.FunctionType(ir.IntType(64), [])
        main_func = ir.Function(self.module, func_type, name="main")
        block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        

    def compile(self) -> str:
        """Assembly code of the module"""
        # Compile the AST
        self._compile_ast(self.ast)
        self.builder.ret(ir.Constant(ir.IntType(64), 0))
        return str(self.module)

    def _compile_ast(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self._compile_ast(statement)
        
        elif isinstance(node, Assignment):
            value = self._compile_ast(node.value)
            var_name = node.identifier.value
            var: Optional[ir.GlobalVariable] = None

            if var_name not in self.symbol_table:
                # Create new global variable
                if isinstance(value.type, ir.IntType):
                    var = ir.GlobalVariable(self.module, ir.IntType(64), var_name)
                    var.initializer = value.type(0)
                elif isinstance(value.type, ir.DoubleType):
                    var = ir.GlobalVariable(self.module, ir.DoubleType(), var_name)
                    var.initializer = value.type(0)
                self.symbol_table[var_name] = var
            
            # Store value and keep track of it
            self.builder.store(value, self.symbol_table[var_name])

        elif isinstance(node, Integer):
            return ir.Constant(ir.IntType(64), node.value)
            
        elif isinstance(node, Float):
            return ir.Constant(ir.DoubleType(), node.value)
            
        elif isinstance(node, Identifier):
            var = self.symbol_table[node.value]
            return self.builder.load(var)
            
        elif isinstance(node, PlusOperation):
            left = self._compile_ast(node.left)
            right = self._compile_ast(node.right)
            return self.builder.add(left, right)
            
        elif isinstance(node, MinusOperation):
            left = self._compile_ast(node.left)
            right = self._compile_ast(node.right)
            return self.builder.sub(left, right)
            
        elif isinstance(node, MultiplicationOperation):
            left = self._compile_ast(node.left)
            right = self._compile_ast(node.right)
            return self.builder.mul(left, right)
            
        elif isinstance(node, DivisionOperation):
            left = self._compile_ast(node.left)
            right = self._compile_ast(node.right)
            return self.builder.sdiv(left, right) if isinstance(left.type, ir.IntType) else self.builder.fdiv(left, right)

    def execute_jit(self):
        """Execute the compiled code using JIT and return the result"""
        # Initialize LLVM if not already done
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Get IR
        ir_output = self.compile()
        
        # Create module from IR
        mod = llvm.parse_assembly(ir_output)
        mod.verify()
        
        # Create execution engine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        engine = llvm.create_mcjit_compiler(mod, target_machine)
        
        # Get function pointer and execute
        func_ptr = engine.get_function_address("main")
        
        # Create Python callable with int64 return type
        from ctypes import CFUNCTYPE, c_int64
        cfunc = CFUNCTYPE(c_int64)(func_ptr)
        
        # Execute and return result
        return cfunc(), engine

    def get_symbol_value(self, engine, var_name: str):
        """Get the value of a symbol after execution"""
        if var_name not in self.symbol_table:
            raise KeyError(f"Variable {var_name} not found in symbol table")

        # Get the global variable from the module
        global_var = self.symbol_table[var_name]

        # Get the address of the global variable
        var_addr = engine.get_global_value_address(var_name)

        # Create a proper ctypes pointer type based on the variable type
        from ctypes import POINTER, c_int64, c_double, cast

        if isinstance(global_var.type.pointee, ir.IntType):
            ptr_type = POINTER(c_int64)
            value = cast(var_addr, ptr_type).contents.value
        elif isinstance(global_var.type.pointee, ir.DoubleType):
            ptr_type = POINTER(c_double)
            value = cast(var_addr, ptr_type).contents.value
        else:
            raise ValueError(f"Unsupported type for variable {var_name}")

        return value
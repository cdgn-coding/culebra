from llvmlite import ir
from llvmlite import binding as llvm

from src.ast import Program, Assignment, Integer, DivisionOperation, MultiplicationOperation, MinusOperation, \
    PlusOperation, Identifier, Float


class Compiler:
    def __init__(self, source: Program):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create module and builder
        self.module = ir.Module(name="main")
        self.builder = None
        
        # Create symbol table for global scope
        self.symbol_table = {}
        
        # Setup main function to return i64 instead of void
        func_type = ir.FunctionType(ir.IntType(64), [])
        main_func = ir.Function(self.module, func_type, name="main")
        block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        # Store the last computed value for return
        self.last_value = None
        
        # Parse source to AST
        self.ast = source  # Assuming source is already an AST Program node

    def compile(self):
        # Compile the AST
        self._compile_ast(self.ast)
        
        # Return the last computed value
        if self.last_value is None:
            self.builder.ret(ir.Constant(ir.IntType(64), 0))
        else:
            # Load the value if it's a pointer (like a global variable)
            if isinstance(self.last_value.type, ir.PointerType):
                return_value = self.builder.load(self.last_value)
            else:
                return_value = self.last_value
            self.builder.ret(return_value)
            
        return str(self.module)

    def _compile_ast(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self._compile_ast(statement)
        
        elif isinstance(node, Assignment):
            value = self._compile_ast(node.value)
            var_name = node.identifier.value
            
            if var_name not in self.symbol_table:
                # Create new global variable
                if isinstance(value.type, ir.IntType):
                    var = ir.GlobalVariable(self.module, ir.IntType(64), var_name)
                elif isinstance(value.type, ir.DoubleType):
                    var = ir.GlobalVariable(self.module, ir.DoubleType(), var_name)
                var.initializer = value.type(0)
                self.symbol_table[var_name] = var
            
            # Store value and keep track of it
            self.builder.store(value, self.symbol_table[var_name])
            self.last_value = value  # Store the computed value
            
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

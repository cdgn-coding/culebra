from culebra import ast
from culebra.interpreter import evaluation_tree
from culebra.interpreter.environment import Environment
from culebra.interpreter.evaluation_tree import Identifier, Evaluable


class Interpreter:
    def __init__(self, program: ast.Program):
        self.program = program
        self.root_environment = Environment()
        self.tree = self.__build_tree(self.program)

    def evaluate(self):
        return self.tree.evaluate(self.root_environment)

    def __build_tree(self, node: ast.ASTNode) -> evaluation_tree.Evaluable:
        if isinstance(node, ast.Identifier):
            name = node.value
            token = node.token
            return evaluation_tree.Identifier(name, token)
        if isinstance(node, ast.Assignment):
            token = node.token
            identifier = Identifier(node.identifier.value, node.identifier.token)
            value = self.__build_tree(node.value)
            return evaluation_tree.Assignment(identifier, value, token)
        if isinstance(node, ast.LiteralValue):
            return evaluation_tree.Literal(node.value, node.token)
        if isinstance(node, (ast.Program, ast.Block)):
            statements = [self.__build_tree(node) for node in node.statements]
            return  evaluation_tree.Block(statements)
        if isinstance(node, ast.BinaryOperation):
            token = node.token
            left = self.__build_tree(node.left)
            right = self.__build_tree(node.right)
            return evaluation_tree.BinaryOperation(left, right, token)
        if isinstance(node, ast.PrefixOperation):
            token = node.token
            expression = self.__build_tree(node.value)
            return evaluation_tree.UnaryOperation(expression, token)
        if isinstance(node, ast.Conditional):
            token = node.token
            condition = self.__build_tree(node.condition)
            body = self.__build_tree(node.body)
            otherwise = None if not node.otherwise else self.__build_tree(node.otherwise)
            return evaluation_tree.Conditional(condition, body, otherwise, token)
        if isinstance(node, ast.While):
            token = node.token
            condition = self.__build_tree(node.condition)
            body = self.__build_tree(node.body)
            return evaluation_tree.While(condition, body, token)
        if isinstance(node, ast.For):
            token = node.token
            condition = self.__build_tree(node.condition)
            body = self.__build_tree(node.body)
            pre = self.__build_tree(node.pre)
            post = self.__build_tree(node.post)
            return evaluation_tree.For(condition, body, pre, post, token)
        if isinstance(node, ast.FunctionDefinition):
            token = node.token
            body = self.__build_tree(node.body)
            arguments = [arg.value for arg in node.arguments]
            name = node.name.value
            return evaluation_tree.Function(name, arguments, body, token)
        if isinstance(node, ast.FunctionCall):
            token = node.token
            name = node.function.value
            arguments = [self.__build_tree(arg) for arg in node.arguments]
            return evaluation_tree.FunctionCall(name, arguments, token)
        if isinstance(node, ast.ReturnStatement):
            token = node.token
            expression = self.__build_tree(node.value)
            return evaluation_tree.Return(expression, token)

        raise TypeError(f"Unexpected type {type(node)}")
from culebra import ast
from culebra.interpreter import evaluation_tree
from culebra.interpreter.environment import Environment
from culebra.interpreter.evaluation_tree import Identifier, Evaluable


class Interpreter(Evaluable):
    def __init__(self, program: ast.Program):
        self.program = program
        self.root_environment = Environment()
        self.tree = self.__build_tree(self.program, self.root_environment)

    def evaluate(self):
        return self.tree.evaluate()

    def __build_tree(self, node: ast.ASTNode, current_environment: Environment) -> evaluation_tree.Evaluable:
        if isinstance(node, ast.Identifier):
            name = node.value
            token = node.token
            return evaluation_tree.Identifier(name, current_environment, token)
        if isinstance(node, ast.Assignment):
            token = node.token
            identifier = Identifier(node.identifier.value, current_environment, node.identifier.token)
            value = self.__build_tree(node.value, current_environment)
            return evaluation_tree.Assignment(identifier, value, current_environment, token)
        if isinstance(node, ast.LiteralValue):
            return evaluation_tree.Literal(node.value, node.token)
        if isinstance(node, (ast.Program, ast.Block)):
            statements = [self.__build_tree(node, current_environment) for node in node.statements]
            return  evaluation_tree.Block(statements)
        if isinstance(node, ast.BinaryOperation):
            token = node.token
            left = self.__build_tree(node.left, current_environment)
            right = self.__build_tree(node.right, current_environment)
            return evaluation_tree.BinaryOperation(left, right, token)
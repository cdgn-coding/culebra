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
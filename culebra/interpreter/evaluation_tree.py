from abc import ABC, abstractmethod
from typing import Union

from culebra.interpreter.environment import Environment
from culebra.token import Token, TokenType


class Evaluable[T](ABC):
    @abstractmethod
    def evaluate(self) -> T:
        pass

class Executable(Evaluable[None]):
    @abstractmethod
    def evaluate(self) -> None:
        pass

LITERAL_TYPES = Union[int, float, bool, str]
class Literal[T = LITERAL_TYPES](Evaluable[T]):
    def __init__(self, value: T, token: Token):
        self.value = value
        self.token = token

    @property
    def type(self):
        return type(self.value)

    def evaluate(self) -> T:
        return self.value

class Identifier(Evaluable):
    def __init__(self, name: str, environment: Environment, token: Token):
        self.name = name
        self.environment = environment
        self.token = token

    def evaluate(self):
        return self.environment.get(self.name)


class Assignment(Executable):
    def __init__(self, identifier: Identifier, expression: Evaluable, environment: Environment, token: Token):
        self.identifier = identifier
        self.expression = expression
        self.environment = environment
        self.token = token

    def evaluate(self):
        self.environment.assign(self.identifier.name, self.expression.evaluate())

class Block(Executable):
    def __init__(self, body: list[Evaluable]):
        self.body = body

    def evaluate(self):
        for evaluable in self.body:
            evaluable.evaluate()

class BinaryOperation(Evaluable):
    def __init__(self, left: Evaluable, right: Evaluable, token: Token):
        self.left = left
        self.right = right
        self.token = token

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        # Arithmetic
        if self.token.type == TokenType.PLUS:
            return left + right
        elif self.token.type == TokenType.MINUS:
            return left - right
        elif self.token.type == TokenType.MUL:
            return left * right
        elif self.token.type == TokenType.DIV:
            return left / right

        # Comparison
        elif self.token.type == TokenType.EQUAL:
            return left == right
        elif self.token.type == TokenType.NOT_EQUAL:
            return left != right
        elif self.token.type == TokenType.LESS:
            return left < right
        elif self.token.type == TokenType.GREATER:
            return left > right
        elif self.token.type == TokenType.LESS_EQ:
            return left <= right
        elif self.token.type == TokenType.GREATER_EQ:
            return left >= right

        # Logical
        elif self.token.type == TokenType.OR:
            return left or right
        elif self.token.type == TokenType.AND:
            return left and right

        raise AssertionError(f"Unexpected binary operation token {self.token}")

class UnaryOperation(Evaluable):
    def __init__(self, expression: Evaluable, token: Token):
        self.expression = expression
        self.token = token

    def evaluate(self):
        expression = self.expression.evaluate()

        if self.token.type == TokenType.MINUS:
            return -expression
        elif self.token.type == TokenType.NOT:
            return not expression

        raise AssertionError(f"Unexpected unary operation token {self.token}")
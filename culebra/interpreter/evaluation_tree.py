from abc import ABC, abstractmethod
from typing import Union, Optional, List

from culebra.interpreter.environment import Environment
from culebra.token import Token, TokenType


class Evaluable[T](ABC):
    @abstractmethod
    def evaluate(self, environment: Environment) -> T:
        pass


class Executable(Evaluable[None]):
    @abstractmethod
    def evaluate(self, environment: Environment) -> None:
        pass


LITERAL_TYPES = Union[int, float, bool, str]


class Literal[T = LITERAL_TYPES](Evaluable[T]):
    def __init__(self, value: T, token: Token):
        self.value = value
        self.token = token

    @property
    def type(self):
        return type(self.value)

    def evaluate(self, environment: Environment) -> T:
        return self.value


class Identifier(Evaluable):
    def __init__(self, name: str, token: Token):
        self.name = name
        self.token = token

    def evaluate(self, environment: Environment):
        return environment.get(self.name)


class Assignment(Executable):
    def __init__(self, identifier: Identifier, expression: Evaluable, token: Token):
        self.identifier = identifier
        self.expression = expression
        self.token = token

    def evaluate(self, environment: Environment):
        environment.assign(self.identifier.name, self.expression.evaluate(environment))


class Block(Executable):
    def __init__(self, body: List[Evaluable]):
        self.body = body

    def evaluate(self, environment: Environment):
        for evaluable in self.body:
            evaluable.evaluate(environment)



class BinaryOperation(Evaluable):
    def __init__(self, left: Evaluable, right: Evaluable, token: Token):
        self.left = left
        self.right = right
        self.token = token

    def evaluate(self, environment: Environment):
        left = self.left.evaluate(environment)
        right = self.right.evaluate(environment)

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

    def evaluate(self, environment: Environment):
        expression = self.expression.evaluate(environment)

        if self.token.type == TokenType.MINUS:
            return -expression
        elif self.token.type == TokenType.NOT:
            return not expression

        raise AssertionError(f"Unexpected unary operation token {self.token}")


class Conditional(Evaluable):
    def __init__(self, condition: Evaluable, body: Evaluable, otherwise: Optional['Conditional'], token: Token):
        self.condition = condition
        self.body = body
        self.otherwise = otherwise
        self.token = token

    def evaluate(self, environment: Environment):
        condition = self.condition.evaluate(environment)
        if condition:
            self.body.evaluate(environment)
        elif self.otherwise:
            self.otherwise.evaluate(environment)


class While(Evaluable):
    def __init__(self, condition: Evaluable, body: Evaluable, token: Token):
        self.condition = condition
        self.body = body
        self.token = token

    def evaluate(self, environment: Environment):
        while self.condition.evaluate(environment):
            self.body.evaluate(environment)


class For(Evaluable):
    def __init__(self, condition: Evaluable, body: Evaluable, pre: Evaluable, post: Evaluable, token: Token):
        self.condition = condition
        self.body = body
        self.pre = pre
        self.post = post
        self.token = token

    def evaluate(self, environment: Environment):
        self.pre.evaluate(environment)
        while self.condition.evaluate(environment):
            self.body.evaluate(environment)
            self.post.evaluate(environment)


class Function(Evaluable):
    def __init__(self, name: str, arguments: List[str], body: Evaluable, token: Token):
        self.name = name
        self.body = body
        self.arguments = arguments
        self.token = token

    def evaluate(self, environment: Environment):
        environment.assign(self.name, self)


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value


class Return(Evaluable):
    def __init__(self, expression: Evaluable, token: Token):
        self.expression = expression
        self.token = token

    def evaluate(self, environment: Environment):
        raise ReturnValue(self.expression.evaluate(environment))


class FunctionCall(Evaluable):
    def __init__(self, function_name: str, arguments: List[Evaluable], token: Token):
        self.function = function_name
        self.arguments = arguments
        self.token = token

    def evaluate(self, environment: Environment):
        function = environment.get(self.function)
        assert isinstance(function, Function)
        function_environment = environment.create_child()
        for name, value in zip(function.arguments, self.arguments):
            function_environment.assign(name, value.evaluate(environment))
        try:
            function.body.evaluate(function_environment)
        except ReturnValue as ret:
            return ret.value
        return None

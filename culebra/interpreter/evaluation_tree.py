from abc import ABC, abstractmethod
from typing import Union

from culebra.interpreter.environment import Environment
from culebra.token import Token


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
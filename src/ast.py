from abc import ABC, abstractmethod
from src.token import Token
from typing import List
class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def token_type(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return self.__repr__()

class Statement(ASTNode, ABC):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def token_type(self) -> str:
        return str(self.token.type)

class Expression(ASTNode, ABC):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def token_type(self) -> str:
        return str(self.token.type)

class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""

    def token_type(self) -> str:
        return ''

    def __repr__(self) -> str:
        return "\n".join([str(stmt) for stmt in self.statements])

class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"


class Assignment(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        super().__init__(token)
        self.identifier = identifier
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.identifier} = {self.value}"

class Integer(Expression):
    def __init__(self, token: Token, value: int):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"

class Float(Expression):
    def __init__(self, token: Token, value: float):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"

class String(Expression):
    def __init__(self, token: Token, value: str):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"

class Bool(Expression):
    def __init__(self, token: Token, value: bool):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"

class PlusOperation(Expression):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.left} + {self.right}"

class MinusOperation(Expression):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.left} - {self.right}"

class MultiplicationOperation(Expression):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.left} * {self.right}"

class DivisionOperation(Expression):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.left} / {self.right}"
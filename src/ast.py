from abc import ABC, abstractmethod
from src.token import Token
from typing import List
class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return self.__repr__()

class Statement(ASTNode):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

class Expression(ASTNode):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""

    def __repr__(self) -> str:
        return "\n".join([str(stmt) for stmt in self.statements])

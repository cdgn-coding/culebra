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
    
    def tree_str(self, level: int = 0, is_last: bool = True) -> str:
        prefix = "    " * (level - 1) + ("└── " if is_last else "├── ") if level > 0 else ""
        result = prefix + self.token_type()
        
        # Handle different node types
        if isinstance(self, Program):
            children = self.statements
        elif isinstance(self, BinaryOperation):
            children = [self.left, self.right]
        elif isinstance(self, Assignment):
            children = [self.identifier, self.value]
        elif isinstance(self, (NegativeOperation, NotOperation)):
            children = [self.value]
        elif isinstance(self, LiteralValue):
            return prefix + f"{self.token_type()}({self.value})"
        else:
            children = []

        # Recursively build tree for children
        for i, child in enumerate(children):
            result += "\n" + child.tree_str(level + 1, i == len(children) - 1)
            
        return result

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

class LiteralValue[T](Expression, ABC):
    def __init__(self, token: Token, value: T):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.value}"

class Identifier(LiteralValue[str]):
    def __init__(self, token: Token, value: str):
        super().__init__(token, value)

class Assignment(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        super().__init__(token)
        self.identifier = identifier
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.identifier} = {self.value}"

class Integer(LiteralValue[int]):
    def __init__(self, token: Token, value: int):
        super().__init__(token, value)

class Float(LiteralValue[float]):
    def __init__(self, token: Token, value: float):
        super().__init__(token, value)

class String(LiteralValue[str]):
    def __init__(self, token: Token, value: str):
        super().__init__(token, value)

class Bool(LiteralValue[bool]):
    def __init__(self, token: Token, value: bool):
        super().__init__(token, value)

class BinaryOperation(Expression, ABC):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.token_type()} {self.left} {self.token.literal} {self.right}"

class PlusOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class MinusOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)


class MultiplicationOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class DivisionOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class AndOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class OrOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class GreaterOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class GreaterOrEqualOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class LessOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)


class LessOrEqualOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class EqualOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class NotEqualOperation(BinaryOperation):
    def __init__(self, token: Token, left: Expression, right: Expression):
        super().__init__(token, left, right)

class NegativeOperation(Expression):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type()}(PrefixOperation) {self.token_literal()} {self.value}"

class NotOperation(Expression):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token)
        self.value = value
    def __repr__(self) -> str:
        return f"{self.token_type()} {self.token_literal()} {self.value}"


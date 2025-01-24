from abc import ABC, abstractmethod
from src.token import Token, TokenType
from typing import List


class ASTNode(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    @abstractmethod
    def children(self) -> List['ASTNode']:
        pass

    @property
    def node_name(self) -> str:
        return self.__class__.__name__

    def pretty(self, level: int = 1) -> str:
        is_last = len(self.children) == 0
        if is_last:
            prefix = "    " * (level - 1)
            return f"{prefix}└──{repr(self)}"

        prefix = "    " * (level - 1) +  "├── "
        result = prefix + self.node_name

        for i, child in enumerate(self.children):
            result += "\n" + child.pretty(level + 1)

        return result


class TokenizedASTNode(ASTNode, ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def token_type(self) -> TokenType:
        pass

class Statement(TokenizedASTNode, ABC):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def token_type(self) -> TokenType:
        return self.token.type

class Expression(TokenizedASTNode, ABC):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def token_type(self) -> TokenType:
        return self.token.type

class Block(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def __repr__(self) -> str:
        return "\n".join([str(stmt) for stmt in self.statements])

    @property
    def children(self) -> List['ASTNode']:
        return self.statements

class Program(Block):
    def __init__(self, statements: List[Statement]):
        super().__init__(statements)

class LiteralValue[T](Expression, ABC):
    def __init__(self, token: Token, value: T):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.node_name}({self.value})"

    @property
    def children(self) -> List['ASTNode']:
        return []


class Identifier(LiteralValue[str]):
    def __init__(self, token: Token, value: str):
        super().__init__(token, value)

class Assignment(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        super().__init__(token)
        self.identifier = identifier
        self.value = value

    def __repr__(self) -> str:
        return f"{self.node_name}({self.identifier}, {self.value})"

    @property
    def children(self) -> List['ASTNode']:
        return [self.identifier, self.value]

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
        return f"{self.node_name}({self.left}, {self.right})"

    @property
    def children(self) -> List['ASTNode']:
        return [self.left, self.right]

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

class PrefixOperation(Expression, ABC):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.node_name}({self.value})"

    @property
    def children(self) -> List['ASTNode']:
        return [self.value]

class NegativeOperation(PrefixOperation):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token, value)

class NotOperation(PrefixOperation):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token, value)


class FunctionCall(Expression, ABC):
    def __init__(self, token: Token, function: Identifier, arguments: List[Expression]):
        super().__init__(token)
        self.function = function
        self.arguments = arguments

    @property
    def children(self) -> List['ASTNode']:
        return self.arguments

    @property
    def node_name(self) -> str:
        return f"{self.__class__.__name__}({self.function})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.function}, {self.arguments})"

class FunctionDefinition(Statement):
    def __init__(self, token: Token, name: Identifier, arguments: List[Identifier], body: Block):
        super().__init__(token)
        self.name = name
        self.arguments = arguments
        self.body = body

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.arguments}, {self.body.statements})"

    @property
    def node_name(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.arguments})"

    @property
    def children(self) -> List['ASTNode']:
        return self.body.children

class ReturnStatement(Statement):
    def __init__(self, token: Token, value: Expression):
        super().__init__(token)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    @property
    def children(self) -> List['ASTNode']:
        return [self.value]

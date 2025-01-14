from typing import List
import re
from src.token import Token, TokenType

class Lexer:
    def __init__(self, text: str):
        self.text = text

    def tokenize(self) -> List[Token]:
        tokens = []
        i = 0
        while i < len(self.text):
            chunk = self.text[i:]
            is_legal = False

            for token_type, regex in TokenRegex.items():
                match = regex.match(chunk)
                if match:
                    value = match.group(0)
                    token = Token(token_type, value)
                    tokens.append(token)
                    i += len(value) + 1
                    is_legal = True
                    break

            if not is_legal:
                char = chunk[0]
                token = Token(TokenType.ILLEGAL_CHARACTER, char)
                tokens.append(token)
                i += 1

        tokens.append(Token(TokenType.EOF, ""))

        return tokens

TokenRegex = {
    TokenType.NUMBER: re.compile(r"^([0-9]+)"),
}

#!/usr/bin/env python3

from typing import List
import re
import sys
from typing import NoReturn
from src.token import Token, TokenType

class Lexer:
    def __init__(self, text: str):
        self.text = text.strip()
        self.current_indent = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        i = 0
        while i < len(self.text):
            chunk = self.text[i:]
            is_legal = False

            if self.text[i] == '\n':
                indent = 0
                i += 1
                while i < len(self.text):
                    match = IndentRegex.match(self.text[i:])
                    if not match: break
                    indent += 1
                    i += match.end()

                if indent != self.current_indent:
                    tokens.append(Token(TokenType.INDENT, indent))
                    self.current_indent = indent

                continue

            for token_type, regex in TokenRegex.items():
                match = regex.match(chunk)
                if match:
                    value = match.group(0)
                    if token_type not in [TokenType.WHITESPACE, TokenType.LINE_COMMENT]:
                        token = Token(token_type, value)
                        tokens.append(token)
                    i += len(value)
                    is_legal = True
                    break

            if not is_legal:
                char = chunk[0]
                token = Token(TokenType.ILLEGAL_CHARACTER, char)
                tokens.append(token)
                i += 1

        if self.current_indent > 0:
            tokens.append(Token(TokenType.INDENT, 0))

        tokens.append(Token(TokenType.EOF, ""))

        return tokens

IndentRegex = re.compile(r"^(\t|    )")

TokenRegex = {
    TokenType.WHITESPACE: re.compile(r"^[\s]+"),
    # Matches line comments, everything except newlines
    TokenType.LINE_COMMENT: re.compile(r"^#[^\n]*"),

    # Keywords
    TokenType.IF: re.compile(r"^if"),
    TokenType.ELSE: re.compile(r"^else"),
    TokenType.ELIF: re.compile(r"^elif"),
    TokenType.WHILE: re.compile(r"^while"),
    TokenType.FOR: re.compile(r"^for"),
    TokenType.BREAK: re.compile(r"^break"),
    TokenType.CONTINUE: re.compile(r"^continue"),
    TokenType.RETURN: re.compile(r"^return"),
    TokenType.FUNCTION_DEFINITION: re.compile(r"^def"),
    TokenType.BOOLEAN: re.compile(r"^(true|false)"),
    
    # Single-character tokens
    TokenType.LPAREN: re.compile(r"^\("),
    TokenType.RPAREN: re.compile(r"^\)"), 
    TokenType.LBRACE: re.compile(r"^{"),
    TokenType.RBRACE: re.compile(r"^}"),
    TokenType.LBRACKET: re.compile(r"^\["),
    TokenType.RBRACKET: re.compile(r"^\]"),
    TokenType.COMMA: re.compile(r"^,"),
    TokenType.SEMICOLON: re.compile(r"^;"),
    TokenType.COLON: re.compile(r"^:"),

    # Assignment after equals
    TokenType.EQUAL: re.compile(r"^=="),
    TokenType.ASSIGN: re.compile(r"^="),

    # Operators
    TokenType.PLUS: re.compile(r"^\+"),
    TokenType.MINUS: re.compile(r"^-"),
    TokenType.MUL: re.compile(r"^\*"),
    TokenType.DIV: re.compile(r"^/"),

    # Comparison operators
    TokenType.NOT_EQUAL: re.compile(r"^!="),
    TokenType.LESS_EQ: re.compile(r"^<="),
    TokenType.LESS: re.compile(r"^<"),
    TokenType.GREATER_EQ: re.compile(r"^>="),
    TokenType.GREATER: re.compile(r"^>"),

    # Literals
    TokenType.INVALID_IDENTIFIER: re.compile(r"^[0-9]+[a-zA-Z_][a-zA-Z0-9_]*"),
    TokenType.FLOAT: re.compile(r"^[0-9]+\.[0-9]+"),
    TokenType.NUMBER: re.compile(r"^([0-9]+)"),
    TokenType.IDENTIFIER: re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"),
    TokenType.STRING: re.compile(r'^"""[\s\S]*?"""|"[^"]*"'),
}

def print_welcome_message() -> None:
    """Print the initial welcome message and instructions."""
    print(r"""
      /^\/^\
    _|__|  O|
\/     /~   \_/ \
 \____|__________/  \
        \_______      \
                `\     \                 \
                  |     |                  \
                 /      /                    \
                /     /                       \\
              /      /                         \ \
             /     /                            \  \
           /     /             _----_            \   \
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~
    """)
    print("Welcome to the Culebra Lexer REPL!")
    print("Type 'exit' or press Ctrl+D to quit")
    print("Enter your code:")

def process_input(text: str) -> bool:
    """
    Process the input text through the lexer and print tokens.
    
    Args:
        text: The input string to tokenize
        
    Returns:
        bool: False if exit command, True otherwise
    """
    if text.lower().strip() == 'exit':
        print("Goodbye!")
        return False
        
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"Token({token.type}, '{token.literal}')")
    
    return True

def repl() -> NoReturn:
    """Run the REPL (Read-Eval-Print Loop)."""
    print_welcome_message()
    
    while True:
        try:
            text = input(">>> ")
            if not process_input(text):
                break
                
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received")
            continue
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)

def main() -> int:
    """
    Main entry point for the script.
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    try:
        repl()
        return 0
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
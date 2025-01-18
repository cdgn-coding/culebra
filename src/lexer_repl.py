import sys
from typing import NoReturn

from src.lexer import Lexer
from src.token import TokenType


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

    lexer = Lexer()
    tokens = lexer.tokenize(text)

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
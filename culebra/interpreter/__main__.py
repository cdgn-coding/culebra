import sys
from pathlib import Path
from culebra.interpreter.interpreter import Interpreter
from culebra.parser import Parser
from culebra.lexer import Lexer
from culebra.error_reporter import ErrorReporter
def main():
    if len(sys.argv) != 2:
        print("Usage: python -m culebra <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    file_path = Path(filename)

    if not file_path.exists():
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    try:
        # Read the source file
        with open(file_path, 'r') as f:
            source = f.read()

        # Create lexer and generate tokens
        lexer = Lexer()
        tokens = lexer.tokenize(source)

        # Parse tokens into AST
        parser = Parser(tokens)
        ast = parser.parse()

        # Create interpreter and evaluate the AST
        interpreter = Interpreter()

        try:
            result = interpreter.evaluate(ast)
        except Exception as e:
            reporter = ErrorReporter(source)
            reporter.report(interpreter.last_node.token, str(e))
            sys.exit(1)

        if interpreter.last_error:
            interpreter.report_error()
            sys.exit(1)

        # If there's a return value from the program, print it
        if result is not None:
            print(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
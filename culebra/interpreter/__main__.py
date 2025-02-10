import sys
import argparse
from pathlib import Path
from culebra.interpreter.interpreter import Interpreter
from culebra.parser import Parser
from culebra.lexer import Lexer
from culebra.error_reporter import ErrorReporter

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Culebra interpreter')
    parser.add_argument('filename', help='Source file to interpret')
    parser.add_argument('-p', '--parse', action='store_true', help='Pretty print the AST')

    # Parse arguments
    args = parser.parse_args()
    file_path = Path(args.filename)

    if not file_path.exists():
        print(f"Error: File '{args.filename}' not found")
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

        if parser.has_error:
            reporter = ErrorReporter(source)
            reporter.report(parser.last_token, str(parser.last_error))
            sys.exit(1)

        # If parse flag is set, pretty print the AST and exit
        if args.parse:
            print(ast.pretty())
            return

        # Create interpreter and evaluate the AST
        interpreter = Interpreter()

        try:
            interpreter.evaluate(ast)
        except Exception as e:
            reporter = ErrorReporter(source)
            reporter.report(interpreter.last_node.token, str(e))
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
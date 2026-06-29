"""Helper tools for the Developer Specialist."""

import ast

def validate_python_code(code_string: str) -> bool:
    """Run ast.parse on python code to check for syntax correctness.

    Args:
        code_string: Python code as a string.

    Returns:
        True if syntax is valid, False otherwise.
    """
    try:
        ast.parse(code_string)
        return True
    except SyntaxError:
        return False

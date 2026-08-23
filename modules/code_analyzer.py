import ast


def check_python_syntax(code):

    try:
        ast.parse(code)

        return {
            "valid": True,
            "message": "No syntax errors detected.",
            "line": None,
            "offset": None
        }

    except SyntaxError as error:

        return {
            "valid": False,
            "message": error.msg,
            "line": error.lineno,
            "offset": error.offset
        }

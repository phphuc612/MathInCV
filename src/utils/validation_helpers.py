import logging
import math

# Allow math functions
ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}

# Add variable names
ALLOWED_NAMES.update({"x": 0, "y": 0})

def is_evaluable(cmd: str) -> bool:
    """
        Validate if math expression is `eval`uable in python.

        Ref: https://realpython.com/python-eval-function/
    """
    try:
        code = compile(cmd, "<string>", "eval")
        
        # Validate allowed names
        for name in code.co_names:
            if name not in ALLOWED_NAMES:
                raise NameError(f"The use of '{name}' is not allowed")

        return True
    except NameError as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Error parsing command: {e}")
        return False

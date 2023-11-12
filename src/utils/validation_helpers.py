import logging


def is_evaluable(cmd: str) -> bool:
    try:
        compile(cmd, "", "eval")
        return True
    except Exception as e:
        logging.error(f"Error parsing command: {e}")
        return False

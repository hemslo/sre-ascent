import random

from langchain_core.tools import tool


@tool()
def random_number(
    lower: int = 0,
    upper: int = 100,
) -> int:
    """
    Generate a random number between lower (default 0) and upper (default 100)
    """
    return random.randint(lower, upper)

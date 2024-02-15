import random

from langchain_core.tools import tool


@tool()
def random_number() -> str:
    """
    Generate a random number between 0 and 100
    """
    return str(random.randint(0, 100))

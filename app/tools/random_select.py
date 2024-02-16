import random
from collections.abc import Sequence
from typing import Any

from langchain_core.tools import tool


@tool()
def random_select(items: Sequence[Any], k: int) -> list[Any]:
    """
    Randomly select k items from a list
    """
    return random.sample(items, k)

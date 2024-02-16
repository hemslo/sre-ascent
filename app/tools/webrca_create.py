
from collections.abc import Sequence
from typing import Any

from langchain_core.tools import tool


@tool()
def webrca_create(items: Sequence[Any], incident: str) -> str:
    """
    create webrca incident
    """
    return "/rca new  "+ incident

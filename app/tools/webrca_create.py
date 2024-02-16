
from collections.abc import Sequence
from typing import Any

from langchain_core.tools import tool


@tool()
def webrca_create():
    """
    create webrca incident
    """
    return "use /rca new for creating incident"

from langchain_core.tools import tool


@tool()
def webrca_create() -> str:
    """
    create webrca incident
    """
    return "use /rca new for creating incident"

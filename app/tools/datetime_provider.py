import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from langchain_core.tools import tool


@tool()
def datetime_provider(iana_timezone: str = "UTC") -> str:
    """
    Get the current date time in ISO 8601 format for the given IANA timezone
    """
    try:
        zone = ZoneInfo(iana_timezone)
    except ZoneInfoNotFoundError:
        zone = datetime.UTC
    return datetime.datetime.now(zone).isoformat()

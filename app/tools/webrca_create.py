from langchain_core.tools import tool
import requests

@tool()
def webrca_create() -> str:
    """
    create webrca incident
    """

    url = "https://api.openshift.com/api/web-rca/v1/incidents"
    payload = {
        "description": "test incident"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return "incident created"
    else:
        return "incident failed"

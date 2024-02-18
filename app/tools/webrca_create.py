from langchain_core.tools import tool
import requests

@tool()
def webrca_create(description: str) -> str:
    """
    create webrca incident
    """
    url = "https://api.openshift.com/api/web-rca/v1/incidents"
    payload = {
        "description": description
    }
    headers = {"Content-Type": "application/json"}
    failedMessage = "We can’t create it. You can try to use `/rca new {incident-name}` for creating the incident"
    try:    
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return "Created the incident"
        else:
            return failedMessage
    except Exception as e:
        return failedMessage

import requests
from utils.config import JIRA_URL, JIRA_EMAIL, JIRA_TOKEN


class JiraTicketCreator:
    def __init__(self):
        self.base_url = f"{JIRA_URL}/rest/api/3"
        self.auth = (JIRA_EMAIL, JIRA_TOKEN)
        self.headers = {"Content-Type": "application/json"}

    def create_ticket(self, project_key, summary, description, issue_type="Bug"):
        url = f"{self.base_url}/issue"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }
        }

        response = requests.post(
            url, auth=self.auth, headers=self.headers, json=payload
        )
        if response.status_code == 201:
            return response.json()  # contains issue key, etc.
        else:
            print("Failed to create ticket:", response.status_code, response.text)
            return None

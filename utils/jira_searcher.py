import requests
import time
from utils.config import JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, JIRA_PROJECT

class JiraSearcher:
    def __init__(self):
        self.auth = (JIRA_EMAIL, JIRA_TOKEN)
        self.base_url = f"{JIRA_URL}/rest/api/3"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.project_id = JIRA_PROJECT
        self.issueType = "Bug"

    def _parse_adf(self, adf: dict) -> str:
        """Convert Jira ADF (Atlassian Document Format) to plain text."""
        def extract_text(content):
            if isinstance(content, list):
                return " ".join(extract_text(c) for c in content)
            elif isinstance(content, dict):
                if content.get("type") == "text":
                    return content.get("text", "")
                elif "content" in content:
                    return extract_text(content["content"])
            return ""

        blocks = adf.get("content", [])
        lines = []
        for block in blocks:
            if block["type"] in ["paragraph", "listItem"]:
                lines.append(extract_text(block.get("content", [])))
            elif block["type"] == "orderedList":
                for i, item in enumerate(block["content"], 1):
                    lines.append(f"{i}. {extract_text(item.get('content', []))}")
        return "\n".join(lines)

    def search_similar_issues(self, summary: str, max_results: int = 5):
        jql = f'text ~ "{summary}" AND issueType = {self.issueType} ORDER BY created DESC'
        url = f"{self.base_url}/search"
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "key,summary,description"
        }

        # Adding a delay to avoid hitting Jira's rate limits
        time.sleep(1)

        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)

        if response.status_code != 200:
            print("Jira search failed:", response.status_code, response.text)
            return []

        issues = response.json().get("issues", [])
        parsed = []

        for issue in issues:
            fields = issue["fields"]
            adf = fields.get("description", {})
            parsed.append({
                "key": issue["key"],
                "summary": fields.get("summary", ""),
                "description": self._parse_adf(adf) if isinstance(adf, dict) else str(adf)
            })

        return parsed

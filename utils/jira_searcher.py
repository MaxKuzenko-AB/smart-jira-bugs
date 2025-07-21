from dataclasses import fields
import requests
import time
from utils.config import JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, JIRA_PROJECT


class JiraSearcher:
    def __init__(self):
        self.auth = (JIRA_EMAIL, JIRA_TOKEN)
        self.base_url = f"{JIRA_URL}/rest/api/3"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.project_id = JIRA_PROJECT
        self.issueType = "Bug"

    def _parse_adf(self, adf: dict) -> str:
        """Convert Jira ADF (Atlassian Document Format) to readable plain text."""

        def extract_text(content):
            if isinstance(content, list):
                return "".join(extract_text(c) for c in content)
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
                text = extract_text(block.get("content", []))
                if text.strip():
                    lines.append(text.strip())
            elif block["type"] == "orderedList":
                for i, item in enumerate(block.get("content", []), 1):
                    text = extract_text(item.get("content", []))
                    if text.strip():
                        lines.append(f"{i}. {text.strip()}")

        return "\n\n".join(lines)

    def search_similar_issues(self, summary: str, max_results: int = 10):
        jql = (
            f'text ~ "{summary}" AND issueType = {self.issueType} ORDER BY created DESC'
        )
        url = f"{self.base_url}/search"
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "key,summary,description,customfield_10029,customfield_10030",
        }

        # Adding a delay to avoid hitting Jira's rate limits
        time.sleep(1)

        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params
        )

        if response.status_code != 200:
            print("Jira search failed:", response.status_code, response.text)
            return []

        issues = response.json().get("issues", [])
        parsed = []

        for issue in issues:
            fields = issue["fields"]
            summary = fields.get("summary", "")
            description_adf = fields.get("description", {})
            description_text = self._parse_adf(description_adf) if isinstance(description_adf, dict) else str(description_adf)

            # Skip known unwanted patterns in either summary or description
            if "BuildPulse Report" in summary or "Flaky Test" in summary:
                continue
            if "BuildPulse Report" in description_text or "Flaky Test" in description_text:
                continue

            actual_adf = fields.get("customfield_10029")
            expected_adf = fields.get("customfield_10030")

            parsed.append(
                {
                    "key": issue["key"],
                    "summary": fields.get("summary", ""),
                    "description": (
                        self._parse_adf(description_adf)
                        if isinstance(description_adf, dict)
                        else str(description_adf)
                    ),
                    "actual": (
                        self._parse_adf(actual_adf)
                        if isinstance(actual_adf, dict)
                        else str(actual_adf)
                    ),
                    "expected": (
                        self._parse_adf(expected_adf)
                        if isinstance(expected_adf, dict)
                        else str(expected_adf)
                    ),
                }
            )

        return parsed

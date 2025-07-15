import os
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")

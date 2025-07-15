from utils.jira_client import create_ticket

if __name__ == "__main__":
    # Temporary test
    create_ticket(
        "Bug: Button crashes app",
        "Steps:\n1. Go to Home\n2. Click X\nExpected: ...\nActual: ...",
    )

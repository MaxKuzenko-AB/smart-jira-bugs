# from utils.jira_client import create_ticket
from utils.jira_searcher import JiraSearcher


def main():
    searcher = JiraSearcher()
    test_summary = "Risk Acceptance Proposals"  # You can tweak this phrase
    results = searcher.search_similar_issues(test_summary)

    for issue in results:
        key = issue["key"]
        summary = issue.get("summary", "No summary")
        description = issue.get("description", "No description")
        print(f"[{key}] {summary}")
        print(description)
        print("Expected:\n", issue["expected"])
        print("Actual:\n", issue["actual"])
        print("-" * 40)


if __name__ == "__main__":
    main()

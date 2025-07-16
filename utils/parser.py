class SummaryParser:

    def parse_summary(self, summary: str) -> dict:
        """
        Parses the summary of a Jira ticket to extract relevant information.

        Args:
            summary (str): The summary text of the Jira ticket.

        Returns:
            dict: A dictionary containing the parsed information.
        """

        parts = [part.strip() for part in summary.split("|")]

        ticket_data = {}

        if len(parts) >= 3:
            ticket_data["project"] = parts[0]
            ticket_data["feature"] = parts[1]
            ticket_data["description"] = parts[2]

        return ticket_data


class FieldMapper:
    def __init__(self):
        self.issue_type = "Bug"  # Default issue type for Jira tickets

    def map_fields(self, ticket_data: dict) -> dict:
        """
        Maps the parsed ticket data to the fields required by the Jira API.

        Args:
            ticket_data (dict): The parsed ticket data.

        Returns:
            dict: A dictionary containing the mapped fields.
        """

        project = ticket_data.get("project")
        feature = ticket_data.get("feature")
        summary = ticket_data.get("description")

        final_summary = f"[{project} | {feature}]: {summary}"

        team_name = f"PED: {project}"

        return {
            "summary": final_summary,
            #"team": team_name,
            "issue_type": self.issue_type,
        }

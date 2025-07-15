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

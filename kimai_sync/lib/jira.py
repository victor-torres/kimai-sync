import httpx

from kimai_sync.schemas.jira import Issue
from kimai_sync.settings import Settings


class Jira:

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def _auth(self) -> tuple[str, str]:
        return (self._settings.jira_username, self._settings.jira_api_token)

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_issues_by_sprint(self, sprint: str) -> list[Issue]:
        jql_query = f"project = {self._settings.jira_project_id} AND sprint = {sprint!r}"
        payload = {
            "jql": jql_query,
            "maxResults": 100,
            "fields": ["issuetype", "summary"],
        }

        response = httpx.post(
            f"{self._settings.jira_url}/rest/api/3/search",
            headers=self._headers,
            auth=self._auth,
            json=payload,
        )
        response.raise_for_status()

        issues = [
            Issue(
                key=issue["key"],
                type=issue["fields"]["issuetype"]["name"],
                summary=issue["fields"]["summary"],
            )
            for issue in response.json()["issues"]
        ]
        return issues

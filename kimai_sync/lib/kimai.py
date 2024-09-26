import httpx

from kimai_sync.schemas.kimai import Activity
from kimai_sync.settings import Settings

COLORS = {
    "silver": "#c0c0c0",
    "grey": "#808080",
    "maroon": "#800000",
    "green": "#008000",
}

VISIBLE_OPTIONS = {
    True: "1",
    False: "2",
    None: "3",
}


class Kimai:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._settings.kimai_api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_activities(self, visible: bool | None = True, **kwargs) -> list[Activity]:
        params: dict[str, str | int] = {
            "project": self._settings.kimai_project,
            "visible": VISIBLE_OPTIONS[visible],
        }

        response = httpx.get(
            f"{self._settings.kimai_url}/api/activities",
            headers=self._headers,
            params=params,
        )
        response.raise_for_status()

        activities = [
            Activity(
                id=activity["id"],
                project=activity["project"],
                name=activity["name"],
                comment=activity["comment"],
                billable=activity["billable"],
                visible=activity["visible"],
                color=activity["color"],
                number=activity["number"],
            )
            for activity in response.json()
            if all((activity[filter[0]] == filter[1] for filter in kwargs.items()))
        ]

        return activities

    def archive_all(self):
        activities = self.get_activities(visible=True)
        for activity in activities:
            activity.visible = False
            self.update_activity(activity)

        return activities

    def create_activity(self, activity: Activity) -> Activity:
        payload = {
            "name": activity.name,
            "comment": activity.comment,
            "project": activity.project,
            "number": activity.number,
            "billable": activity.billable,
            "visible": activity.visible,
            "color": activity.color,
        }

        response = httpx.post(
            f"{self._settings.kimai_url}/api/activities",
            headers=self._headers,
            json=payload,
        )

        # Check if activity already exists by number (when this field is available)
        if response.status_code == 400 and activity.number is not None:
            data = response.json()
            number_errors = data["errors"]["children"]["number"].get("errors", [])
            if f"The number {activity.number} is already used." in number_errors:
                return self.update_activity(activity=activity)

        response.raise_for_status()

        return activity

    def update_activity(self, activity: Activity) -> Activity:
        if activity.id is None:
            if activity.number is None:
                raise ValueError(f"Activities must have an id or number defined to be updated.")

            activities = self.get_activities(number=activity.number, visible=None)
            assert activities[0].number == activity.number
            activity.id = activities[0].id

        payload = {
            "name": activity.name,
            "number": activity.number,
            "comment": activity.comment,
            "project": activity.project,
            "billable": activity.billable,
            "visible": activity.visible,
            "color": activity.color,
        }

        response = httpx.patch(
            f"{self._settings.kimai_url}/api/activities/{activity.id}",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()

        return activity

from pydantic import BaseModel

from kimai_sync.lib import kimai
from kimai_sync.schemas.kimai import Activity
from kimai_sync.settings import Settings

settings = Settings()


TYPE_EMOJIS = {
    "bug": "🐛",
    "story": "📖",
    "task": "🛠️",
    "subtask": "🔧",
}

TYPE_COLORS = {
    "bug": "maroon",
    "story": "green",
    "task": "grey",
    "subtask": "silver",
}


class Issue(BaseModel):
    key: str
    type: str
    summary: str

    @property
    def type_emoji(self) -> str:
        return TYPE_EMOJIS.get(self.type.lower(), "❓")

    @property
    def billable(self) -> bool:
        return self.type.lower() == "story"

    @property
    def color(self) -> str | None:
        jira_color = TYPE_COLORS.get(self.type.lower())
        kimai_color = jira_color and kimai.COLORS.get(jira_color)
        return kimai_color

    def to_activity(self) -> Activity:
        return Activity(
            name=f"{self.key}: {self.summary}",
            comment=f"Jira issue: {settings.jira_url}/browse/{self.key}",
            project=settings.kimai_project,
            number=self.key,
            billable=self.billable,
            visible=True,
            color=self.color,
        )

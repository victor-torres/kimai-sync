from pydantic import BaseModel


class Activity(BaseModel):
    id: str | int | None = None
    name: str
    comment: str | None
    project: int
    number: str | None
    billable: bool
    visible: bool
    color: str | None

    @property
    def billable_emoji(self) -> str:
        return "💰" if self.billable else "🕐"

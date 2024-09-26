import typer

from kimai_sync.lib.jira import Jira
from kimai_sync.lib.kimai import Kimai
from kimai_sync.settings import Settings

app = typer.Typer()
settings = Settings()


@app.command()
def get_jira_issues_by_sprint(sprint: str):
    jira = Jira(settings=settings)
    issues = jira.get_issues_by_sprint(sprint)
    for issue in issues:
        print(f"{issue.type_emoji} {issue.key}: {issue.summary}")


@app.command()
def get_kimai_activities(**kwargs):
    kimai = Kimai(settings=settings)
    activities = kimai.get_activities(**kwargs)
    for activity in activities:
        print(f"{activity.billable_emoji} {activity.name}")


@app.command()
def sync_jira_sprint_issues_to_kimai(sprint: str):
    jira = Jira(settings=settings)
    kimai = Kimai(settings=settings)

    issues = jira.get_issues_by_sprint(sprint)
    for issue in issues:
        activity = issue.to_activity()
        kimai.create_activity(activity)
        print(f"{activity.billable_emoji} {activity.name}")


@app.command()
def archive_all_kimai_activities():
    kimai = Kimai(settings=settings)
    activities = kimai.archive_all()
    for activity in activities:
        print(f"{activity.billable_emoji} {activity.name}")


if __name__ == "__main__":
    app()

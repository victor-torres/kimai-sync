from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jira_api_token: str
    jira_username: str
    jira_url: str
    jira_project_id: int

    kimai_api_token: str
    kimai_url: str
    kimai_project: int

    class Config:
        env_file = ".env"

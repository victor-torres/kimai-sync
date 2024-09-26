# Kimai Sync

This is a command-line project to help syncing Jira issues to Kimai, a time-tracking platform.


## Installing dependencies

We're using Python Poetry. You can install dependencies like this:

```
poetry install
```

## Running commands

Create a new `.env` file from `.env.sample`, and run commands like this:

```
poetry run python kimai_sync/main.py sync-jira-sprint-issues-to-kimai "Dev week 2024.39"
```

You can discover more commands with the `--help` flag:

```
poetry run python kimai_sync/main.py --help
```

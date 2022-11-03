import datetime
import os
import random

from celery import Task
from dotenv import load_dotenv
from jira import JIRA
from pymongo import MongoClient
from pymongo.collection import Collection

from mq.constants import Priority

from .master import app
from .models.models import JiraIssue


# Avoids creating a MongoClient() every time a task is run
class DatabaseTask(Task):
    client: MongoClient = MongoClient()
    _collection: Collection[JiraIssue] = client.takehome.jira

    @property
    def collection(self) -> Collection[JiraIssue]:
        return self._collection


class JiraTask(Task):
    def __init__(self):
        load_dotenv()

        token = os.getenv("JIRA_API_TOKEN")
        user = os.getenv("JIRA_USERNAME")
        server = os.getenv("JIRA_SERVER")

        if not token or not user or not server:
            raise ValueError(
                f"Error: Jira Server, Token and/or Email are missing in your \
                environment variables. Values found: \
                (token: {token}, user: {user} server: {server})"
            )

        self._jira = JIRA(
            server=server,
            basic_auth=(user, token),
        )

    @property
    def jira(self) -> JIRA:
        return self._jira


@app.task(base=JiraTask)
def create_jira_issue(project_key: str) -> JiraIssue:
    """create_jira_issue creates a jira issue with a random severity
     in project project_key

    Args:
        project_key (str): the key of the project to add this task to

    Returns:
        JiraIssue: the issue that was created
    """
    num: int = random.randrange(1, len(Priority) + 1)
    priority: str = Priority(num).name
    issue = JiraIssue(
        {
            "project": {"key": project_key},
            "summary": "A sample issue",
            "priority": {"name": priority},
            "issuetype": {"name": "Task"},
            "description": "Issue Description",
        }
    )
    create_jira_issue.jira.create_issue(fields=issue)
    return issue


@app.task(base=DatabaseTask)
def insert_jira_issue_into_db(issue: JiraIssue) -> None:
    """insert_jira_issue inserts issue into the jira collection

    Args:
        issue (JiraIssue): the issue to be inserted

    """
    i = dict(issue)
    i["time"] = datetime.datetime.now()
    insert_jira_issue_into_db.collection.insert_one(i)
    print(f"Inserted Jira Issue into db {i}")

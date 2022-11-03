from typing import Any, Dict, TypedDict

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult


# Defines a Jira Issue object in the database
class JiraIssue(TypedDict):
    project: Dict[str, Any]
    summary: str
    priority: str
    issuetype: Dict[str, Any]
    description: str


client: MongoClient = MongoClient()
collection: Collection[JiraIssue] = client.takehome.jira


def insert_jira_issue(issue: JiraIssue) -> InsertOneResult:
    """insert_jira_issue inserts issue into the jira collection

    Args:
        issue (JiraIssue): the issue to be inserted

    Returns:
        InsertOneResult: mongo insert result object
    """
    return collection.insert_one(issue)

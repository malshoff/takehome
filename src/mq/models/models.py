from typing import Any, Dict, TypedDict

from pymongo import MongoClient
from pymongo.collection import Collection


# Defines a Jira Issue object in the database
class JiraIssue(TypedDict):
    project: Dict[str, Any]
    summary: str
    priority: str
    issuetype: Dict[str, Any]
    description: str


client: MongoClient = MongoClient()
collection: Collection[JiraIssue] = client.takehome.jira

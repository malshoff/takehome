from unittest.mock import patch

from mq.models.models import JiraIssue
from mq.tasks import JiraTask


@patch("jira.JIRA.create_issue")
def test_jira_creation(jira_object):
    issue = JiraIssue(
        {
            "project": {"key": "TEST"},
            "summary": "A sample issue",
            "priority": {"name": "Medium"},
            "issuetype": {"name": "Task"},
            "description": "Issue Description",
        }
    )
    task = JiraTask()
    task.jira.create_issue(issue)
    jira_object.assert_called_with(issue)

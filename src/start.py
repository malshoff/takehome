import datetime
import random

import pandas as pd
import plotly.express as px
import typer
from pymongo import MongoClient
from pymongo.cursor import Cursor
from mq.tasks import create_jira_issue, insert_jira_issue_into_db

app = typer.Typer()


def get_posts():
    """get_posts returns timestamps for each object in the dictionary.
    The query could be slightly amended to only return posts from the most
    recent hour at the time the function is called, but for the assignment
    there's no guarantee that the script is running every hour.

    Returns:
        Cursor: Cursor object containing the matched documents
    """
    client: MongoClient = MongoClient()
    collection = client.takehome.jira
    return collection.find(
        {
            "$or": [
                {"priority": {"name": "High"}},
                {"priority": {"name": "Highest"}},
            ]
        },
        {"time": True, "_id": False},
    )


@app.command()
def graph():
    """Plot the latest hour of created jira issues"""
    posts = list(get_posts())
    df = pd.DataFrame(posts)
    # add count column
    df["count"] = 1
    start_time, end_time = get_start_and_end_times(posts)
    # print((start_time, end_time))
    fig = px.histogram(
        df,
        x="time",
        y="count",
        histfunc="count",
        title="Jira Issues Created In The Past Hour",
    )
    fig.update_traces(xbins_size=60000)
    fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="60000")
    fig.update_layout(
        bargap=0.1,
        xaxis_range=[start_time, end_time],
    )
    fig.show()


def get_start_and_end_times(times: list[Cursor]):
    """Returns the correct x axis boundaries given posts

    Args:
        posts (list): list of timestamps

    Returns:
        _type_: _description_
    """
    # sort list in order to find the start and end times for the histogram
    times.sort(key=lambda x: x["time"])
    first_time = times[0]["time"]
    last_time = times[-1]["time"]

    # if both times fit within the same hour,the end hour will be that hour+1.
    # otherwise, we want the graph to go from first_time to last_time, so that
    # we will still have exactly 60 x-values, as required in the assignment
    # details.

    if first_time.hour == last_time.hour:
        x_axis_begin = first_time.replace(minute=0, second=0, microsecond=0)
        x_axis_end = last_time.replace(
            minute=0, second=0, microsecond=0
        ) + datetime.timedelta(hours=1)
        return (x_axis_begin, x_axis_end)
    else:
        x_axis_begin = first_time.replace(
            minute=last_time.minute, second=0, microsecond=0
        )
        x_axis_end = last_time
        return (x_axis_begin, x_axis_end)


@app.command()
def generate_tickets(amount: int):
    """Enqueue (amount) jira tickets to be created. Celery and RabbitMQ must be
    running!


    Args:
        amount (int): number of tickets to generate
    """

    for i in range(amount):
        create_jira_issue.apply_async(
            ("TEST",),
            link=insert_jira_issue_into_db.s(),
            countdown=random.randrange(1, 60 * 60),
        )


@app.command()
def generate_instantly():
    """Instantly enqueue a Jira Task"""

    create_jira_issue.apply_async(
        ("TEST",), link=insert_jira_issue_into_db.s()
    )


if __name__ == "__main__":
    app()

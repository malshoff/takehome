import os
import sys

from celery import Celery

"""sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mq"))
)"""

app = Celery(
    "mq",
    broker="amqp://localhost",
    backend="rpc://",
    include=["mq.tasks"],
)

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()

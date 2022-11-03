from celery import Celery

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

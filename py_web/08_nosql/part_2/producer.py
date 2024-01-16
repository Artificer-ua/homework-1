import logging
from random import choice

import pika
from faker import Faker
from mongoengine import connect

from connect import credentials, mongo_connect_test, r_domain, r_port, uri
from models import User

USERS_COUNT = 10
NEWSLETTER_METHOD = ["email", "sms"]
# NEWSLETTER_METHOD = ["email", "sms", "both"]

connect(host=uri)

fake = Faker(locale="uk_UA")

logging.getLogger("pika").setLevel(
    logging.WARNING
)  # reduce log level for pika because of...

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=r_domain, port=r_port, credentials=credentials)
)
channel = connection.channel()


for method in NEWSLETTER_METHOD:
    logging.info(f"RabbitMQ. Create {method} queue.")
    channel.queue_declare(queue=method)


def add_users():
    for _ in range(0, USERS_COUNT):
        new_item = User(
            fullname=fake.name(),
            email=fake.email(),
            method=choice(NEWSLETTER_METHOD),
            phone=fake.phone_number(),
            done=False,
        )
        new_item.save()


def create_tasks():
    users = User.objects()
    # for id_task in users.scalar("id"):
    #     print(str(id_task))
    for user in users:
        task = str(user.to_mongo().to_dict().get("_id"))
        task_queue = user.to_mongo().to_dict().get("method")
        logging.info(f"Creating newsletter task '{task_queue}' for user id: {task}")
        # logging.info(
        #     f"Creating newsletter task {('(email + sms)' if task_queue == 'both' else '('+ task_queue + ')')}"
        #     f" for user id: {task}"
        # )
        # create RabbitMQ task
        channel.basic_publish(exchange="", routing_key=task_queue, body=task.encode())
    connection.close()


if __name__ == "__main__":
    # if we want to test connection to MONGO service
    mongo_connect_test()
    # add_users()
    create_tasks()

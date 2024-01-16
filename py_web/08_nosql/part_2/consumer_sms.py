import logging
import sys

import pika
from mongoengine import connect

from connect import credentials, r_domain, r_port, uri
from models import User

connect(host=uri)

logging.getLogger("pika").setLevel(logging.WARNING)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=r_domain, port=r_port, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="sms")


def send_sms(contact_id: str):
    contact = User.objects.get(id=contact_id)
    logging.info(
        f"Sending sms to contact: {contact.to_mongo().to_dict().get('fullname')}, "
        f"phone: {contact.to_mongo().to_dict().get('phone')}"
    )
    contact.done = True  # set done flag
    contact.save()


def main():
    def callback(ch, method, properties, body):
        logging.info(f"Task received: {body.decode()}")
        send_sms(contact_id=body.decode())

    channel.basic_consume(queue="sms", on_message_callback=callback, auto_ack=True)

    print("Waiting for tasks. To exit press CTRL+C")
    channel.start_consuming()


try:
    main()
except KeyboardInterrupt:
    print("Interrupted")
    sys.exit(0)

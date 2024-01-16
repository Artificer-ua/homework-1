import configparser
import logging
from pathlib import Path

import pika
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

CONFIG_FILE = "config.ini"
file_config = Path(__file__).parent.joinpath(CONFIG_FILE)
config = configparser.ConfigParser()
config.read(file_config)

m_username = config.get("MONGO", "MONGO_USER")
m_password = config.get("MONGO", "MONGO_PASS")
db_name = config.get("MONGO", "DB_NAME")
m_domain = config.get("MONGO", "DOMAIN")

r_username = config.get("RABBIT", "RABBIT_USER")
r_password = config.get("RABBIT", "RABBIT_PASS")
r_port = config.get("RABBIT", "RABBIT_PORT")
r_domain = config.get("RABBIT", "RABBIT_DOMAIN")

# for RABBITMQ
credentials = pika.PlainCredentials(r_username, r_password)

# for MONGO DB
uri = f"mongodb+srv://{m_username}:{m_password}@{m_domain}/{db_name}?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# db = client[db_name]

# logging rules
logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
    handlers=[
        # logging.FileHandler("file.log"),
        logging.StreamHandler()
    ],
)


def mongo_connect_test() -> None:
    # Send a ping to confirm a successful connection to MONGO host
    try:
        client.admin.command("ping")
        logging.info("Pinged your deployment. You successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Connection database error {e}")


if __name__ == "__main__":
    mongo_connect_test()

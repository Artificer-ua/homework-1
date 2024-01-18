import configparser
import logging
from pathlib import Path

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

CONFIG_FILE = "config.ini"
file_config = Path(__file__).parent.joinpath(CONFIG_FILE)
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("MONGO", "MONGO_USER")
password = config.get("MONGO", "MONGO_PASS")
db_name = config.get("MONGO", "DB_NAME")
domain = config.get("MONGO", "DOMAIN")

uri = f"mongodb+srv://{username}:{password}@{domain}/{db_name}?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# db = client[db_name]

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
    handlers=[
        # logging.FileHandler("file.log"),
        logging.StreamHandler()
    ],
)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    logging.info("Pinged your deployment. You successfully connected to MongoDB")
except Exception as e:
    logging.error(f"Connection database error {e}")

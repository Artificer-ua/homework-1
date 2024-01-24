from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGO_USER = "user_goit_web17"
MONGO_PASS = "E341L50psvipiXeQ"
DB_NAME = "pyweb17_hw9"
DOMAIN = "cluster0.aryr0zq.mongodb.net"

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{DOMAIN}"
#       f"/{DB_NAME}?retryWrites=true&w=majority")


def get_mongodb():
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client.pyweb17_hw9
    return db

from connect import uri
from mongoengine import connect
from pathlib import Path
from models import Author, Quote
import json
import logging

connect(host=uri)

BASE_PATH = Path(__file__).parent


def seed_authors(filename: str):
    if BASE_PATH.joinpath(filename).exists():
        logging.info(f"Reading file {filename} from {BASE_PATH}")
        with open(BASE_PATH.joinpath(filename), "r", encoding="utf-8") as f:
            json_data = json.load(f)

        for item in json_data:
            new_item = Author(
                fullname=item.get("fullname"),
                born_date=item.get("born_date"),
                born_location=item.get("born_location"),
                description=item.get("description"),
            )
            new_item.save()
    else:
        logging.error(f"File: {filename} is not exist in: {BASE_PATH}")


def seed_quotes(filename: str):
    if BASE_PATH.joinpath(filename).exists():
        logging.info(f"Reading file {filename} from {BASE_PATH}")
        with open(BASE_PATH.joinpath(filename), "r", encoding="utf-8") as f:
            json_data = json.load(f)

        for item in json_data:
            new_item = Quote(
                tags=item.get("tags"),
                author=Author.objects(fullname=item.get("author")).first(),
                text=item.get("quote")
            )
            new_item.save()
    else:
        logging.error(f"File: {filename} is not exist in: {BASE_PATH}")

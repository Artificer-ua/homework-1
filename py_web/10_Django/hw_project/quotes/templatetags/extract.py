from django import template
from bson.objectid import ObjectId

from ..utils import get_mongodb

register = template.Library()

def get_authors(id_):
    db = get_mongodb()
    # author = Author.objects(fullname=fullname).first().to_mongo().to_dict().get("_id")
    author = db.author.find_one({"_id": ObjectId(id_)})
    return author["fullname"]

register.filter("author", get_authors)

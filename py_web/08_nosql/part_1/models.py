from mongoengine import (CASCADE, Document, ListField, ReferenceField,
                         StringField)


class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = StringField(max_length=20, required=True)
    born_location = StringField(max_length=50, required=True)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField(required=True))
    # ObjectId from another doc
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    # author = StringField(required=True)
    text = StringField(required=True)

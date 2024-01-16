from mongoengine import BooleanField, Document, StringField


class User(Document):
    fullname = StringField(max_length=50, required=True)
    email = StringField(max_length=50, required=True)
    method = StringField(max_length=5, required=True, default=None)
    phone = StringField(max_length=20, required=False)
    done = BooleanField(default=False)

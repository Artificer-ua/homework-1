from django.forms import CharField, Form, Textarea, TextInput


class Author(Form):
    fullname = CharField(label="Author name", max_length=50, widget=TextInput())
    born_date = CharField(label="Date of born", max_length=20, widget=TextInput())
    born_location = CharField(label="Born location", max_length=200, widget=TextInput())
    description = CharField(label="About", widget=Textarea())


class AutorQuote(Form):
    tags = CharField(
        label="Tags (input with coma separator)", max_length=100, widget=TextInput()
    )
    author = CharField(label="Author name", max_length=50, widget=TextInput())
    text = CharField(label="Quote", widget=Textarea())

# from django.db.models import CharField, Model, TextField

# Create your models here.


# class Author(Model):
#     fullname = CharField(max_length=50, null=False)
#     born_date = CharField(max_length=20)
#     born_location = CharField(max_length=200)
#     description = TextField()
#
#     def __str__(self):
#         return f"{self.fullname}"
#
#
# class Quote(Model):
#     tags = CharField(max_length=50)
#     author = CharField(max_length=50, null=False)
#     text = TextField( null=False)
#
#     def __str__(self):
#         return f"{self.text}"

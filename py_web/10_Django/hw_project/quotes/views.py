from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import Author, AutorQuote
from .utils import get_mongodb

# from bson import ObjectId


def main(request, page=1, per_page=10):
    db = get_mongodb()
    quotes = db.quote.find()  # get all quotes
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={"title": "Homework 10", "quotes": quotes_on_page},
    )


def show_author_info(request, author_id):
    db = get_mongodb()
    # author = db.author.find_one({"_id": ObjectId(author_id)})
    author = db.author.find_one({"fullname": author_id})
    # return render(request, "quotes/author.html", context={"title": author.get("fullname"),
    #                                                       "author": author.get("fullname"),
    #                                                       "born_date": author.get("born_date"),
    #                                                       "born_location": author.get("born_date"),
    #                                                       "description": author.get("description")})
    return render(
        request, "quotes/author.html", context={"title": author_id, "author": author}
    )


@login_required
def add_author(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = Author(request.POST)
        # check whether it's valid:
        if form.is_valid():
            db = get_mongodb()
            db_table = db.author
            db_table.insert_one(
                {
                    "fullname": form.cleaned_data["fullname"],
                    "born_date": form.cleaned_data["born_date"],
                    "born_location": form.cleaned_data["born_location"],
                    "description": form.cleaned_data["description"],
                }
            )

            #  return blank. no time to do another logic.
            form = Author()
            return render(
                request,
                "quotes/add_author.html",
                context={"title": "add author", "form": form},
            )

    # if a GET we'll create a blank form
    else:
        form = Author()

    return render(
        request, "quotes/add_author.html", context={"title": "add author", "form": form}
    )


@login_required
def add_quote(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = AutorQuote(request.POST)
        # check whether it's valid:
        if form.is_valid():
            db = get_mongodb()
            db_table = db.quote
            # add only existing author, without mistakes
            author_id = db.author.find_one(
                {"fullname": form.cleaned_data["author"]}
            ).get("_id")
            clear_tag_list = [t.strip() for t in form.cleaned_data["tags"].split(",")]

            print(type(author_id), author_id)
            print(clear_tag_list)

            result = db_table.insert_one(
                {
                    "tags": clear_tag_list,
                    "author": author_id,
                    "text": form.cleaned_data["text"],
                }
            )
            print(result.inserted_id)

            #  return blank. no time to do another logic.
            form = AutorQuote()
            return render(
                request,
                "quotes/add_quote.html",
                context={"title": "add quote", "form": form},
            )

    # if a GET we'll create a blank form
    else:
        form = AutorQuote()
    return render(
        request, "quotes/add_quote.html", context={"title": "add quote", "form": form}
    )

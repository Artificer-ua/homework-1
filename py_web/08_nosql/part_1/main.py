from models import Author, Quote
from seeds import seed_authors, seed_quotes

AUTHORS = "authors.json"
QUOTES = "quotes.json"


def search_quote_by_author(fullname: str) -> list:
    author_object_id = (
        Author.objects(fullname=fullname).first().to_mongo().to_dict().get("_id")
    )
    # print(type(Quote.objects(author=author_object_id).all()))
    # result = []
    # quotes_found = Quote.objects(author=author_object_id).all()
    # print(
    #     f"Quotes of author {Author.objects(fullname=fullname).first().to_mongo().get("fullname")} "
    #     f"where found {quotes_found.count()}."
    # )
    # for quote in quotes_found:
    #     print("Quote: ", quote.to_mongo().to_dict().get("text").encode("utf-8"))
    #     print("Tags: ", [q.encode("utf-8") for q in quote.to_mongo().to_dict().get("tags")])
    # for quote in quotes_found:
    #     result.append(quote.to_mongo().to_dict().get("text").encode("utf-8"))
    # return result
    return Quote.objects(author=author_object_id).all()


def search_quote_by_tag(tag: str) -> list:
    # result = []
    # for text in Quote.objects(tags=tag).all():
    #     result.append(text.text)
    # return result
    return Quote.objects(tags=tag).all()


def search_quote_by_tags(tags: list) -> list:
    # result = []
    # for text in Quote.objects(tags__in=tags).all():
    #     result.append(text.text)
    # return result
    return Quote.objects(tags__in=tags).all()


if __name__ == "__main__":
    # to fill tables with json data from files
    # seed_authors(AUTHORS)
    # seed_quotes(QUOTES)

    print("")
    while True:
        command = input("Enter command: ")

        if command.startswith("name:"):
            search_author = command.split(":")[1].strip()
            print(f"Search by author: {search_author}")
            result = search_quote_by_author(search_author)
        elif command.startswith("tag:"):
            tag_search = command.split(":")[1].strip()
            print(f"Search by tag: {tag_search}")
            result = search_quote_by_tag(tag_search)
        elif command.startswith("tags:"):
            tags_search = command.split(":")[1].split(",")  # list of tags
            print(f"Search by tags list: {tags_search}")
            result = search_quote_by_tags(tags_search)
        elif command == "exit":
            break
        else:
            print("Unrecognized command. Try again.")
            continue

        # display results
        for quote in result:
            print(
                f"Author: {quote.author.fullname.encode('utf-8')}\n"
                f"Tags: {[tag.encode('utf-8') for tag in quote.tags]}\n"
                f"Quote:  {quote.text.encode('utf-8')}"
            )

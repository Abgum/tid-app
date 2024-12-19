from flask_injector import inject
from data_access.db_access import get_books, insert_into_books
from pathlib import Path
from random import Random


@inject
def get_all_books():
    books = []
    for book in get_books():
        books.append(
            {
                "book_id": book[0],
                "title": book[1],
                "cover_path": "static/covers/" + book[2],
            }
        )
    return books, 200


@inject
def insert_book(cover_image, book_title):
    if not cover_image:
        return "No file uploaded", 400

    print(cover_image)
    if cover_image.filename.split(".")[-1].lower() not in [
        "jpeg",
        "jpg",
        "png",
        "webp",
    ]:
        return "Image extension not accepted", 400

    file_name = (
        cover_image.filename.split(".")[0]
        + "_"
        + str(Random().randint(1000, 9999))
        + "."
        + cover_image.filename.split(".")[-1]
    )

    try:
        file_path = Path(".", "static", "covers", file_name)
        # Create directories if not exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "xb") as fp:
            cover_image.save(fp)
    except FileExistsError:
        return (
            "Cover with the same name exists. Try with a different cover image name.",
            400,
        )
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    return insert_into_books(book_title, file_name), 200

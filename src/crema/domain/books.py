from src.crema.data_models.models import Book, Cook


def create_book(book_title: str):
    """Creates a book in the database."""
    book = Book.objects.create(title=book_title)

    return book

def create_cook(cook_name: str):
    """Creates a cook in the db."""
    cook = Cook.objects.create(name="new cook")

    return cook

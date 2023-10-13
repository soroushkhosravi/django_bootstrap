from src.crema.data_models.models import Book

def test_can_be_instantiated():
    """Tests book model instantiation."""
    book = Book(title="first book")

    assert isinstance(book, Book)

    assert book.title == "first book"
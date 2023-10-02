"""The definition of the entity list class for returning models by cursor based pagination."""
from collections import UserList

class EntityList(UserList):
    """A customised list class."""
    def __init__(self, iterable, last_cursor: str):
        """Instantiates the object."""
        super().__init__(iterable)
        self.last_cursor = last_cursor
        self.has_next = iterable.has_next
        self.has_previous = iterable.has_previous
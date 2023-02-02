import sys
from abc import abstractmethod
from datetime import datetime
from typing import Iterable, Tuple, Any

from persistence_layer.bookmark_db import BookmarkDatabase

persistence = BookmarkDatabase()


class Command:
    @abstractmethod
    def execute(self, *args, **kwargs) -> Tuple[bool, Any]:
        ...


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        persistence.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self) -> Iterable:
        data = persistence.select(self.order_by)
        return True, data


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        persistence.delete(data)
        return True, None


class EditBookmarkCommand(Command): # experimental
    def execute(self, data):
        persistence.edit(data['id'], data['update'])
        return True, None


class QuitCommand(Command):
    def execute(self):
        sys.exit()

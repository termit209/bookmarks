import sys
from abc import abstractmethod
from datetime import datetime
from typing import Iterable

from database import DatabaseManager

db = DatabaseManager('bookmarks.db')


class Command:
    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class CreateBookmarksTableCommand(Command):
    def execute(self):
        db.create_table('bookmarks', {'id': 'integer primary key autoincrement',
                                      'title': 'text not null',
                                      'url': 'text not null',
                                      'notes': 'text',
                                      'date_added': 'text not null', })


class AddBookmarkCommand(Command):
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self) -> Iterable:
        return db.select('bookmarks', sort_column=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        db.delete('bookmarks', data)
        return 'Bookmark deleted!'


class QuitCommand(Command):
    def execute(self):
        sys.exit()

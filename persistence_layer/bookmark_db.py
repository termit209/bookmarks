from typing import Any, Dict, Optional

from persistence_layer.base import PersistenceLayer
from persistence_layer.database.db_manager import DatabaseManager

COLUMNS = {"id": "integer primary key autoincrement",
           "title": "text not null",
           "url": "text not null'",
           "notes": "text",
           "date_added": "text not null"}


class BookmarkDatabase(PersistenceLayer):
    def __int__(self, table_name: str):
        self.table_name = table_name
        self.db = DatabaseManager("bookmarks.db")
        self.db.create_table(table_name, COLUMNS)

    def add(self, data: Dict[str, Any]):
        self.db.add(self.table_name, data)

    def select(self, order_by: Optional[str] = None):
        return self.db.select(self.table_name, order_by=order_by).fetchall()

    def delete(self, bookmark_id: int):
        self.db.delete(self.table_name, {'id': bookmark_id})

    def edit(self, bookmark_id, bookmark_data):
        self.db.update(self.table_name, {'id': bookmark_id}, bookmark_data)

if __name__ == '__main__':
    db = BookmarkDatabase('sdd')

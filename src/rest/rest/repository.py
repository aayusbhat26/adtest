import os
import logging
from typing import Dict, List, Protocol
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class TodoStore(Protocol):
    def get_all(self) -> List[Dict[str, str]]:
        ...

    def create(self, title: str) -> Dict[str, str]:
        ...


class TodoRepository:
    def __init__(self, db=None):
        if db is None:
            mongo_uri = "mongodb://{}:{}".format(
                os.environ.get("MONGO_HOST", "mongo"),
                os.environ.get("MONGO_PORT", "27017"),
            )
            db = MongoClient(mongo_uri)["test_db"]

        self.db = db

    def get_all(self) -> List[Dict[str, str]]:
        todos = []
        try:
            for todo in self.db.todos.find():
                todos.append({
                    "_id": str(todo["_id"]),
                    "title": todo["title"]
                })
        except Exception:
            logger.exception("Database error while fetching todos")
            raise RuntimeError("Failed to fetch todos from database")

        return todos

    def create(self, title: str) -> Dict[str, str]:
        try:
            todo = {"title": title}
            result = self.db.todos.insert_one(todo)
            return {
                "_id": str(result.inserted_id),
                "title": title
            }
        except Exception:
            logger.exception("Database error while creating todo")
            raise RuntimeError("Failed to create todo in database")

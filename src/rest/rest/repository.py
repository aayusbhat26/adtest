import os
from abc import ABC, abstractmethod
from pymongo import MongoClient

class MongoDAO(ABC):
    def __init__(self, collection_name, client=None):
        if not collection_name:
            raise ValueError("collection_name is required")

        host = os.environ.get("MONGO_HOST", "mongo")
        port = os.environ.get("MONGO_PORT", "27017")

        self.client = client or MongoClient(f"mongodb://{host}:{port}")
        self.db = self.client[os.environ.get("MONGO_DB_NAME", "test_db")]
        self.collection = self.db[collection_name]

    @property
    @abstractmethod
    def collection_name(self):
        pass

    def get_all(self):
        try:
            return [self._serialize_document(doc) for doc in self.collection.find()]
        except Exception as e:
            print(f"Error fetching docs: {e}")
            return []

    def create(self, document):
        try:
            result = self.collection.insert_one(document)
            doc = self.collection.find_one({"_id": result.inserted_id})
            return self._serialize_document(doc)
        except Exception as e:
            print(f"Error creating doc: {e}")
            raise

    def update(self, query, changes):
        try:
            self.collection.update_one(query, {"$set": changes})
            doc = self.collection.find_one(query)
            return self._serialize_document(doc) if doc else None
        except Exception as e:
            print(f"Error updating doc: {e}")
            raise

    def _serialize_document(self, document):
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document


class TodoDAO(MongoDAO):
    @property
    def collection_name(self):
        return "todos"

    def __init__(self, client=None):
        super().__init__(self.collection_name, client)

    def create(self, title):
        if not title or not str(title).strip():
            raise ValueError("title is required")

        return super().create({"title": str(title).strip()})

    def update(self, query, changes):
        if not changes:
            raise ValueError("changes cannot be empty")

        return super().update(query, changes)


TodoRepository = TodoDAO
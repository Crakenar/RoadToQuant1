from typing import Any, Mapping
from pymongo.synchronous.database import Database
import pymongo

DEFAULT_TABLE = "transactions"
DEFAULT_DATABASE_NAME = "mydatabase"

def init_db() -> Database[Mapping[str, Any]] | None:
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client[DEFAULT_DATABASE_NAME]
        print("Successfully connected to database")
        return mydb
    except Exception as e:
        print("An error occurred while initiating database:", e)
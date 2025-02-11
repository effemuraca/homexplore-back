from os import environ
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Dict, List, Union, Any
from config.config import settings

MONGO_URL = environ.get('MONGO_URL')


if MONGO_URL is None or MONGO_URL == '':
    MONGO_URL = settings.mongo_url

if MONGO_URL is None:
    raise Exception('MONGO_URL environment variable not set')

DEFAULT_MONGO_DB = MONGO_URL.split('/')[-1]

if MONGO_URL is None:
    raise Exception('MONGO_URL environment variable not set')

client = MongoClient(MONGO_URL)

def get_mongo_client():
    """
    Returns:
        MongoClient: The MongoDB client instance.
    """
    return client

def get_default_mongo_db():
    """
    Returns:
        Database: The default MongoDB database specified by environment variables.
    """
    return client[DEFAULT_MONGO_DB]

def convert_object_id(result: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """
    Converts the _id field(s) of a mongo result to string(s).

    Args:
        result (dict or list): The result(s) of a MongoDB query.

    Returns:
        dict or list: The same data structure with '_id' turned into a string.
    """
    if isinstance(result, list):
        for res in result:
            res["_id"] = str(res["_id"])
    else:
        result["_id"] = str(result["_id"])
    return result
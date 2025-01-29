# purpose:
#     this file creates an instance of the mongo client that can be used to interact with the mongo database.

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
    This function returns the mongo client instance.
    """
    return client

def get_default_mongo_db():
    """
    This function returns the database instance, which is the default database specified in the environment variables.
    """
    return client[DEFAULT_MONGO_DB]
    
def convert_object_id(result: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """
    This function converts the _id field of a mongo result to a string.
    
    @param result: the result of a mongo query, can be a single document or a list of documents.
    """
    if isinstance(result, list):
        for res in result:
            res["_id"] = str(res["_id"])
    else:
        result["_id"] = str(result["_id"])
    return result
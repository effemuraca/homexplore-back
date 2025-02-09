from os import environ
from typing import Dict, Any
from neo4j import GraphDatabase
from config.config import settings

NEO4J_URI = environ.get('NEO4J_URL')
NEO4J_USER = environ.get('NEO4J_USER')
NEO4J_PASSWORD = environ.get('NEO4J_PASSWORD')

if NEO4J_URI is None or NEO4J_URI == '':
    NEO4J_URI = settings.neo4j_uri

if NEO4J_USER is None or NEO4J_USER == '':
    NEO4J_USER = settings.neo4j_user

if NEO4J_PASSWORD is None or NEO4J_PASSWORD == '':
    NEO4J_PASSWORD = settings.neo4j_password

if NEO4J_URI is None or NEO4J_USER is None or NEO4J_PASSWORD is None:
    raise Exception('Neo4j environment variables not set')

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_neo4j_driver():
    """
    This function returns the Neo4j driver instance.
    """
    return neo4j_driver

def convert_neo4j_result(result: Dict[str, Any]):
    """
    This function converts the Neo4j result nodes or relationships into a dictionary format.

    @param result: the result of a Neo4j query.
    """
    if 'records' in result:
        return [record.data() for record in result['records']]
    return result
from setup.sql_setup.sql_setup import get_db_session
from setup.mongo_setup.mongo_setup import get_mongo_client, ObjectId

def test_create_mongo_session():
    client = get_mongo_client()
    assert client
    client.close()
    assert ObjectId
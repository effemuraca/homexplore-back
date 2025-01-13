# purpose:
#     this file contains the database model for this entity, that allows to interact with the databases with its methods.

from entities.TestEntity.class_test_entity import TestEntity
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver

class TestEntityDB:
    test_entity:TestEntity = None
    
    def __init__(self, test_entity:TestEntity):
        self.test_entity = test_entity
        
    #example mongo query    
    def get_test_entity_by_id(self, id:int):
        # this method should return the entity with the given id from the database
        mongo_client = get_default_mongo_db()
        self.test_entity = db.entity_collection.find_one({"_id":id})
        return test_entity
    
    #example neo4j query
    def get_test_entity_by_name(self, name:str):
        # this method should return the entity with the given name from the database
        neo4j_client = get_neo4j_driver()
        with driver.session() as session:
            result = session.run("MATCH (n:TestEntity {name: $name}) RETURN n", name=name)
            self.test_entity.attribute1 = result.single().get('attribute1')
        return test_entity
    
    #example redis query
    def get_test_entity_by_attribute(self, attribute:str):
        redis_client = get_redis_client()
        self.test_entity.attribute1 = redis_client.get(attribute)
        return test_entity
    
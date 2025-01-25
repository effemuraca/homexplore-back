# purpose:
#     this file contains the API endpoints for this module.

from fastapi import APIRouter, HTTPException
from entities.TestEntity.class_test_entity import TestEntity
from entities.TestEntity.db_model_test_entity import TestEntityDB

test_module_router = APIRouter()

@test_module_router.get("/test_module")
def get_test_module(id:int): #https://localhost:8080/module/test_module
    """
    This endpoint retrieves a test entity by its id.
    
    @param id: the id of the entity to retrieve.
    """
    test_entity = TestEntity(None, None, None, None)
    test_entity_db = TestEntityDB(test_entity)
    test_entity_db.get_test_entity_by_id(id)
    if test_entity.test_entity is None:
        raise HTTPException(status_code=404, detail="Test entity not found")
    return test_entity

# to make the routes more readable, it's better an handler structure like the one below.
# We can choose to keep the description in the handler or in the function.

@test_module_router.get("/test_module_2")
def get_test_module_2_handler(id:int):
    """
    This endpoint retrieves a test entity by its id.
    
    @param id: the id of the entity to retrieve.
    """
    return get_test_module_2(id)






def get_test_module_2(id:int):
    test_entity = TestEntity(None, None, None, None)
    test_entity_db = TestEntityDB(test_entity)
    test_entity_db.get_test_entity_by_id(id)
    if test_entity is None:
        raise HTTPException(status_code=404, detail="Test entity not found")
    return test_entity
    
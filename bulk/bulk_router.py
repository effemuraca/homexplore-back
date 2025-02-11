from fastapi import APIRouter
from bulk.neo4j import populate_neo4j_db, update_livability_scores, reset_neo4j_db
from bulk.redis import populate_redis_db, reset_redis_db, verify_redis_data
import os

bulk_router = APIRouter(prefix="/bulk", tags=["bulk"])

@bulk_router.post("/neo4j")
def populate_neo4j():
    """
    Populates the Neo4j database with the data from the MongoDB database.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if something goes wrong.
    """
    try:
        populate_neo4j_db()
        print(os.curdir)
        update_livability_scores()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Graph populated successfully!"}

@bulk_router.put("/neo4j/score")
def update_score():
    """
    Updates the livability scores in the Neo4j database.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if something goes wrong.
    """
    try:
        update_livability_scores()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Livability scores updated successfully!"}

@bulk_router.delete("/neo4j")
def delete_neo4j():
    """
    Deletes the Neo4j database.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if something goes wrong.
    """
    try:
        reset_neo4j_db()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Graph deleted successfully!"}

@bulk_router.post("/redis")
def populate_redis():
    """
    Populates the Redis database with the data from the CSV files.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if something goes wrong.
    """
    try:
        populate_redis_db()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Database populated successfully!"}

@bulk_router.delete("/redis")
def delete_redis():
    """
    Deletes the Redis database.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if something goes wrong.
    """
    try:
        reset_redis_db()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Database cleared successfully!"}

@bulk_router.get("/redis/verify")
def verify_redis():
    """
    Verifies the data in the Redis database.

    Returns:
        dict: A dictionary containing either a success message or an error.

    Raises:
        Exception: Propagates the exception as an error string if verification fails.
    """
    try:
        verify_redis_data()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Data verified successfully!"}
from fastapi import APIRouter
from bulk.neo4j import populate_neo4j_db, update_livability_scores, reset_neo4j_db
import os

bulk_router = APIRouter(prefix="/bulk", tags=["bulk"])

@bulk_router.post("/neo4j")
def populate_neo4j():
    """
    This function populates the Neo4j database with the data from the MongoDB database.
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
    This function updates the livability scores in the Neo4j database.
    """
    try:
        update_livability_scores()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Livability scores updated successfully!"}

@bulk_router.delete("/neo4j")
def delete_neo4j():
    """
    This function deletes the Neo4j database.
    """
    try:
        reset_neo4j_db()
    except Exception as e:
        return {"error": str(e)}
    return {"message": "Graph deleted successfully!"}
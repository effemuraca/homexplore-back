from entities.Neo4J.POI.poi import POI
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
import logging

logger = logging.getLogger(__name__)
class POIDB:
    def __init__(self):
        self.poi = None
        
    
    def get_poi_by_name(self) -> int:
        """ 
        Get a point of interest from the database.
        
        Returns:
        int: 200 if the property is retrieved successfully,
             404 if the property is not found,
             500 if an error occurs.
        """
        neo4j_driver = get_neo4j_driver()
        if not neo4j_driver:
            logger.error("Could not connect to Neo4J.")
            return 500
            
        with neo4j_driver.session() as session:
            try:
                query = (
                    "MATCH (p:POI {name: $name})"
                    "RETURN p"
                )
                result = session.run(query, name=self.poi.name)
                poi = result.single()
                if poi:
                    self.poi = POI(name=poi['name'],type=poi['type'], coordinates=poi['coordinates'])
                    return 200
                else:
                    return 404
            except Exception as e:
                logger.error(f"An error occurred in get_poi: {e}")
                return 500
    
    def create_poi(self) -> int:
        """ 
        Create a point of interest in the database.
        
        Returns:
        int: 201 if the property is created successfully,
             500 if an error occurs.
        """
        neo4j_driver = get_neo4j_driver()
        if not neo4j_driver:
            logger.error("Could not connect to Neo4J.")
            return 500
            
        with neo4j_driver.session() as session:
            try:
                query = (
                    "CREATE (p:POI {name: $name, type: $type,  coordinates: point({latitude: $latitude, longitude: $longitude})})"
                    "RETURN id(p)"
                )
                result = session.run(query, name=self.poi.name, type=self.poi.type, latitude=self.poi.coordinates.latitude, longitude=self.poi.coordinates.longitude)
                return 201
            except Exception as e:
                logger.error(f"An error occurred in create_poi: {e}")
                return 500
            
    def update_poi(self, poi: POI) -> int:
        """ 
        Update a point of interest in the database.
        
        Returns:
        int: 200 if the property is updated successfully,
             500 if an error occurs.
        """
        neo4j_driver = get_neo4j_driver()
        if not neo4j_driver:
            logger.error("Could not connect to Neo4J.")
            return 500
            
        with neo4j_driver.session() as session:
            try:
                query = (
                    "MATCH (p:POI {name: $name})"
                    "SET p.type = $type, p.coordinates = point({latitude: $latitude, longitude: $longitude})"
                    "RETURN p"
                )
                result = session.run(query, name=poi.name, type=poi.type, latitude=poi.coordinates.latitude, longitude=poi.coordinates.longitude)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in update_poi: {e}")
                return 500
            
    def delete_poi(self) -> int:
        """ 
        Delete a point of interest from the database.
        
        Returns:
        int: 200 if the property is deleted successfully,
             500 if an error occurs.
        """
        neo4j_driver = get_neo4j_driver()
        if not neo4j_driver:
            logger.error("Could not connect to Neo4J.")
            return 500
            
        with neo4j_driver.session() as session:
            try:
                query = (
                    "MATCH (p:POI {name: $name})"
                    "DELETE p"
                )
                session.run(query, name=self.poi.name)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in delete_poi: {e}")
                return 500
from entities.Neo4J.Neighbourhood.neighbourhood import Neighbourhood
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
import logging

logger = logging.getLogger(__name__)
class NeighbourhoodDB:
    def __init__(self): 
        self.neighbourhood = None
        
    
    def get_neighbourhood(self) -> int:
        """ 
        Get a neighbourhood from the database.
        
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
                    "MATCH (n:Neighbourhood {name: $name})"
                    "RETURN n"
                )
                result = session.run(query, name=self.neighbourhood.name)
                neighbourhood = result.single()
                if neighbourhood:
                    self.neighbourhood = Neighbourhood(name=neighbourhood['name'], coordinates=neighbourhood['coordinates'], safety_index=neighbourhood['safety_index'], health_care_index=neighbourhood['health_care_index'], cost_of_living_index=neighbourhood['cost_of_living_index'], pollution_index=neighbourhood['pollution_index'])
                    return 200
                else:
                    return 404
            except Exception as e:
                logger.error(f"An error occurred in get_neighbourhood: {e}")
                return 500
    
    def create_neighbourhood(self) -> int:
        """ 
        Create a neighbourhood in the database.
        
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
                    "CREATE (n:Neighbourhood {name: $name, coordinates: point({latitude: $latitude, longitude: $longitude})})"
                    "RETURN n"
                )
                result = session.run(query, name=self.neighbourhood.name, latitude=self.neighbourhood.coordinates.latitude, longitude=self.neighbourhood.coordinates.longitude)
                return 201
            except Exception as e:
                logger.error(f"An error occurred in create_neighbourhood: {e}")
                return 500
            
    def update_neighbourhood(self, neighbourhood: Neighbourhood) -> int:
        """ 
        Update a neighbourhood in the database.
        
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
                    "MATCH (n:Neighbourhood {name: $name})"
                    "SET n.coordinates = point({latitude: $latitude, longitude: $longitude}), n.safety_index = $safety_index, n.health_care_index = $health_care_index, n.cost_of_living_index = $cost_of_living_index, n.pollution_index = $pollution_index"
                    "RETURN n"
                )
                result = session.run(query, name=neighbourhood.name, latitude=neighbourhood.coordinates.latitude, longitude=neighbourhood.coordinates.longitude, safety_index=neighbourhood.safety_index, health_care_index=neighbourhood.health_care_index, cost_of_living_index=neighbourhood.cost_of_living_index, pollution_index=neighbourhood.pollution_index)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in update_neighbourhood: {e}")
                return 500
       
    def delete_neighbourhood(self) -> int:
        """ 
        Delete a neighbourhood from the database.
        
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
                    "MATCH (n:Neighbourhood {name: $name})"
                    "DETACH DELETE n"
                )
                session.run(query, name=self.neighbourhood.name)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in delete_neighbourhood: {e}")
                return 500
                
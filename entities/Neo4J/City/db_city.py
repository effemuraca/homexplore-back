from entities.Neo4J.City.city import City
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
import logging

logger = logging.getLogger(__name__)
class CityDB:
    def __init__(self):
        self.city = None
        
    
    def get_city(self) -> int:
        """ 
        Get a city from the database.
        
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
                    "MATCH (c:City {name: $name})"
                    "RETURN c"
                )
                result = session.run(query, name=self.city.name)
                city = result.single()
                if city:
                    self.city = City(name=city['name'], coordinates=city['coordinates'], safety_index=city['safety_index'], health_care_index=city['health_care_index'], cost_of_living_index=city['cost_of_living_index'], pollution_index=city['pollution_index'])
                    return 200
                else:
                    return 404
            except Exception as e:
                logger.error(f"An error occurred in get_city: {e}")
                return 500
    
    def create_city(self) -> int:
        """ 
        Create a city in the database.
        
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
                    "CREATE (c:City {name: $name, coordinates: point({latitude: $latitude, longitude: $longitude}), safety_index: $safety_index, health_care_index: $health_care_index, cost_of_living_index: $cost_of_living_index, pollution_index: $pollution_index})"
                    "RETURN id(c)"
                )
                result = session.run(query, name=self.city.name, latitude=self.city.coordinates.latitude, longitude=self.city.coordinates.longitude, safety_index=self.city.safety_index, health_care_index=self.city.health_care_index, cost_of_living_index=self.city.cost_of_living_index, pollution_index=self.city.pollution_index)
                city_id = result.single()[0]
                return 201
            except Exception as e:
                logger.error(f"An error occurred in create_city: {e}")
                return 500
                
    def update_city(self, city: City) -> int:
        """ 
        Update a city in the database.
        
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
                    "MATCH (c:City {name: $name})"
                    "SET c.coordinates = point({latitude: $latitude, longitude: $longitude}), c.safety_index = $safety_index, c.health_care_index = $health_care_index, c.cost_of_living_index = $cost_of_living_index, c.pollution_index = $pollution_index"
                )
                session.run(query, name=city.name, latitude=city.coordinates.latitude, longitude=city.coordinates.longitude, safety_index=city.safety_index, health_care_index=city.health_care_index, cost_of_living_index=city.cost_of_living_index, pollution_index=city.pollution_index)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in update_city: {e}")
                return 500
            
    def delete_city(self) -> int:
        """ 
        Delete a city from the database.
        
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
                    "MATCH (c:City {name: $name})"
                    "DETACH DELETE c"
                )
                session.run(query, name=self.city.name)
                return 200
            except Exception as e:
                logger.error(f"An error occurred in delete_city: {e}")
                return 500 
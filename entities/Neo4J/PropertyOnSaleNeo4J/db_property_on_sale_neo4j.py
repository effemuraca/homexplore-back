import logging
import math
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
from entities.Neo4J.PropertyOnSaleNeo4J.property_on_sale_neo4j import PropertyOnSaleNeo4J
from entities.Neo4J.Neighbourhood.neighbourhood import Neighbourhood, Neo4jPoint
from entities.Neo4J.City.city import City
from entities.Neo4J.POI.poi import POI
from typing import List


logger = logging.getLogger(__name__)
class PropertyOnSaleNeo4JDB:
    def __init__(self, property_on_sale_neo4j: PropertyOnSaleNeo4J):
        self.property_on_sale_neo4j: PropertyOnSaleNeo4J = property_on_sale_neo4j
        self.near_properties: List[PropertyOnSaleNeo4J] = None
        self.neighbourhood: Neighbourhood = None
        self.city: City = None
        self.pois: List[POI] = None
        
    def get_property_on_sale_neo4j(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        with neo4j_driver.session() as session:
            try:
                result = session.run(
                    "MATCH (p:PropertyOnSale) "
                    "WHERE p.property_on_sale_id = $property_on_sale_id "
                    "RETURN p",
                    property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                )
            except Exception as e:
                logger.error("Error while retrieving property on sale on Neo4j with id %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500
            result_list = list(result)
            if not result_list:
                return 404
            
            coordinates = Neo4jPoint(latitude=dict(result_list[0]["p"])["coordinates"].latitude, longitude=dict(result_list[0]["p"])["coordinates"].longitude)
            self.property_on_sale_neo4j = PropertyOnSaleNeo4J(**{k: v for k, v in dict(result_list[0]["p"]).items() if k != 'coordinates'}, coordinates=coordinates.model_dump())
            return 200
    
    def create_property_on_sale_neo4j(self, neighbourhood_name: str):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        try:
            with neo4j_driver.session() as session:
                def tx_func(tx):
                    # Extract properties from the model dump and remove the 'coordinates' key from the properties dictionary.
                    properties = self.property_on_sale_neo4j.model_dump()
                    coordinates = properties.pop('coordinates', None)

                    # Verify that the coordinates are provided.
                    if coordinates is None:
                        raise ValueError("Coordinates were not provided")

                    # Use MERGE to avoid duplicate nodes, and set the node properties.
                    # The coordinates are set using the Neo4j built-in 'point' function.
                    query1 = """
                    MERGE (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    ON CREATE SET p += $properties_on_sale,
                                p.coordinates = point({latitude: $latitude, longitude: $longitude})
                    ON MATCH SET p += $properties_on_sale,
                                p.coordinates = point({latitude: $latitude, longitude: $longitude})
                    """
                    tx.run(
                        query1,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        properties_on_sale=properties,
                        latitude=coordinates['latitude'],
                        longitude=coordinates['longitude']
                    )

                    # The neighbourhood is identified by its name.
                    query2 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    MERGE (n:Neighbourhood {name: $neighbourhood_name})
                    MERGE (p)-[:LOCATED_IN_NEIGHBOURHOOD]->(n)
                    """
                    tx.run(
                        query2,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        neighbourhood_name=neighbourhood_name
                    )

                    # Step 3: Create NEAR relationships between the property and all existing POI nodes
                    # where the distance between their coordinates is less than or equal to 500 meters.
                    query3 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (poi:POI)
                    WHERE point.distance(p.coordinates, poi.coordinates) <= 500
                    MERGE (p)-[r:NEAR]->(poi)
                    SET r.distance = point.distance(p.coordinates, poi.coordinates)
                    """
                    tx.run(
                        query3,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                    )

                    # Step 4: Create bidirectional NEAR_PROPERTY relationships between the new property and all existing properties
                    # where the distance is less than or equal to 500 meters.
                    query4 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (other:PropertyOnSale)
                    WHERE other.property_on_sale_id <> $property_on_sale_id
                    AND point.distance(p.coordinates, other.coordinates) <= 500
                    MERGE (p)-[r:NEAR_PROPERTY]->(other)
                    SET r.distance = point.distance(p.coordinates, other.coordinates)
                    MERGE (other)-[r2:NEAR_PROPERTY]->(p)
                    SET r2.distance = point.distance(p.coordinates, other.coordinates)
                    """
                    tx.run(
                        query4,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                    )
                # Execute all transactional steps
                session.write_transaction(tx_func)
            return 201
        except Exception as e:
            logger.error("Error while creating property on sale on Neo4j with id %s: %s", 
                        self.property_on_sale_neo4j.property_on_sale_id, e)
            return 500


    
    def update_property_on_sale_neo4j(self, update_data: PropertyOnSaleNeo4J, neighbourhood_name: str = None):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500

        try:
            with neo4j_driver.session() as session:
                def tx_func(tx):
                    # Create a dictionary of properties from update_data, excluding 'property_on_sale_id'
                    # and also 'coordinates' if present. This avoids sending a map as a property value.
                    update_properties = update_data.model_dump(exclude_none=True, exclude={"property_on_sale_id", "coordinates"})
                    
                    # Always update the property node with the provided fields (excluding coordinates)
                    query_update_property = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    SET p += $update_properties
                    """
                    tx.run(
                        query_update_property,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        update_properties=update_properties
                    )

                    # If coordinates are provided, update the coordinates and related spatial relationships.
                    if update_data.coordinates is not None:
                        coordinates = update_data.coordinates

                        # Delete all relationships except those of type LOCATED_IN_NEIGHBOURHOOD,
                        # so that we preserve the neighbourhood relationship if not updated.
                        delete_query = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})-[r]-()
                        WHERE NOT type(r) = 'LOCATED_IN_NEIGHBOURHOOD'
                        DELETE r
                        """
                        tx.run(delete_query, property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id)

                        # Update the node's coordinates using the Neo4j point() function.
                        query_update_coords = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                        SET p.coordinates = point({latitude: $latitude, longitude: $longitude})
                        """
                        tx.run(
                            query_update_coords,
                            property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                            latitude=coordinates.latitude,
                            longitude=coordinates.longitude
                        )

                        # Create NEAR relationships between the property and all POI nodes within 500 meters.
                        query_near_poi = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (poi:POI)
                        WHERE point.distance(p.coordinates, poi.coordinates) <= 500
                        MERGE (p)-[r:NEAR]->(poi)
                        SET r.distance = point.distance(p.coordinates, poi.coordinates)
                        """
                        tx.run(
                            query_near_poi,
                            property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                        )

                        # Create bidirectional NEAR_PROPERTY relationships with other properties within 500 meters.
                        query_near_property = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (other:PropertyOnSale)
                        WHERE other.property_on_sale_id <> $property_on_sale_id
                        AND point.distance(p.coordinates, other.coordinates) <= 500
                        MERGE (p)-[r:NEAR_PROPERTY]->(other)
                        SET r.distance = point.distance(p.coordinates, other.coordinates)
                        MERGE (other)-[r2:NEAR_PROPERTY]->(p)
                        SET r2.distance = point.distance(p.coordinates, other.coordinates)
                        """
                        tx.run(
                            query_near_property,
                            property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                        )

                    # If a neighbourhood is provided, update the neighbourhood relationship.
                    if neighbourhood_name is not None:
                        # Delete any existing LOCATED_IN_NEIGHBOURHOOD relationship.
                        delete_neighbourhood_query = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})-[r:LOCATED_IN_NEIGHBOURHOOD]-()
                        DELETE r
                        """
                        tx.run(
                            delete_neighbourhood_query,
                            property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                        )

                        # Create the new neighbourhood relationship.
                        query_neighbourhood = """
                        MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                        MERGE (n:Neighbourhood {name: $neighbourhood_name})
                        MERGE (p)-[:LOCATED_IN_NEIGHBOURHOOD]->(n)
                        """
                        tx.run(
                            query_neighbourhood,
                            property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                            neighbourhood_name=neighbourhood_name
                        )

                # Execute all operations in a single transaction.
                session.write_transaction(tx_func)
            return 200

        except Exception as e:
            logger.error("Error while updating property on sale on Neo4j with id %s: %s",
                        self.property_on_sale_neo4j.property_on_sale_id, e)
            return 500


    
    def delete_property_on_sale_neo4j(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        try:
            with neo4j_driver.session() as session:
                def tx_func(tx):
                    query = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    DETACH DELETE p
                    """
                    tx.run(
                        query,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                    )
                session.write_transaction(tx_func)
            return 200
        except Exception as e:
            logger.error("Error while deleting property on sale on Neo4j with id %s: %s", 
                        self.property_on_sale_neo4j.property_on_sale_id, e)
            return 500

        
    def get_city_and_neighbourhood(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        print(self.property_on_sale_neo4j.property_on_sale_id)
        with neo4j_driver.session() as session:
            try:
                query = """
                MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                MATCH (p)-[:LOCATED_IN_NEIGHBOURHOOD]->(n:Neighbourhood)-[:BELONGS_TO_CITY]-(c:City)
                RETURN n AS neighbourhood, c AS city
                """
                result = session.run(query, property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id)
            except Exception as e:
                logger.error("Error while retrieving city and neighbourhood for property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500
            result_list = list(result)
            if not result_list:
                return 404
            row = result_list[0]
            city_coordinates = Neo4jPoint(latitude=dict(row["city"])["coordinates"].latitude, longitude=dict(row["city"])["coordinates"].longitude)
            neighbourhood_coordinates = Neo4jPoint(latitude=dict(row["neighbourhood"])["coordinates"].latitude, longitude=dict(row["neighbourhood"])["coordinates"].longitude)
            self.city = City(**{k: v for k, v in dict(row["city"]).items() if k != 'coordinates'}, coordinates=city_coordinates.model_dump())
            self.neighbourhood = Neighbourhood(**{k: v for k, v in dict(row["neighbourhood"]).items() if k != 'coordinates'}, coordinates=neighbourhood_coordinates.model_dump())
            return 200
        
    def get_near_POIs(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        with neo4j_driver.session() as session:
            try:
                query = """
                MATCH (p:PropertyOnSale)-[:NEAR]->(poi:POI)
                WHERE p.property_on_sale_id = $property_on_sale_id
                RETURN poi
                """
                result = session.run(query, property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id)
            except Exception as e:
                logger.error("Error while retrieving POIs for property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500
            
            result_list = list(result)
            if not result_list:
                return 404
            
            self.pois = []
            for record in result_list:
                poi_node = record["poi"]
                node_dict = dict(poi_node)
                
                poi_coordinates = node_dict.pop("coordinates", None)
                
                coordinates = Neo4jPoint(latitude=poi_coordinates.latitude, longitude=poi_coordinates.longitude)
                
                self.pois.append(POI(**node_dict, coordinates=coordinates.model_dump()))
            
            return 200
    
    def get_near_properties(self):
        """
        Retrieve two levels of near properties for the current property.
        Level 1: Properties directly connected via a NEAR relationship.
        Level 2: Properties that are connected via a NEAR relationship from a level 1 property.
        """
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500
        with neo4j_driver.session() as session:
            try:
                query = """
                MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                OPTIONAL MATCH (p)-[:NEAR_PROPERTY]->(p2:PropertyOnSale)
                OPTIONAL MATCH (p2)-[:NEAR_PROPERTY]->(p3:PropertyOnSale)
                RETURN collect(DISTINCT p2) AS level1, collect(DISTINCT p3) AS level2
                """
                result = session.run(query, property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id)
            except Exception as e:
                logger.error("Error while retrieving near properties to property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500

            record = result.single()
            if record is None:
                return 404

            # Extract the two levels from the returned record. If none, default to empty lists
            level1_nodes = record.get("level1", [])
            level2_nodes = record.get("level2", [])
            

            # Extract the properties from the nodes and store them in the corresponding lists
            self.near_properties = []
            for node in level1_nodes:
                coordinates = Neo4jPoint(latitude=node["coordinates"].latitude, longitude=node["coordinates"].longitude)
                self.near_properties.append(PropertyOnSaleNeo4J(**{k: v for k, v in dict(node).items() if k != 'coordinates'}, coordinates=coordinates.model_dump()))
            for node in level2_nodes:
                coordinates = Neo4jPoint(latitude=node["coordinates"].latitude, longitude=node["coordinates"].longitude)
                self.near_properties.append(PropertyOnSaleNeo4J(**{k: v for k, v in dict(node).items() if k != 'coordinates'}, coordinates=coordinates.model_dump()))

            return 200
    
    def update_livability_score(self):
        """
        Calculate and update the livability score for the current PropertyOnSale node.
        
        This method retrieves the nearby POIs (via the NEAR relationship), aggregates the counts 
        and the minimum distances for each POI type, computes the livability score using predefined 
        weights, and finally updates the PropertyOnSale node with the calculated score.
        """

        poi_weights = {
            "hospital": 0.5,
            "school": 0.2,
            "park": 0.3,
            "police": 0.2,
            "supermarket": 0.3,
            "kindergarten": 0.1,
            "factory": -0.2,
            "landfill": -0.3,
            "prison": -0.4,
            "grave_yard": -0.1
        }
        
        def calculate_livability_score(poi_weights, distances, counts):
            for poi in poi_weights.keys():
                if poi not in distances:
                    distances[poi] = 500
                if poi not in counts:
                    counts[poi] = 0
            
            # Calculate the total contribution from each POI type
            # The score contribution decreases with distance
            x = sum(counts[poi] * weight * math.exp(-distances[poi] / 1000) for poi, weight in poi_weights.items())
            # Normalize the score using an exponential function
            score = 100 - 100 * math.exp(-x)
            return score

        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            logger.error("Neo4j driver not initialized.")
            return 500

        with neo4j_driver.session() as session:
            # Retrieve the POI information (grouped by type) for the current property
            try:
                result = session.run(
                    """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_id})- [r:NEAR] -> (poi:POI)
                    RETURN toLower(trim(poi.type)) AS poi_type, count(poi) AS cnt, min(r.distance) AS min_distance
                    """,
                    property_id=self.property_on_sale_neo4j.property_on_sale_id
                )
            except Exception as e:
                logger.error("Error retrieving POI information for property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500
            counts = {}
            distances = {}
            for rec in result:
                poi_type = rec["poi_type"]
                counts[poi_type] = rec["cnt"]
                distances[poi_type] = rec["min_distance"]
            
            # Ensure defaults for any POI types not found in the query
            for poi in poi_weights.keys():
                if poi not in counts:
                    counts[poi] = 0
                if poi not in distances:
                    distances[poi] = 500
            
            try:
                # Calculate the livability score using the helper function
                score = calculate_livability_score(poi_weights, distances, counts)
            except Exception as e:
                logger.error("Error calculating livability score for property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                score = 0
            
            # Update the PropertyOnSale node with the calculated livability score
            try:
                session.run(
                    """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_id})
                    SET p.score = $score
                    """,
                    property_id=self.property_on_sale_neo4j.property_on_sale_id,
                    score=score
                )
            except Exception as e:
                logger.error("Error updating livability score for property %s: %s", 
                            self.property_on_sale_neo4j.property_on_sale_id, e)
                return 500
            
            return 200
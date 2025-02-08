import logging
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
from entities.Neo4J.PropertyOnSaleNeo4J.property_on_sale_neo4j import PropertyOnSaleNeo4J
from entities.Neo4J.Neighbourhood.neighbourhood import Neighbourhood, Neo4jPoint
from entities.Neo4J.City.city import City
from entities.Neo4J.POI.poi import POI


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
                logging.error("Error while retrieving property on sale: %s", e)
                return 500
            result_list = list(result)
            if not result_list:
                return 404
            
            self.property_on_sale_neo4j = PropertyOnSaleNeo4J(**dict(result_list[0]["p"]))
            return 200
    
    def create_property_on_sale_neo4j(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            return 500
        try:
            with neo4j_driver.session() as session:
                def tx_func(tx):
                    # 1. Create or update the PropertyOnSale node using MERGE to avoid duplicates
                    query1 = """
                    MERGE (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    ON CREATE SET p += $properties_on_sale
                    ON MATCH SET p += $properties_on_sale
                    """
                    tx.run(
                        query1,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        properties_on_sale=self.property_on_sale_neo4j.dict()
                    )

                    # 2. Link the PropertyOnSale node to the corresponding Neighbourhood node
                    query2 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    MERGE (n:Neighbourhood {neighbourhood_id: $neighbourhood_id})
                    MERGE (p)-[:LOCATED_IN_NEIGHBOURHOOD]->(n)
                    """
                    tx.run(
                        query2,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        neighbourhood_id=self.property_on_sale_neo4j.neighbourhood_id
                    )

                    # 3. Create NEAR relationships between the property and all existing POI nodes (distance <= 500m)
                    query3 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (poi:POI)
                    WHERE p.coordinates.distance(poi.coordinates) <= 500
                    MERGE (p)-[r:NEAR]->(poi)
                    SET r.distance = p.coordinates.distance(poi.coordinates)
                    """
                    tx.run(
                        query3,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                    )

                    # 4. Create bidirectional NEAR_PROPERTY relationships between the new property and all existing properties (distance <= 500m)
                    query4 = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id}), (other:PropertyOnSale)
                    WHERE other.property_on_sale_id <> $property_on_sale_id
                    AND p.coordinates.distance(other.coordinates) <= 500
                    MERGE (p)-[r:NEAR_PROPERTY]->(other)
                    SET r.distance = p.coordinates.distance(other.coordinates)
                    MERGE (other)-[r2:NEAR_PROPERTY]->(p)
                    SET r2.distance = p.coordinates.distance(other.coordinates)
                    """
                    tx.run(
                        query4,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id
                    )

                session.write_transaction(tx_func)
            return 201
        except Exception as e:
            logging.error("Error while creating property on sale: %s", e)
            return 500
    
    def update_property_on_sale_neo4j(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
            return 500
        try:
            with neo4j_driver.session() as session:
                def tx_func(tx):
                    query = """
                    MATCH (p:PropertyOnSale {property_on_sale_id: $property_on_sale_id})
                    SET p += $properties_on_sale
                    """
                    tx.run(
                        query,
                        property_on_sale_id=self.property_on_sale_neo4j.property_on_sale_id,
                        properties_on_sale=self.property_on_sale_neo4j.model_dump()
                    )
                session.write_transaction(tx_func)
            return 200
        except Exception as e:
            logging.error("Error while updating property on sale: %s", e)
            return 500
    
    def delete_property_on_sale_neo4j(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
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
            logging.error("Error while deleting property on sale: %s", e)
            return 500

        
    def get_city_and_neighbourhood(self):
        neo4j_driver = get_neo4j_driver()
        if neo4j_driver is None:
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
                logging.error("Error while retrieving city and neighbourhood: %s", e)
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
                logging.error("Error while retrieving POIs: %s", e)
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
                logging.error("Error while retrieving near properties: %s", e)
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
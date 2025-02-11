import pandas as pd
from setup.neo4j_setup.neo4j_setup import get_neo4j_driver
import math

# Helper function to execute queries in Neo4j
def create_nodes(tx, query, parameters):
    tx.run(query, parameters)

def parse_coordinates(latitude: str, longitude: str) -> dict:
    """
    Parse latitude and longitude strings into a dictionary.
    :param latitude: The latitude as a string.
    :param longitude: The longitude as a string.
    :return: A dictionary with the latitude and longitude as floats.
    """
    return {"latitude": float(latitude), "longitude": float(longitude)}

def populate_neo4j_db():
    """
    Populate the Neo4j database with the data from the CSV files.
    This function creates nodes for cities, neighbourhoods, properties, and POIs.
    It also establishes relationships between the nodes based on proximity.
    """
    
    cities_df = pd.read_csv('bulk/files/Neo4J/cities.csv')
    neighbourhoods_df = pd.read_csv('bulk/files/Neo4J/neighbourhoods.csv')
    # Remove neighbourhood rows with name "Unknown"
    neighbourhoods_df = neighbourhoods_df[neighbourhoods_df["name"] != "Unknown"]

    properties_df = pd.read_csv('bulk/files/Neo4J/properties_on_sale_neo4j.csv', dtype={"coordinates": str})
    properties_df = properties_df.drop_duplicates(subset=["property_on_sale_id"])
    
    pois_df = pd.read_csv('bulk/files/Neo4J/pois.csv')
    # Remove POI rows with name "Unknown"
    pois_df = pois_df[pois_df["name"] != "Unknown"]

    neo4j_driver = get_neo4j_driver()
    with neo4j_driver.session() as session:
        # Set constraint
        #session.write_transaction(lambda tx: tx.run("CREATE CONSTRAINT FOR (p:PropertyOnSale) REQUIRE p.property_on_sale_id IS UNIQUE"))
        
        counter = 1
        # Create City nodes
        for _, row in cities_df.iterrows():
            print(f"Processing city {row['city']} ({counter}/{len(cities_df)})")
            session.write_transaction(
                create_nodes,
                """
                CREATE (c:City {
                    name: $name,
                    coordinates: point({latitude: $latitude, longitude: $longitude}),
                    safety_index: $safety_index,
                    health_care_index: $health_care_index,
                    cost_of_living_index: $cost_of_living_index,
                    pollution_index: $pollution_index
                })
                """,
                {
                    "name": row["city"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "safety_index": row["safety_index"],
                    "health_care_index": row["health_care_index"],
                    "cost_of_living_index": row["cost_of_living_index"],
                    "pollution_index": row["pollution_index"]
                }
            )
            counter += 1
        
        counter = 1
        # Create Neighbourhood nodes and link them to the corresponding City
        for _, row in neighbourhoods_df.iterrows():
            print(f"Processing neighbourhood {row['name']} ({counter}/{len(neighbourhoods_df)})")
            session.write_transaction(
                create_nodes,
                """
                MATCH (c:City {name: $city_name})
                CREATE (n:Neighbourhood {
                    name: $name,
                    coordinates: point({latitude: $latitude, longitude: $longitude})
                })-[:BELONGS_TO_CITY]->(c)
                """,
                {
                    "city_name": row["city"],
                    "name": row["name"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"]
                }
            )
            counter += 1
        
        counter = 1
        # Create Property nodes and link them to the corresponding Neighbourhood
        for _, row in properties_df.iterrows():
            print(f"Processing property {row['property_on_sale_id']} ({counter}/{len(properties_df)})")
            # Use separate latitude and longitude columns to build the coordinate
            coordinates = parse_coordinates(row["latitude"], row["longitude"])
            session.write_transaction(
                create_nodes,
                """
                MATCH (n:Neighbourhood {name: $neighbourhood_name})
                MERGE (p:PropertyOnSale { property_on_sale_id: $property_on_sale_id })
                ON CREATE SET p.coordinates = point($coordinates),
                            p.price = $price,
                            p.type = $type,
                            p.thumbnail = $thumbnail
                CREATE (p)-[:LOCATED_IN_NEIGHBOURHOOD]->(n)
                """,
                {
                    "property_on_sale_id": row["property_on_sale_id"],
                    "coordinates": coordinates,
                    "price": row["price"],
                    "type": row["type"],
                    "thumbnail": row["thumbnail"],
                    "neighbourhood_name": row["neighbourhood"]
                }
            )
            counter += 1
        
        counter = 1
        # Create POI nodes
        for _, row in pois_df.iterrows():
            print(f"Processing POI {row['name']} ({counter}/{len(pois_df)})")
            session.write_transaction(
                create_nodes,
                """
                CREATE (poi:POI {
                    name: $name,
                    type: $type,
                    coordinates: point({latitude: $latitude, longitude: $longitude})
                })
                """,
                {
                    "name": row["name"],
                    "type": row["type"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"]
                }
            )
            counter += 1

    # After nodes are created, use Cypher with the built-in distance function to create relationships.
    create_near_relationships()
    create_near_property_relationships()


def create_near_relationships():
    """
    Create NEAR relationships between PropertyOnSale and POI nodes in Neo4j.
    Relationships are created only if the distance between a property and a POI is ≤ 500 meters.
    """
    neo4j_driver = get_neo4j_driver()
    with neo4j_driver.session() as session:
        session.write_transaction(lambda tx: tx.run(
            """
            MATCH (p:PropertyOnSale), (poi:POI)
            WHERE point.distance(p.coordinates, poi.coordinates) <= 500
            CREATE (p)-[:NEAR { distance: point.distance(p.coordinates, poi.coordinates) }]->(poi)
            """
        ))
        print("NEAR relationships between properties and POIs created.")
    return True

def create_near_property_relationships():
    """
    Create bidirectional NEAR_PROPERTY relationships between PropertyOnSale nodes.
    Only properties with a distance ≤ 500 meters will be linked.
    To avoid duplicate links, we use a condition on property IDs.
    """
    neo4j_driver = get_neo4j_driver()
    with neo4j_driver.session() as session:
        session.write_transaction(lambda tx: tx.run(
            """
            MATCH (p1:PropertyOnSale), (p2:PropertyOnSale)
            WHERE p1.property_on_sale_id < p2.property_on_sale_id
              AND point.distance(p1.coordinates, p2.coordinates) <= 500
            CREATE (p1)-[:NEAR_PROPERTY { distance: point.distance(p1.coordinates, p2.coordinates) }]->(p2),
                   (p2)-[:NEAR_PROPERTY { distance: point.distance(p1.coordinates, p2.coordinates) }]->(p1)
            """
        ))
        print("NEAR_PROPERTY relationships between properties created.")
    return True

def calculate_livability_score(poi_weights, distances, counts):
    """
    Calculate the livability score based on the given POI weights, distances, and counts.
    
    For each key in poi_weights, if a key is missing in distances or counts, defaults are set:
      - Count default: 0
      - Distance default: 500 meters
      
    :param poi_weights: A dictionary where keys are POI types and values are their respective weights.
    :param distances: A dictionary where keys are POI types and values are the minimum distance (in meters).
    :param counts: A dictionary where keys are POI types and values are the counts.
    :return: The final livability score as a float.
    """
    # For every expected POI type, set default values if missing.
    for poi in poi_weights.keys():
        if poi not in distances:
            distances[poi] = 500
        if poi not in counts:
            counts[poi] = 0

    # Calculate total contribution (x)
    x = sum(counts[poi] * weight * math.exp(-distances[poi]/1000) for poi, weight in poi_weights.items())
    # Normalize the score using the exponential function
    score = 100 - 100 * math.exp(-x)
    return score


def update_livability_scores():
    """
    Update the livability scores for each PropertyOnSale node in the Neo4j database.
    
    For each property, this function retrieves related POIs through the NEAR relationship,
    groups the results by POI type, and constructs dictionaries for counts and minimum distances.
    
    If a particular POI type (e.g., hospital, school, etc.) is not found,
    defaults are used (0 count and 500 meters distance).
    
    The function then calculates the livability score using calculate_livability_score() and updates the node.
    """
    # Define the weights for each POI type (all keys are in lowercase)
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
    
    neo4j_driver = get_neo4j_driver()
    with neo4j_driver.session() as session:
        # Retrieve all property nodes
        properties = session.run("MATCH (p:PropertyOnSale) RETURN p.property_on_sale_id AS pid")
        for record in properties:
            print(f"Processing property {record['pid']}")
            property_id = record["pid"]
            # Retrieve POI information (group by type: count and minimum distance) for the current property
            result = session.run(
                """
                MATCH (p:PropertyOnSale {property_on_sale_id: $property_id})- [r:NEAR] -> (poi:POI)
                RETURN toLower(trim(poi.type)) AS poi_type, count(poi) AS cnt, min(r.distance) AS min_distance
                """,
                {"property_id": property_id}
            )
            counts = {}
            distances = {}
            for rec in result:
                poi_type = rec["poi_type"]
                counts[poi_type] = rec["cnt"]
                distances[poi_type] = rec["min_distance"]
            # For every expected POI type, if no data was found, assign defaults
            for poi in poi_weights.keys():
                if poi not in counts:
                    counts[poi] = 0
                if poi not in distances:
                    distances[poi] = 500
            try:
                score = calculate_livability_score(poi_weights, distances, counts)
            except Exception as e:
                print(f"Error calculating livability score for property {property_id}: {e}")
                score = 0
            # Update the PropertyOnSale node with the calculated livability score
            session.run(
                """
                MATCH (p:PropertyOnSale {property_on_sale_id: $property_id})
                SET p.score = $score
                """,
                {"property_id": property_id, "score": score}
            )
            print(f"Updated property {property_id} with livability score {score:.2f}")

def reset_neo4j_db():
    """
    Reset the Neo4j database by deleting all nodes and relationships.
    """
    try:
        neo4j_driver = get_neo4j_driver()
        with neo4j_driver.session() as session:
            session.write_transaction(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
        return {"status": "Database successfully reset"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

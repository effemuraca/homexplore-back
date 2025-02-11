import pandas as pd
from datetime import datetime
import json
from setup.mongo_setup.mongo_setup import get_default_mongo_db

# Database and collection names
BUYER_COLLECTION = "Buyer"
SELLER_COLLECTION = "Seller"
PROPERTY_COLLECTION = "PropertyOnSale"

buyers_csv = 'bulk/files/MongoDB/buyers.csv'
sellers_csv = 'bulk/files/MongoDB/sellers.csv'
properties_csv = 'bulk/files/MongoDB/properties_on_sale.csv'

# Function to parse and insert data into MongoDB
def populate_mongodb():
    db = get_default_mongo_db()

    # Load CSV files
    buyers_data = pd.read_csv(buyers_csv)
    sellers_data = pd.read_csv(sellers_csv)
    properties_data = pd.read_csv(properties_csv)

    # Remove latitude and longitude columns from properties data
    properties_data = properties_data.drop(['latitude', 'longitude'], axis=1, errors='ignore')

    # Convert data to dictionary format for MongoDB insertion
    buyers_records = buyers_data.to_dict(orient='records')
    sellers_records = sellers_data.to_dict(orient='records')
    properties_records = properties_data.to_dict(orient='records')

    # Insert data into collections
    db[BUYER_COLLECTION].insert_many(buyers_records)
    db[SELLER_COLLECTION].insert_many(sellers_records)
    db[PROPERTY_COLLECTION].insert_many(properties_records)

    print("Data inserted successfully into MongoDB.")

# Function to clear MongoDB collections
def clear_mongodb():
    client = get_mongo_client()
    db = client[DB_NAME]

    db[BUYER_COLLECTION].delete_many({})
    db[SELLER_COLLECTION].delete_many({})
    db[PROPERTY_COLLECTION].delete_many({})

    print("All collections cleared successfully.")

# Function to verify inserted data
def verify_mongodb_data():
    client = get_mongo_client()
    db = client[DB_NAME]

    buyer_sample = db[BUYER_COLLECTION].find_one()
    seller_sample = db[SELLER_COLLECTION].find_one()
    property_sample = db[PROPERTY_COLLECTION].find_one()

    print("Sample Buyer Data:", json.dumps(buyer_sample, indent=4, default=str))
    print("Sample Seller Data:", json.dumps(seller_sample, indent=4, default=str))
    print("Sample Property Data:", json.dumps(property_sample, indent=4, default=str))

# Example usage:
# populate_mongodb('path/to/buyers.csv', 'path/to/sellers.csv', 'path/to/property_on_sale.csv')
# clear_mongodb()
# verify_mongodb_data()

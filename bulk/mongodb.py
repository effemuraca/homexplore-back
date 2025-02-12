import pandas as pd
from datetime import datetime
import json
from bson import ObjectId
from setup.mongo_setup.mongo_setup import get_default_mongo_db

# Database and collection names
BUYER_COLLECTION = "Buyer"
SELLER_COLLECTION = "Seller"
PROPERTY_COLLECTION = "PropertyOnSale"

buyers_csv = 'bulk/files/MongoDB/buyers.csv'
sellers_csv = 'bulk/files/MongoDB/sellers.csv'
properties_csv = 'bulk/files/MongoDB/properties_on_sale.csv'

def convert_ids(obj):
    """
    Recursively convert any '_id' fields from strings to ObjectId.
    It strips extra whitespace and quotes before conversion.
    """
    if isinstance(obj, dict):
        # If the dictionary has an '_id' key and it is a string, attempt conversion.
        if '_id' in obj and isinstance(obj['_id'], str):
            cleaned_id = obj['_id'].strip().strip('"').strip("'")
            if ObjectId.is_valid(cleaned_id):
                obj['_id'] = ObjectId(cleaned_id)
        # Recursively process all dictionary values.
        for key, value in obj.items():
            obj[key] = convert_ids(value)
        return obj
    elif isinstance(obj, list):
        # Process each item in the list recursively.
        return [convert_ids(item) for item in obj]
    else:
        # Return the object unchanged.
        return obj

def clean_record(record):
    """
    Remove the 'description' field if it is NaN, if it equals the string 'nan'
    (case insensitive), or if it is a dict with a "$numberDouble" key equal to "NaN".
    """
    if 'description' in record:
        desc = record['description']
        if pd.isna(desc) or (isinstance(desc, str) and desc.lower() == 'nan'):
            del record['description']
        elif isinstance(desc, dict) and desc.get('$numberDouble') == 'NaN':
            del record['description']
        elif isinstance(desc, dict) and pd.isna(desc.get('$numberDouble')):
            del record['description']
    if 'bath_number' in record:
        bath_number = record['bath_number']
        if pd.isna(bath_number):
            del record['bath_number']
    
    if 'bed_number' in record:
        bed_number = record['bed_number']
        if pd.isna(bed_number):
            del record['bed_number']
            
    if 'area' in record:
        area = record['area']
        if pd.isna(area):
            del record['area']
    
    if 'thumbnail' in record:
        thumbnail = record['thumbnail']
        if not thumbnail.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            del record['thumbnail']
    
    if 'photos' in record:
        photos = record['photos']
        for photo in photos:
            if not photo.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                photos.remove(photo)
    
    
    return record

def populate_mongodb():
    db = get_default_mongo_db()

    # Load CSV files.
    buyers_data = pd.read_csv(buyers_csv)
    sellers_data = pd.read_csv(sellers_csv)
    properties_data = pd.read_csv(properties_csv)

    # Convert nested JSON fields in properties_data back to objects.
    if 'disponibility' in properties_data.columns:
        properties_data['disponibility'] = properties_data['disponibility'].apply(
            lambda x: json.loads(x) if pd.notna(x) else x
        )
    if 'photos' in properties_data.columns:
        properties_data['photos'] = properties_data['photos'].apply(
            lambda x: json.loads(x) if pd.notna(x) else x
        )
    
    # Convert nested JSON fields in buyers_data.
    if 'favourites' in buyers_data.columns:
        buyers_data['favourites'] = buyers_data['favourites'].apply(
            lambda x: json.loads(x) if pd.notna(x) else x
        )

    # Convert nested JSON fields in sellers_data.
    if 'property_on_sale' in sellers_data.columns:
        sellers_data['property_on_sale'] = sellers_data['property_on_sale'].apply(
            lambda x: json.loads(x) if pd.notna(x) else x
        )
    if 'sold_property' in sellers_data.columns:
        sellers_data['sold_property'] = sellers_data['sold_property'].apply(
            lambda x: json.loads(x) if pd.notna(x) else x
        )

    # Remove unnecessary columns from properties_data (e.g., latitude and longitude).
    properties_data = properties_data.drop(['latitude', 'longitude'], axis=1, errors='ignore')

    # Convert DataFrames to lists of dictionaries.
    buyers_records = buyers_data.to_dict(orient='records')
    sellers_records = sellers_data.to_dict(orient='records')
    properties_records = properties_data.to_dict(orient='records')

    # Clean records by removing 'description' fields that are not valid.
    buyers_records = [clean_record(record) for record in buyers_records]
    sellers_records = [clean_record(record) for record in sellers_records]
    properties_records = [clean_record(record) for record in properties_records]

    # Convert all _id fields (both top-level and embedded) from strings to ObjectId.
    buyers_records = [convert_ids(record) for record in buyers_records]
    sellers_records = [convert_ids(record) for record in sellers_records]
    properties_records = [convert_ids(record) for record in properties_records]

    # Insert data into the respective MongoDB collections.
    db[BUYER_COLLECTION].insert_many(buyers_records)
    db[SELLER_COLLECTION].insert_many(sellers_records)
    db[PROPERTY_COLLECTION].insert_many(properties_records)

    print("Data inserted successfully into MongoDB.")

# Function to clear MongoDB collections
def clear_mongodb():
    db = get_default_mongo_db()

    db[BUYER_COLLECTION].delete_many({})
    db[SELLER_COLLECTION].delete_many({})
    db[PROPERTY_COLLECTION].delete_many({})

    print("All collections cleared successfully.")

# Function to verify inserted data
def verify_mongodb_data():
    db = get_default_mongo_db()

    buyer_sample = db[BUYER_COLLECTION].find_one()
    seller_sample = db[SELLER_COLLECTION].find_one()
    property_sample = db[PROPERTY_COLLECTION].find_one()

    print("Sample Buyer Data:", json.dumps(buyer_sample, indent=4, default=str))
    print("Sample Seller Data:", json.dumps(seller_sample, indent=4, default=str))
    print("Sample Property Data:", json.dumps(property_sample, indent=4, default=str))

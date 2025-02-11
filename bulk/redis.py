import redis
import json
import pandas as pd
from setup.redis_setup.redis_setup import get_redis_client

def populate_redis_db(seller_csv_path ='bulk/files/Redis/reservations_seller.csv', buyer_csv_path = 'bulk/files/Redis/reservations_buyer.csv'):
    r = get_redis_client()

    # Load data from CSV files
    seller_data = pd.read_csv(seller_csv_path)
    buyer_data = pd.read_csv(buyer_csv_path)

    # Populate seller-side reservations
    for _, row in seller_data.iterrows():
        key = row['redis_key']
        reservations = json.loads(row['reservations'])
        r.set(key, json.dumps(reservations))

    # Populate buyer-side reservations
    for _, row in buyer_data.iterrows():
        key = row['redis_key']
        reservations = json.loads(row['reservations'])
        r.set(key, json.dumps(reservations))

    print("Database populated successfully.")

def reset_redis_db():
    r = get_redis_client()

    # Remove all keys related to reservations
    keys_to_delete = r.keys('property_on_sale_id:*:reservations') + r.keys('buyer_id:*:reservations')
    for key in keys_to_delete:
        r.delete(key)

    print("Database cleared successfully.")

def verify_redis_data():
    r = get_redis_client()

    # Verify a few random keys to ensure data is present
    seller_keys = r.keys('property_on_sale_id:*:reservations*')
    buyer_keys = r.keys('buyer_id:*:reservations*')
    

    if not seller_keys or not buyer_keys:
        print("Verification failed: no data found.")
        return

    # Check sample keys for data integrity
    seller_sample = r.get(seller_keys[0])
    buyer_sample = r.get(buyer_keys[0])

    print("Sample seller data:", json.loads(seller_sample))
    print("Sample buyer data:", json.loads(buyer_sample))
"""
Seed Data Script
Populates Redis with sample data for users, products, and orders tables.
"""

import os
import sys
from dotenv import load_dotenv
import redis

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

# Sample Users
USERS = [
    {"id": "1", "name": "Alice Johnson", "email": "alice@example.com", "role": "admin", "created": "2024-01-15"},
    {"id": "2", "name": "Bob Smith", "email": "bob@example.com", "role": "developer", "created": "2024-02-20"},
    {"id": "3", "name": "Carol Williams", "email": "carol@example.com", "role": "analyst", "created": "2024-03-10"},
    {"id": "4", "name": "David Brown", "email": "david@example.com", "role": "developer", "created": "2024-04-05"},
    {"id": "5", "name": "Eve Davis", "email": "eve@example.com", "role": "manager", "created": "2024-05-12"},
]

# Sample Products
PRODUCTS = [
    {"id": "1", "name": "Laptop Pro", "price": "1299.99", "category": "electronics", "stock": "50"},
    {"id": "2", "name": "Wireless Mouse", "price": "49.99", "category": "accessories", "stock": "200"},
    {"id": "3", "name": "USB-C Hub", "price": "79.99", "category": "accessories", "stock": "150"},
    {"id": "4", "name": "Monitor 27\"", "price": "399.99", "category": "electronics", "stock": "75"},
    {"id": "5", "name": "Mechanical Keyboard", "price": "129.99", "category": "accessories", "stock": "100"},
]

# Sample Orders
ORDERS = [
    {"id": "1", "user_id": "1", "product_id": "1", "quantity": "1", "status": "completed", "order_date": "2024-06-01"},
    {"id": "2", "user_id": "2", "product_id": "2", "quantity": "2", "status": "shipped", "order_date": "2024-06-15"},
    {"id": "3", "user_id": "3", "product_id": "4", "quantity": "1", "status": "processing", "order_date": "2024-06-20"},
    {"id": "4", "user_id": "1", "product_id": "3", "quantity": "3", "status": "completed", "order_date": "2024-06-25"},
    {"id": "5", "user_id": "5", "product_id": "5", "quantity": "1", "status": "pending", "order_date": "2024-06-28"},
]


def seed_data():
    """Populate Redis with sample data."""
    print("[SEED] Seeding Redis with sample data...")
    
    # Check connection
    try:
        redis_client.ping()
        print("[OK] Connected to Redis")
    except redis.ConnectionError as e:
        print(f"[ERROR] Failed to connect to Redis: {e}")
        return
    
    # Seed users
    print("\n[USERS] Adding users...")
    for user in USERS:
        key = f"user:{user['id']}"
        redis_client.hset(key, mapping=user)
        print(f"   Added {key}: {user['name']}")
    
    # Seed products
    print("\n[PRODUCTS] Adding products...")
    for product in PRODUCTS:
        key = f"product:{product['id']}"
        redis_client.hset(key, mapping=product)
        print(f"   Added {key}: {product['name']}")
    
    # Seed orders
    print("\n[ORDERS] Adding orders...")
    for order in ORDERS:
        key = f"order:{order['id']}"
        redis_client.hset(key, mapping=order)
        print(f"   Added {key}: Order #{order['id']}")
    
    print("\n[DONE] Seeding complete!")
    print(f"   Total keys created: {len(USERS) + len(PRODUCTS) + len(ORDERS)}")


if __name__ == "__main__":
    seed_data()

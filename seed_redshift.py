"""
Seed Data Script for Redshift/Postgres
Creates and populates users, products, and orders tables.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Connection configuration
DB_HOST = os.getenv("REDSHIFT_HOST", "localhost")
DB_PORT = int(os.getenv("REDSHIFT_PORT", 5439))
DB_NAME = os.getenv("REDSHIFT_DATABASE", "dev")
DB_USER = os.getenv("REDSHIFT_USER", "awsuser")
DB_PASS = os.getenv("REDSHIFT_PASSWORD", "")

# Determine driver (redshift+redshift_connector or postgresql+psycopg2)
if DB_HOST == "localhost" and DB_PORT == 5432:
    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    engine_url = f"redshift+redshift_connector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(engine_url)

def seed_data():
    print(f"[SEED] Connecting to {DB_HOST}:{DB_PORT}...")
    
    try:
        with engine.connect() as conn:
            # Drop existing tables
            print("[SEED] Dropping existing tables...")
            conn.execute(text("DROP TABLE IF EXISTS orders CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS products CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.commit()

            # Create Users table
            print("[SEED] Creating users table...")
            conn.execute(text("""
                CREATE TABLE users (
                    id INT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    role VARCHAR(50),
                    created_at DATE
                )
            """))

            # Create Products table
            print("[SEED] Creating products table...")
            conn.execute(text("""
                CREATE TABLE products (
                    id INT PRIMARY KEY,
                    name VARCHAR(100),
                    price DECIMAL(10, 2),
                    category VARCHAR(50),
                    stock INT
                )
            """))

            # Create Orders table
            print("[SEED] Creating orders table...")
            conn.execute(text("""
                CREATE TABLE orders (
                    id INT PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    product_id INT REFERENCES products(id),
                    quantity INT,
                    status VARCHAR(50),
                    order_date DATE
                )
            """))
            conn.commit()

            # Insert Sample Data
            print("[SEED] Inserting sample data...")
            
            # Users
            users_data = [
                (1, "Alice Johnson", "alice@example.com", "admin", "2024-01-15"),
                (2, "Bob Smith", "bob@example.com", "developer", "2024-02-20"),
                (3, "Carol Williams", "carol@example.com", "analyst", "2024-03-10"),
                (4, "David Brown", "david@example.com", "developer", "2024-04-05"),
                (5, "Eve Davis", "eve@example.com", "manager", "2024-05-12"),
            ]
            for u in users_data:
                conn.execute(text("INSERT INTO users VALUES (:id, :name, :email, :role, :created_at)"), 
                             {"id": u[0], "name": u[1], "email": u[2], "role": u[3], "created_at": u[4]})

            # Products
            products_data = [
                (1, "Laptop Pro", 1299.99, "electronics", 50),
                (2, "Wireless Mouse", 49.99, "accessories", 200),
                (3, "USB-C Hub", 79.99, "accessories", 150),
                (4, "Monitor 27\"", 399.99, "electronics", 75),
                (5, "Mechanical Keyboard", 129.99, "accessories", 100),
            ]
            for p in products_data:
                conn.execute(text("INSERT INTO products VALUES (:id, :name, :price, :category, :stock)"),
                             {"id": p[0], "name": p[1], "price": p[2], "category": p[3], "stock": p[4]})

            # Orders
            orders_data = [
                (1, 1, 1, 1, "completed", "2024-06-01"),
                (2, 2, 2, 2, "shipped", "2024-06-15"),
                (3, 3, 4, 1, "processing", "2024-06-20"),
                (4, 1, 3, 3, "completed", "2024-06-25"),
                (5, 5, 5, 1, "pending", "2024-06-28"),
            ]
            for o in orders_data:
                conn.execute(text("INSERT INTO orders VALUES (:id, :user_id, :product_id, :quantity, :status, :order_date)"),
                             {"id": o[0], "user_id": o[1], "product_id": o[2], "quantity": o[3], "status": o[4], "order_date": o[5]})
            
            conn.commit()
            print("[DONE] Seeding complete!")

    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")

if __name__ == "__main__":
    seed_data()

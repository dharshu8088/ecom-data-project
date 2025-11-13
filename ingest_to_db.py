"""
Read CSV files and insert data into SQLite database.
Creates ecom.db with tables: customers, products, orders, order_items, reviews.
"""

import csv
import sqlite3
import os
from datetime import datetime


def create_database(db_name='ecom.db'):
    """Create SQLite database and tables."""
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Removed existing {db_name}")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            date_joined DATE
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price REAL NOT NULL,
            cost REAL,
            stock_quantity INTEGER,
            brand TEXT,
            sku TEXT UNIQUE,
            created_at DATE
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT,
            shipping_address TEXT,
            shipping_city TEXT,
            shipping_state TEXT,
            shipping_zip TEXT,
            shipping_cost REAL,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    # Create reviews table
    cursor.execute('''
        CREATE TABLE reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            review_date DATE,
            verified_purchase BOOLEAN,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX idx_orders_customer_id ON orders(customer_id)')
    cursor.execute('CREATE INDEX idx_orders_order_date ON orders(order_date)')
    cursor.execute('CREATE INDEX idx_order_items_order_id ON order_items(order_id)')
    cursor.execute('CREATE INDEX idx_order_items_product_id ON order_items(product_id)')
    cursor.execute('CREATE INDEX idx_reviews_product_id ON reviews(product_id)')
    cursor.execute('CREATE INDEX idx_reviews_customer_id ON reviews(customer_id)')
    cursor.execute('CREATE INDEX idx_products_category ON products(category)')
    
    conn.commit()
    print(f"✓ Created database {db_name} with tables and indexes")
    
    return conn, cursor


def insert_customers(cursor, filename='customers.csv'):
    """Insert customers from CSV."""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        customers = []
        
        for row in reader:
            customers.append((
                int(row['customer_id']),
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'],
                row['address'],
                row['city'],
                row['state'],
                row['zip_code'],
                row['country'],
                row['date_joined']
            ))
        
        cursor.executemany('''
            INSERT INTO customers 
            (customer_id, first_name, last_name, email, phone, address, 
             city, state, zip_code, country, date_joined)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', customers)
    
    print(f"✓ Inserted {len(customers)} customers")


def insert_products(cursor, filename='products.csv'):
    """Insert products from CSV."""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        products = []
        
        for row in reader:
            products.append((
                int(row['product_id']),
                row['name'],
                row['description'],
                row['category'],
                float(row['price']),
                float(row['cost']),
                int(row['stock_quantity']),
                row['brand'],
                row['sku'],
                row['created_at']
            ))
        
        cursor.executemany('''
            INSERT INTO products 
            (product_id, name, description, category, price, cost, 
             stock_quantity, brand, sku, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
    
    print(f"✓ Inserted {len(products)} products")


def insert_orders(cursor, filename='orders.csv'):
    """Insert orders from CSV."""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        orders = []
        
        for row in reader:
            orders.append((
                int(row['order_id']),
                int(row['customer_id']),
                row['order_date'],
                row['status'],
                row['shipping_address'],
                row['shipping_city'],
                row['shipping_state'],
                row['shipping_zip'],
                float(row['shipping_cost']),
                float(row['total_amount'])
            ))
        
        cursor.executemany('''
            INSERT INTO orders 
            (order_id, customer_id, order_date, status, shipping_address, 
             shipping_city, shipping_state, shipping_zip, shipping_cost, total_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders)
    
    print(f"✓ Inserted {len(orders)} orders")


def insert_order_items(cursor, filename='order_items.csv'):
    """Insert order items from CSV."""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        order_items = []
        
        for row in reader:
            order_items.append((
                int(row['order_item_id']),
                int(row['order_id']),
                int(row['product_id']),
                int(row['quantity']),
                float(row['unit_price']),
                float(row['subtotal'])
            ))
        
        cursor.executemany('''
            INSERT INTO order_items 
            (order_item_id, order_id, product_id, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', order_items)
    
    print(f"✓ Inserted {len(order_items)} order items")


def insert_reviews(cursor, filename='reviews.csv'):
    """Insert reviews from CSV."""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reviews = []
        
        for row in reader:
            # Convert boolean string to integer (SQLite uses 0/1 for booleans)
            verified = 1 if row['verified_purchase'].lower() == 'true' else 0
            
            reviews.append((
                int(row['review_id']),
                int(row['product_id']),
                int(row['customer_id']),
                int(row['rating']),
                row['review_text'],
                row['review_date'],
                verified
            ))
        
        cursor.executemany('''
            INSERT INTO reviews 
            (review_id, product_id, customer_id, rating, review_text, 
             review_date, verified_purchase)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', reviews)
    
    print(f"✓ Inserted {len(reviews)} reviews")


def verify_data(cursor):
    """Verify data was inserted correctly."""
    print("\nVerifying data...")
    
    tables = ['customers', 'products', 'orders', 'order_items', 'reviews']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} records")
    
    # Check foreign key constraints
    cursor.execute('''
        SELECT COUNT(*) FROM orders o
        WHERE NOT EXISTS (
            SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
        )
    ''')
    orphan_orders = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM order_items oi
        WHERE NOT EXISTS (
            SELECT 1 FROM orders o WHERE o.order_id = oi.order_id
        )
    ''')
    orphan_items = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM order_items oi
        WHERE NOT EXISTS (
            SELECT 1 FROM products p WHERE p.product_id = oi.product_id
        )
    ''')
    invalid_products = cursor.fetchone()[0]
    
    if orphan_orders == 0 and orphan_items == 0 and invalid_products == 0:
        print("✓ All foreign key constraints are valid")
    else:
        print(f"⚠ Warning: Found {orphan_orders} orphan orders, "
              f"{orphan_items} orphan items, {invalid_products} invalid products")


def main():
    """Main function to ingest all CSV files into SQLite database."""
    print("=" * 60)
    print("CSV to SQLite Database Ingestion")
    print("=" * 60)
    print()
    
    # Check if CSV files exist
    csv_files = ['customers.csv', 'products.csv', 'orders.csv', 
                 'order_items.csv', 'reviews.csv']
    
    missing_files = [f for f in csv_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing CSV files: {', '.join(missing_files)}")
        print("Please run generate_data.py first to create the CSV files.")
        return
    
    # Create database and tables
    conn, cursor = create_database('ecom.db')
    
    try:
        # Insert data in order (respecting foreign key constraints)
        print("\nInserting data...")
        insert_customers(cursor)
        insert_products(cursor)
        insert_orders(cursor)
        insert_order_items(cursor)
        insert_reviews(cursor)
        
        # Commit all changes
        conn.commit()
        print("\n✓ All data inserted successfully")
        
        # Verify data
        verify_data(cursor)
        
        print("\n" + "=" * 60)
        print("Ingestion complete!")
        print("=" * 60)
        print(f"\nDatabase: ecom.db")
        print(f"Size: {os.path.getsize('ecom.db') / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error occurred: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()


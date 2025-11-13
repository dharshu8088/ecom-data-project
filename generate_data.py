"""
Generate synthetic e-commerce data using Faker.
Creates 5 CSV files: customers, products, orders, order_items, and reviews.
"""

import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Configuration
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 2000
NUM_REVIEWS = 1500

# Set seed for reproducibility
Faker.seed(42)
random.seed(42)


def generate_customers(filename='customers.csv'):
    """Generate customer data."""
    print(f"Generating {NUM_CUSTOMERS} customers...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['customer_id', 'first_name', 'last_name', 'email', 
                     'phone', 'address', 'city', 'state', 'zip_code', 'country', 
                     'date_joined']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, NUM_CUSTOMERS + 1):
            writer.writerow({
                'customer_id': i,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.unique.email(),
                'phone': fake.phone_number(),
                'address': fake.street_address(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip_code': fake.zipcode(),
                'country': fake.country(),
                'date_joined': fake.date_between(start_date='-2y', end_date='today').isoformat()
            })
    
    print(f"✓ Created {filename}")


def generate_products(filename='products.csv'):
    """Generate product data."""
    print(f"Generating {NUM_PRODUCTS} products...")
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors', 
                  'Books', 'Toys & Games', 'Health & Beauty', 'Automotive', 
                  'Food & Beverages', 'Office Supplies']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_id', 'name', 'description', 'category', 'price', 
                     'cost', 'stock_quantity', 'brand', 'sku', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, NUM_PRODUCTS + 1):
            price = round(random.uniform(10, 500), 2)
            cost = round(price * random.uniform(0.3, 0.7), 2)
            
            writer.writerow({
                'product_id': i,
                'name': fake.catch_phrase(),
                'description': fake.text(max_nb_chars=200),
                'category': random.choice(categories),
                'price': price,
                'cost': cost,
                'stock_quantity': random.randint(0, 1000),
                'brand': fake.company(),
                'sku': fake.unique.bothify(text='SKU-####-????'),
                'created_at': fake.date_between(start_date='-1y', end_date='today').isoformat()
            })
    
    print(f"✓ Created {filename}")


def generate_orders(filename='orders.csv', customer_ids=None):
    """Generate order data."""
    print(f"Generating {NUM_ORDERS} orders...")
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['order_id', 'customer_id', 'order_date', 'status', 
                     'shipping_address', 'shipping_city', 'shipping_state', 
                     'shipping_zip', 'shipping_cost', 'total_amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, NUM_ORDERS + 1):
            order_date = fake.date_between(start_date='-1y', end_date='today')
            
            writer.writerow({
                'order_id': i,
                'customer_id': random.choice(customer_ids),
                'order_date': order_date.isoformat(),
                'status': random.choice(statuses),
                'shipping_address': fake.street_address(),
                'shipping_city': fake.city(),
                'shipping_state': fake.state_abbr(),
                'shipping_zip': fake.zipcode(),
                'shipping_cost': round(random.uniform(5, 25), 2),
                'total_amount': 0  # Will be calculated from order_items
            })
    
    print(f"✓ Created {filename}")


def generate_order_items(filename='order_items.csv', order_ids=None, product_ids=None):
    """Generate order items data."""
    print(f"Generating order items...")
    
    order_items = []
    order_totals = {}  # Track totals for each order
    
    # Generate multiple items per order
    for order_id in order_ids:
        num_items = random.randint(1, 5)  # 1-5 items per order
        selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
        
        for product_id in selected_products:
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(10, 500), 2)
            subtotal = round(unit_price * quantity, 2)
            
            order_items.append({
                'order_item_id': len(order_items) + 1,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal
            })
            
            # Track order totals
            if order_id not in order_totals:
                order_totals[order_id] = 0
            order_totals[order_id] += subtotal
    
    # Write order items
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['order_item_id', 'order_id', 'product_id', 'quantity', 
                     'unit_price', 'subtotal']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in order_items:
            writer.writerow(item)
    
    print(f"✓ Created {filename} with {len(order_items)} items")
    
    # Update order totals in orders.csv
    update_order_totals('orders.csv', order_totals)
    
    return order_totals


def update_order_totals(filename, order_totals):
    """Update total_amount in orders.csv based on order_items."""
    print("Updating order totals...")
    
    # Read existing orders
    orders = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            order_id = int(row['order_id'])
            if order_id in order_totals:
                # Add shipping cost to total
                shipping_cost = float(row['shipping_cost'])
                row['total_amount'] = round(order_totals[order_id] + shipping_cost, 2)
            orders.append(row)
    
    # Write updated orders
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['order_id', 'customer_id', 'order_date', 'status', 
                     'shipping_address', 'shipping_city', 'shipping_state', 
                     'shipping_zip', 'shipping_cost', 'total_amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
    
    print("✓ Updated order totals")


def generate_reviews(filename='reviews.csv', customer_ids=None, product_ids=None):
    """Generate review data."""
    print(f"Generating {NUM_REVIEWS} reviews...")
    
    ratings = [1, 2, 3, 4, 5]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['review_id', 'product_id', 'customer_id', 'rating', 
                     'review_text', 'review_date', 'verified_purchase']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, NUM_REVIEWS + 1):
            writer.writerow({
                'review_id': i,
                'product_id': random.choice(product_ids),
                'customer_id': random.choice(customer_ids),
                'rating': random.choice(ratings),
                'review_text': fake.text(max_nb_chars=500),
                'review_date': fake.date_between(start_date='-1y', end_date='today').isoformat(),
                'verified_purchase': random.choice([True, False])
            })
    
    print(f"✓ Created {filename}")


def main():
    """Main function to generate all CSV files."""
    print("=" * 60)
    print("Generating Synthetic E-commerce Data")
    print("=" * 60)
    print()
    
    # Generate customers
    generate_customers('customers.csv')
    customer_ids = list(range(1, NUM_CUSTOMERS + 1))
    
    # Generate products
    generate_products('products.csv')
    product_ids = list(range(1, NUM_PRODUCTS + 1))
    
    # Generate orders
    generate_orders('orders.csv', customer_ids)
    order_ids = list(range(1, NUM_ORDERS + 1))
    
    # Generate order items (this also updates order totals)
    generate_order_items('order_items.csv', order_ids, product_ids)
    
    # Generate reviews
    generate_reviews('reviews.csv', customer_ids, product_ids)
    
    print()
    print("=" * 60)
    print("Data generation complete!")
    print("=" * 60)
    print(f"\nGenerated files:")
    print(f"  - customers.csv ({NUM_CUSTOMERS} records)")
    print(f"  - products.csv ({NUM_PRODUCTS} records)")
    print(f"  - orders.csv ({NUM_ORDERS} records)")
    print(f"  - order_items.csv (variable records)")
    print(f"  - reviews.csv ({NUM_REVIEWS} records)")


if __name__ == '__main__':
    main()


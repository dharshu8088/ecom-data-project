📦 E-Commerce Data Engineering Project
Synthetic Data Generation + SQLite Database Ingestion
This project generates a complete E-Commerce dataset and loads it into a SQLite database (ecom.db) using Python.
It includes customers, products, orders, order items, and reviews.
🚀 Features
Generates synthetic CSV files
Creates SQLite database automatically
Inserts all CSV data with foreign key relationships
Prints ingestion summary
Simple to run on any machine
📁 Project Structure
ecom-data-project/
│
├── generate_data.py
├── ingest_to_db.py
│
├── customers.csv
├── products.csv
├── orders.csv
├── order_items.csv
├── reviews.csv
│
├── ecom.db
│
└── requirements.txt
🛠️ 1. Install Dependencies
Run in terminal:
pip install -r requirements.txt
🧪 2. Generate CSV Data
python3 generate_data.py
Creates:
customers.csv
products.csv
orders.csv
order_items.csv
reviews.csv
🗄️ 3. Ingest Into SQLite Database
python3 ingest_to_db.py
This will:
Create ecom.db
Create all tables
Insert all CSV data
Show success message
📊 4. Verify the Database
Option A — DB Browser for SQLite
Download from sqlitebrowser.org → Open ecom.db
Option B — Python
import sqlite3
conn = sqlite3.connect("ecom.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM customers")
print(cursor.fetchone())
📐 ER Diagram (Conceptual)
 Customers (1) ----< Orders (Many)
 Orders (1) ----< Order_Items (Many)
 Customers (1) ----< Reviews (Many)
 Products (1) ----< Order_Items (Many)
 Products (1) ----< Reviews (Many)
📘 Requirements
pandas
faker
👨‍💻 Author
Dharshini K M
E-Commerce Data Engineering Project

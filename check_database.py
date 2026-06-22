import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("food_wastage.db")

# List of tables
tables = ["providers", "receivers", "food_listings", "claims"]

# Display first 5 rows from each table
for table in tables:
    print("\n" + "=" * 60)
    print(f"TABLE: {table.upper()}")
    print("=" * 60)

    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
    print(df)

conn.close()
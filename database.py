import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("food_wastage.db")

# Read CSV files
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

# Store data in SQLite tables
providers.to_sql("providers", conn, if_exists="replace", index=False)
receivers.to_sql("receivers", conn, if_exists="replace", index=False)
food.to_sql("food_listings", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)

print("Database created successfully!")

conn.close()
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("food_wastage.db")
print("\nQUERY 1: Number of Food Providers in Each City")
print("-" * 50)

query1 = """
SELECT City, COUNT(*) AS Total_Providers
FROM providers
GROUP BY City
ORDER BY Total_Providers DESC;
"""

df1 = pd.read_sql_query(query1, conn)
print(df1)
print("\nQUERY 2: Number of Food Receivers in Each City")
print("-" * 50)

query2 = """
SELECT City, COUNT(*) AS Total_Receivers
FROM receivers
GROUP BY City
ORDER BY Total_Receivers DESC;
"""

df2 = pd.read_sql_query(query2, conn)
print(df2)
print("\nQUERY 3: Food Provider Type Contribution")
print("-" * 50)

query3 = """
SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;
"""

df3 = pd.read_sql_query(query3, conn)
print(df3)
print("\nQUERY 4: Contact Details of Providers in New Carol")
print("-" * 50)

query4 = """
SELECT Name, Contact
FROM providers
WHERE City = 'New Carol';
"""

df4 = pd.read_sql_query(query4, conn)
print(df4)
print("\nQUERY 5: Receivers Who Claimed the Most Food")
print("-" * 50)

query5 = """
SELECT
    r.Name,
    COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN receivers r
ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name
ORDER BY Total_Claims DESC;
"""

df5 = pd.read_sql_query(query5, conn)
print(df5)
print("\nQUERY 6: Total Quantity of Food Available")
print("-" * 50)

query6 = """
SELECT SUM(Quantity) AS Total_Food_Quantity
FROM food_listings;
"""

df6 = pd.read_sql_query(query6, conn)
print(df6)
print("\nQUERY 7: City with Highest Food Listings")
print("-" * 50)

query7 = """
SELECT Location AS City,
COUNT(*) AS Total_Listings
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;
"""

df7 = pd.read_sql_query(query7, conn)
print(df7)
print("\nQUERY 8: Most Common Food Types")
print("-" * 50)

query8 = """
SELECT Food_Type,
COUNT(*) AS Total_Items
FROM food_listings
GROUP BY Food_Type
ORDER BY Total_Items DESC;
"""

df8 = pd.read_sql_query(query8, conn)
print(df8)
print("\nQUERY 9: Claims for Each Food Item")
print("-" * 50)

query9 = """
SELECT
f.Food_Name,
COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings f
LEFT JOIN claims c
ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY Total_Claims DESC;
"""

df9 = pd.read_sql_query(query9, conn)
print(df9)
print("\nQUERY 10: Provider with Highest Successful Claims")
print("-" * 50)

query10 = """
SELECT
p.Name,
COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_listings f
ON p.Provider_ID = f.Provider_ID
JOIN claims c
ON f.Food_ID = c.Food_ID
WHERE c.Status='Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC;
"""

df10 = pd.read_sql_query(query10, conn)
print(df10)
print("\nQUERY 11: Claim Status Percentage")
print("-" * 50)

query11 = """
SELECT
Status,
COUNT(*) AS Total_Claims,
ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims
GROUP BY Status;
"""

df11 = pd.read_sql_query(query11, conn)
print(df11)
print("\nQUERY 12: Average Quantity Claimed Per Receiver")
print("-" * 50)

query12 = """
SELECT
ROUND(AVG(Quantity),2) AS Average_Quantity
FROM food_listings
WHERE Food_ID IN
(
SELECT Food_ID
FROM claims
);
"""

df12 = pd.read_sql_query(query12, conn)
print(df12)
print("\nQUERY 13: Most Claimed Meal Type")
print("-" * 50)

query13 = """
SELECT
Meal_Type,
COUNT(*) AS Total_Claims
FROM food_listings f
JOIN claims c
ON f.Food_ID = c.Food_ID
GROUP BY Meal_Type
ORDER BY Total_Claims DESC;
"""

df13 = pd.read_sql_query(query13, conn)
print(df13)
print("\nQUERY 14: Quantity Donated by Each Provider")
print("-" * 50)

query14 = """
SELECT
p.Name,
SUM(f.Quantity) AS Total_Donated
FROM providers p
JOIN food_listings f
ON p.Provider_ID=f.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC
LIMIT 10;
"""

df14 = pd.read_sql_query(query14, conn)
print(df14)
print("\nQUERY 15: Top Cities by Food Quantity")
print("-" * 50)

query15 = """
SELECT
Location,
SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Location
ORDER BY Total_Quantity DESC
LIMIT 10;
"""

df15 = pd.read_sql_query(query15, conn)
print(df15)
conn.close()
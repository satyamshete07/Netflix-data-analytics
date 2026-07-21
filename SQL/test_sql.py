import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("netflix.db")

query = """
SELECT * FROM netflix
WHERE type = 'Movie'
"""

df = pd.read_sql(query, conn)

# 1. Content Type Distribution
print("\n📊 Content Type Distribution")
query1 = """
SELECT type, COUNT(*) as total
FROM netflix
GROUP BY type;
"""
df1 = pd.read_sql(query1, conn)
print(df1)

# 2. Growth Over Time
print("\n📈 Growth Over Time")
query2 = """
SELECT 
    SUBSTR(date_added, -4) AS year_added,
    COUNT(*) as total
FROM netflix
WHERE date_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;
"""
df2 = pd.read_sql(query2, conn)
print(df2)

# 3. Top Countries
print("\n🌍 Top Countries")
query3 = """
SELECT country, COUNT(*) as total
FROM netflix
GROUP BY country
ORDER BY total DESC
LIMIT 10;
"""
df3 = pd.read_sql(query3, conn)
print(df3)

# 4. Top Genres
print("\n🎭 Top Genres")
query4 = """
SELECT listed_in, COUNT(*) as total
FROM netflix
GROUP BY listed_in
ORDER BY total DESC
LIMIT 10;
"""
df4 = pd.read_sql(query4, conn)
print(df4)

# 5. Ratings Distribution
print("\n🔞 Ratings Distribution")
query5 = """
SELECT rating, COUNT(*) as total
FROM netflix
GROUP BY rating
ORDER BY total DESC;
"""
df5 = pd.read_sql(query5, conn)
print(df5)


# Close connection
conn.close()


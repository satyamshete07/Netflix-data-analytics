import pandas as pd
import sqlite3

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Create connection
conn = sqlite3.connect("netflix.db")

# Save table
df.to_sql("netflix", conn, if_exists="replace", index=False)

print("✅ Database created successfully!")

conn.close()
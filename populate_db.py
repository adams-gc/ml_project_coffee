import sqlite3
import pandas as pd

# Load the coffee data
df = pd.read_csv('coffee_data.csv')

# Connect to the SQLite database
conn = sqlite3.connect('coffee_recommendations.db')

# Insert coffee data into the database
df.to_sql('coffee', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

import sqlite3

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('coffee_recommendations.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a table to store user feedback
def create_feedback_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roast_level TEXT,
            acidity TEXT,
            drink_type TEXT,
            description TEXT,
            drink_time TEXT,
            strength TEXT,
            recommendation_id INTEGER,
            feedback_value TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table
create_feedback_table()

import sqlite3

def create_database():
    conn = sqlite3.connect("data/chargers.db")
    cursor = conn.cursor()  # Create a cursor object so I can run SQL commands using Python

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chargers ( 
        id INTEGER PRIMARY KEY,
        title TEXT,
        address TEXT,
        latitude REAL,
        longitude REAL,
        is_free INTEGER,
        power_kw REAL,
        connector_type TEXT,
        last_updated TEXT
    )
    """)
    # NB: 'IF NOT EXISTS' ensures this code won’t fail if the table is already present

    conn.commit()
    conn.close()
    print("Database and table created")

if __name__ == "__main__":
    create_database()
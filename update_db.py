import sqlite3

conn = sqlite3.connect('search_history.db')
c = conn.cursor()

# Add timestamp column if it doesn't exist
try:
    c.execute("ALTER TABLE searches ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP")
except:
    print("Timestamp column may already exist.")

conn.commit()
conn.close()

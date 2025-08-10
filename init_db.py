import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('search_history.db')
cursor = conn.cursor()

# Create table with timestamp column
cursor.execute('''
CREATE TABLE IF NOT EXISTS searches (
    case_type TEXT,
    case_number TEXT,
    filing_year TEXT,
    timestamp TEXT
)
''')

conn.commit()
conn.close()

print("✅ Database and table created successfully with timestamp column.")


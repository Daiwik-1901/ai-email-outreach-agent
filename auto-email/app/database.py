import sqlite3
from datetime import datetime

def init_db():
    """Initialize the SQLite database and create the outreach table if it doesn't exist."""
    conn = sqlite3.connect('outreach.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS outreach
                 (id INTEGER PRIMARY KEY,
                  company TEXT,
                  email TEXT,
                  status TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def store_outreach(company: str, email: str, status: str):
    """Store an outreach attempt in the database."""
    conn = sqlite3.connect('outreach.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO outreach (company, email, status, timestamp) VALUES (?, ?, ?, ?)",
              (company, email, status, timestamp))
    conn.commit()
    conn.close()

def fetch_history():
    """Fetch all outreach history from the database."""
    conn = sqlite3.connect('outreach.db')
    c = conn.cursor()
    c.execute("SELECT * FROM outreach")
    rows = c.fetchall()
    conn.close()
    return rows
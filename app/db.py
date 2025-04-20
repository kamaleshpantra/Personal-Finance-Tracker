import sqlite3
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = sqlite3.connect('finance.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_db():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      type TEXT NOT NULL,
                      category TEXT NOT NULL,
                      amount REAL NOT NULL,
                      currency TEXT NOT NULL,
                      date TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS budgets
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      category TEXT NOT NULL,
                      amount REAL NOT NULL,
                      month TEXT NOT NULL)''')
        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()
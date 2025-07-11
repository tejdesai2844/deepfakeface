# db.py
import streamlit as st
import sqlite3
import threading
import time

class DatabaseManager:
    """A thread-safe manager for the SQLite database."""
    def __init__(self, db_path):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize the database and create tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path, timeout=20.0) as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY, name TEXT, city TEXT, email TEXT UNIQUE, mobile TEXT, password TEXT)''')
                conn.commit()
        except Exception as e:
            # Use st.exception to show a full traceback in the app for debugging
            st.exception(f"Database initialization error: {e}")
    
    def get_connection(self):
        """Get a database connection with proper timeout and error handling."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            conn.execute("PRAGMA journal_mode=WAL")  # Use WAL mode for better concurrency
            return conn
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=None, max_retries=3):
        """
        Execute a database query with error handling and a retry mechanism.
        fetch can be 'one', 'all', or None.
        """
        for attempt in range(max_retries):
            with self._lock:
                try:
                    conn = self.get_connection()
                    if conn is None: return None
                    
                    cursor = conn.cursor()
                    cursor.execute(query, params or ())
                    
                    if fetch == 'one':
                        result = cursor.fetchone()
                    elif fetch == 'all':
                        result = cursor.fetchall()
                    else:
                        conn.commit()
                        result = None
                    
                    conn.close()
                    return result
                    
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e).lower():
                        if attempt < max_retries - 1:
                            time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                            continue
                        else:
                            st.error("Database is temporarily busy. Please try again in a moment.")
                    else:
                        st.error(f"Database operation error: {e}")
                    return None
                except Exception as e:
                    st.error(f"Unexpected database error: {e}")
                    return None

# --- Initialize the database manager ---
db_manager = DatabaseManager('users.db')

# --- Helper functions for user operations ---
def view_all_users():
    """Get all users from the database."""
    return db_manager.execute_query("SELECT id, name, city, email, mobile FROM users", fetch='all')

def delete_user(email):
    """Delete a user by email."""
    db_manager.execute_query("DELETE FROM users WHERE email=?", (email,))

def insert_user(name, city, email, mobile, password):
    """Insert a new user into the database."""
    db_manager.execute_query(
        "INSERT INTO users (name, city, email, mobile, password) VALUES (?, ?, ?, ?, ?)",
        (name, city, email, mobile, password)
    )

def check_user_credentials(email, password):
    """Check if user credentials are valid and return user data."""
    result = db_manager.execute_query(
        "SELECT name, city, email, mobile FROM users WHERE email=? AND password=?", 
        (email, password), 
        fetch='one'
    )
    if result:
        # Return data as a dictionary
        return {'name': result[0], 'city': result[1], 'email': result[2], 'mobile': result[3]}
    return None


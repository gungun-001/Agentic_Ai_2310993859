"""
database.py – SQLite database management for FireReach users.
"""

import sqlite3
import bcrypt
import os

DB_PATH = "users.db"

def init_db():
    """Initialize the SQLite database and create the users table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user(name, email, company, role, password):
    """
    Create a new user with a hashed password.
    Returns (success: bool, message: str)
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, company, role, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, company, role, hashed))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, f"Database error: {e}"

def authenticate_user(email, password):
    """
    Verify user credentials.
    Returns (success: bool, user_info: dict or None)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, company, role, password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[5]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "company": user[3],
                    "role": user[4]
                }
        return False, None
    except Exception as e:
        print(f"Authentication error: {e}")
        return False, None

# Initialize the database when the module is loaded
init_db()

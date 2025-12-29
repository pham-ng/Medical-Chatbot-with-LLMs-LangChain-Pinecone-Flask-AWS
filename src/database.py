import sqlite3
import os
from datetime import datetime
from threading import Lock

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'chat_history.db')

# Thread-safe lock for database operations
db_lock = Lock()

def init_db():
    """Initialize the SQLite database with chat_logs table."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index on session_id for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_id ON chat_logs(session_id)
        ''')
        
        conn.commit()
        conn.close()
    print("✅ Database initialized successfully!")


def save_message(session_id, role, content):
    """
    Save a message to the database.
    
    Args:
        session_id (str): Unique session identifier
        role (str): Either 'user' or 'bot'
        content (str): The message content
    
    Returns:
        bool: True if successful, False otherwise
    """
    with db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_logs (session_id, role, content, timestamp)
                VALUES (?, ?, ?, datetime('now'))
            ''', (session_id, role, content))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            return False


def get_history(session_id):
    """
    Retrieve all messages for a specific session.
    
    Args:
        session_id (str): Unique session identifier
    
    Returns:
        list: List of dictionaries containing message data
    """
    with db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, session_id, role, content, timestamp
                FROM chat_logs
                WHERE session_id = ?
                ORDER BY timestamp ASC
            ''', (session_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert rows to list of dictionaries
            messages = [
                {
                    'id': row['id'],
                    'session_id': row['session_id'],
                    'role': row['role'],
                    'content': row['content'],
                    'timestamp': row['timestamp']
                }
                for row in rows
            ]
            
            return messages
        except Exception as e:
            print(f"❌ Error retrieving history: {e}")
            return []


def clear_history(session_id):
    """
    Clear all messages for a specific session.
    
    Args:
        session_id (str): Unique session identifier
    
    Returns:
        bool: True if successful, False otherwise
    """
    with db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM chat_logs WHERE session_id = ?', (session_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False

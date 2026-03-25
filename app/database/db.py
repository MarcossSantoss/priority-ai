"""Database connection and operations for the priority-ai application."""
import sqlite3


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect("database.db")


def create_table():
    """Create the tickets table if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        priority TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_ticket(title, description, priority):
    """Insert a new ticket into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets (title, description, priority)
    VALUES (?, ?, ?)
    """, (title, description, priority))

    conn.commit()
    conn.close()


def get_tickets():
    """Retrieve all tickets from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, description, priority FROM tickets")
    tickets = cursor.fetchall()

    conn.close()
    return tickets

import sqlite3


def get_connection():
    return sqlite3.connect("database.db")


def create_table():
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets (title, description, priority)
    VALUES (?, ?, ?)
    """, (title, description, priority))

    conn.commit()
    conn.close()


def get_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, description, priority FROM tickets")
    tickets = cursor.fetchall()

    conn.close()
    return tickets

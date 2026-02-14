import sqlite3

def get_connection():
    return sqlite3.connect("sahaaya.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Community Events Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            location TEXT,
            event_date TEXT,
            description TEXT,
            created TEXT
        )
    """)

    # Mood Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            mood TEXT,
            problems TEXT,
            severity INTEGER,
            note TEXT,
            area TEXT,
            time TEXT
        )
    """)

    # Volunteers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            area TEXT,
            age_group TEXT,
            skills TEXT,
            volunteering_type TEXT,
            mode TEXT,
            availability TEXT
        )
    """)

    # Recovery Stories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recovery_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            rating INTEGER,
            story TEXT,
            time TEXT,
            approved INTEGER DEFAULT 0,
            helpful INTEGER DEFAULT 0
        )
    """)

    # Comments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            comment TEXT
        )
    """)
        # Circle Posts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS circle_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            time TEXT
        )
    """)


    conn.commit()
    conn.close()

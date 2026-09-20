import sqlite3

def init_db():
    conn = sqlite3.connect("ja_assure.db")
    cursor = conn.cursor()

    # Shared content queue table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS content_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        platform TEXT NOT NULL,
        language TEXT NOT NULL,
        body_content TEXT NOT NULL,
        compliance_status TEXT DEFAULT 'pending',
        status TEXT DEFAULT 'pending_review',
        rejection_tag TEXT,
        human_notes TEXT
    )
    """)

    # Feedback loop memory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        rejection_tag TEXT NOT NULL,
        human_notes TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
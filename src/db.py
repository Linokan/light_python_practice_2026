import sqlite3
from pathlib import Path


DB_PATH = Path("data/app.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            relative_path TEXT UNIQUE,
            size INTEGER,
            modified_time REAL,
            extension TEXT,
            file_hash TEXT,
            exists_flag INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()
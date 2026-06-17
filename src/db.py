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


def save_files(files):
    conn = sqlite3.connect(DB_PATH)

    for file in files:
        conn.execute("""
            INSERT INTO files (
                relative_path,
                size,
                modified_time,
                extension,
                exists_flag
            )
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(relative_path) DO UPDATE SET
                size = excluded.size,
                modified_time = excluded.modified_time,
                extension = excluded.extension,
                exists_flag = 1
        """, (
            file["relative_path"],
            file["size"],
            file["modified_time"],
            file["extension"]
        ))

    conn.commit()
    conn.close()


def get_all_files():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        SELECT relative_path, size, extension
        FROM files
    """)

    result = cursor.fetchall()

    conn.close()

    return result
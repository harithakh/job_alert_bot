import sqlite3
import os

DATABASE = "data/jobs.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS job_listings(
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                title           TEXT NOT NULL,
                company         TEXT,
                location        TEXT,
                url             TEXT,
                posted_date     TEXT,
                category        TEXT,
                reference_no    TEXT UNIQUE
            )

        """)
        conn.commit()

def insert_job(title, company, location, url, posted_date, category, reference_no):
    try:
        with get_connection() as conn:
            conn.execute("""
                    INSERT OR IGNORE INTO  job_listings
                        (title, company, location, url, posted_date, category, reference_no) VALUES (?,?,?,?,?,?,?)""",
                        (title, company, location, url, posted_date, category, reference_no)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"DB eror: {e}")

def get_all_jobs():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM job_listings ORDER_BY posted_date DESC").fetchall()

def job_exists(reference_no, today):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM job_listings WHERE reference_no = ? AND posted_date = ?", (reference_no,today)).fetchone()
        return row is not None

import sqlite3
from datetime import datetime

conn = sqlite3.connect("narrative.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    timestamp TEXT,
    topic TEXT,
    count INTEGER
)
""")

conn.commit()


def save_signals(results):
    timestamp = datetime.now().isoformat()

    for topic, count in results.items():
        cursor.execute("""
        INSERT INTO signals (timestamp, topic, count)
        VALUES (?, ?, ?)
        """, (timestamp, topic, count))

    conn.commit()
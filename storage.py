import sqlite3
from datetime import datetime

conn = sqlite3.connect("narrative.db", check_same_thread=False)
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

    for topic, value in results.items():

        # # handle both int and dict safely
        # if isinstance(value, dict):
        #     count = value.get("count", 0)
        # else:
        count = value

        cursor.execute("""
        INSERT INTO signals (timestamp, topic, count)
        VALUES (?, ?, ?)
        """, (timestamp, topic, count))

    conn.commit()


def get_recent_signals(limit_runs=5):
    cursor.execute("""
    SELECT timestamp, topic, count
    FROM signals
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    data = {}

    for ts, topic, count in rows:
        if topic not in data:
            data[topic] = []

        if len(data[topic]) < limit_runs:
            data[topic].append((ts, count))

    return data
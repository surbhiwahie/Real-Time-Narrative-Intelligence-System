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

    for topic, count in results.items():
        cursor.execute("""
        INSERT INTO signals (timestamp, topic, count)
        VALUES (?, ?, ?)
        """, (timestamp, topic, count))

    conn.commit()


def get_recent_signals(limit_runs=5):
    """
    Returns last N runs aggregated per topic
    """

    cursor.execute("""
    SELECT topic, count, timestamp
    FROM signals
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    data = {}

    run_counter = {}

    for topic, count, ts in rows:
        if topic not in data:
            data[topic] = []

        if len(data[topic]) < limit_runs:
            data[topic].append(count)

    # convert to averages
    averages = {}
    for topic, values in data.items():
        averages[topic] = sum(values) / len(values)

    return averages
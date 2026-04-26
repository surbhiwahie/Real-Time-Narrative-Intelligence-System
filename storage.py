import sqlite3
from datetime import datetime

conn = sqlite3.connect("narrative.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    run_id TEXT,
    timestamp TEXT,
    topic TEXT,
    count INTEGER
)
""")

conn.commit()

import uuid

def save_signals(results):
    run_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    for topic, count in results.items():
        cursor.execute("""
        INSERT INTO signals (run_id, timestamp, topic, count)
        VALUES (?, ?, ?, ?)
        """, (run_id, timestamp, topic, count))

    conn.commit()


def get_recent_signals(limit_runs=5):
    cursor.execute("""
    SELECT run_id, timestamp, topic, count
    FROM signals
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    runs = {}
    ordered_runs = []

    for run_id, ts, topic, count in rows:
        if run_id not in runs:
            runs[run_id] = {
                "timestamp": ts,
                "data": {}
            }
            ordered_runs.append(run_id)

        runs[run_id]["data"][topic] = count

        if len(ordered_runs) >= limit_runs:
            break

    return [runs[rid] for rid in ordered_runs]
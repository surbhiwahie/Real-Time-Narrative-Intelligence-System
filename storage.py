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

# this function can be called by the processor to save computed signals into the database
def save_signals(results):
    timestamp = datetime.now().isoformat()

    for topic, count in results.items():
        cursor.execute("""
        INSERT INTO signals (timestamp, topic, count)
        VALUES (?, ?, ?)
        """, (timestamp, topic, count))

    conn.commit()

# this function can be used to retrieve previous signals for comparison or trend analysis
def get_previous_signals():
    cursor.execute("""
    SELECT topic, SUM(count)
    FROM signals
    GROUP BY topic
    """)
    
    return dict(cursor.fetchall())
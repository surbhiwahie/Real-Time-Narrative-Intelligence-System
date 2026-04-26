import streamlit as st
from streamlit_autorefresh import st_autorefresh

from youtube_producer import fetch_multi_topic
from processor import compute_narratives, get_top_narratives
from storage import save_signals, get_recent_signals
from ai_insights import explain_trends

st.set_page_config(page_title="Narrative Intelligence", layout="wide")

st.title(" Real-Time Narrative Intelligence System")

st_autorefresh(interval=60000, key="refresh")

# ---------------- FETCH ----------------
titles = fetch_multi_topic()

st.subheader("Fetched Data")
st.write(len(titles), "videos analyzed")

# ---------------- PROCESS ----------------
scores = compute_narratives([t.lower() for t in titles])

st.subheader("Narrative Distribution")
st.bar_chart(scores)

# ---------------- HISTORY ----------------
history = get_recent_signals(limit_runs=5)

st.subheader("Trend (vs history)")

trend = {}
for k, v in scores.items():
    prev_vals = []
    for run in history:
        if isinstance(run, dict):
            prev_vals.append(run.get(k, 0))
        elif isinstance(run, (list, tuple)) and len(run) >= 2:
            prev_vals.append(run[1])
    prev_avg = sum(prev_vals) / len(prev_vals) if prev_vals else 0
    # trend[k] = int(v) - prev_avg
    # trend[k] = (v.get("count", v) if isinstance(v, dict) else v) - prev_avg
    trend[k] = v - prev_avg

st.bar_chart(trend)

# ---------------- TOP ----------------
st.subheader("Top Narratives")

top = get_top_narratives(scores)

for k, v in top:
    st.metric(label=k, value=int(v))

# ---------------- AI SUMMARY ----------------
st.subheader("AI Analysis")

summary = "\n".join([f"{k}: {v}" for k, v in scores.items()])
st.write(explain_trends(summary))

# ---------------- SAVE ----------------
save_signals(scores)
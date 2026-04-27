import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import pandas as pd
import re

from youtube_producer import fetch_multi_topic
from processor import compute_narratives, get_top_narratives
from storage import save_signals, get_recent_signals
from ai_insights import explain_trends

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Narrative Intelligence",
    page_icon="🧠",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🧠 Real-Time Narrative Intelligence System")
st.markdown("### Detecting and analyzing evolving narratives in real time")
st.caption("🔄 Auto-refreshing every 60 seconds")

st.divider()

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=60000, key="refresh")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
show_raw = st.sidebar.toggle("Show Raw Data", False)

# ---------------- FETCH ----------------
with st.spinner("📡 Fetching real-time data..."):
    titles = fetch_multi_topic()

# ---------------- PROCESS ----------------
scores = compute_narratives([t.lower() for t in titles])

df_scores = pd.DataFrame(list(scores.items()), columns=["Narrative", "Score"])
df_scores = df_scores.sort_values(by="Score", ascending=False)

# ---------------- TOP METRICS ----------------
top = get_top_narratives(scores)

st.subheader("📊 Top Narratives Overview")

cols = st.columns(len(top))

for i, (k, v) in enumerate(top):
    cols[i].metric(label=k, value=int(v))

st.divider()

# ---------------- NARRATIVE DISTRIBUTION ----------------
st.subheader("📈 Narrative Distribution")

fig = px.bar(
    df_scores,
    x="Narrative",
    y="Score",
    title="Current Narrative Strength",
)

fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- HISTORY / TREND ----------------
history = get_recent_signals(limit_runs=5)

trend = {}
for k, v in scores.items():
    prev_vals = []
    for run in history:
        if isinstance(run, dict):
            prev_vals.append(run.get(k, 0))
        elif isinstance(run, (list, tuple)) and len(run) >= 2:
            prev_vals.append(run[1])

    prev_avg = sum(prev_vals) / len(prev_vals) if prev_vals else 0
    trend[k] = v - prev_avg

df_trend = pd.DataFrame(list(trend.items()), columns=["Narrative", "Change"])

st.subheader("📉 Narrative Trend (vs History)")

fig2 = px.bar(
    df_trend,
    x="Narrative",
    y="Change",
    title="Trend Shift from Previous Runs",
)

fig2.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("🧠 AI Insights")

summary = "\n".join([f"{k}: {v}" for k, v in scores.items()])

with st.spinner("Generating AI insights..."):
    insights = explain_trends(summary)

# ---------------- FORMAT FIX ----------------
def format_insights(text):
    # Fix missing newline after ### headings
    text = re.sub(r"(###\s*\d+\.\s[^\n]+)", r"\1\n", text)

    # Convert numbered sections into bold headers
    text = re.sub(r"\n?(\d+\.\s[^\n]+)", r"\n<br><strong>\1</strong><br>", text)

    # Replace line breaks for HTML rendering
    text = text.replace("\n", "<br>")

    return text

formatted_insights = format_insights(insights)

# ---------------- DISPLAY CARD ----------------
st.markdown(
    f"""
    <div style="
        background-color: rgba(248,249,251,0.9);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.7;
        color: #111;
    ">
        <strong style="font-size:18px;">🧠 AI Insight</strong><br><br>
        {formatted_insights}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- RAW DATA ----------------
if show_raw:
    st.subheader("📰 Raw Titles")
    st.write(titles)

# ---------------- SAVE ----------------
save_signals(scores)
import streamlit as st
from youtube_producer import fetch_multi_topic
from processor import compute_narratives
from storage import get_recent_signals, save_signals
from ai_insights import explain_trends
from streamlit_autorefresh import st_autorefresh


st_autorefresh(interval=60000, key="data_refresh")
st.set_page_config(page_title="Narrative Intelligence Dashboard", layout="wide")

st.title("📊 Real-Time Narrative Intelligence System")

# ---------------------------
# 1. Fetch Data
# ---------------------------
st.header("1. Data Ingestion")

titles = fetch_multi_topic()

st.write(f"Total videos fetched: {len(titles)}")

with st.expander("View raw titles"):
    for t in titles:
        st.write("-", t)

# ---------------------------
# 2. Processing Layer
# ---------------------------
st.header("2. Narrative Signals")

scores = compute_narratives([t.lower() for t in titles])

st.bar_chart(scores)

# ---------------------------
# 3. Trend Layer
# ---------------------------
st.header("3. Trend Analysis")

previous = get_recent_signals()

trend_data = {}

for k, v in scores.items():
    prev = previous.get(k, 0)
    change = v - prev
    trend_data[k] = change

st.bar_chart(trend_data)

# ---------------------------
# 4. Top Narratives
# ---------------------------
st.header("4. Top Narratives")

top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

for k, v in top:
    st.metric(label=k, value=v)

# ---------------------------
# 5. AI Insight Layer
# ---------------------------
st.header("5. AI Narrative Summary")

trend_summary = "\n".join(
    [f"{k}: current={v}, previous={previous.get(k,0)}, change={v - previous.get(k,0)}"
     for k, v in scores.items()]
)

analysis = explain_trends(trend_summary)

st.write(analysis)

# ---------------------------
# 6. Save State
# ---------------------------
save_signals(scores)
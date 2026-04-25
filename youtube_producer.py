from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from storage import save_signals, get_previous_signals
from processor import compute_narratives, generate_insights, compute_trends

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")

# This function fetches recent YouTube video titles based on a "search query"
def fetch_youtube(query="OpenAI"):       # this is the search query for YouTube videos, can be modified to fetch different topics
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=5,
        type="video"
    )

    response = request.execute()

    return [item["snippet"]["title"] for item in response["items"]]

# The main execution flow for the YouTube producer
if __name__ == "__main__":
    videos = fetch_youtube()

    print("\nYouTube Raw Data:\n")
    for v in videos:
        print("-", v)

    # Compute narrative signals from video titles
    results = compute_narratives([v.lower() for v in videos])

    save_signals(results)
    previous = get_previous_signals()
    insights = generate_insights(results)
    trends = compute_trends(insights, previous)

    print("\nAI-STYLE INSIGHTS (YouTube):\n")

    # Display insights along with trend information
    for k, v in insights.items():
        print(k.upper())
        print("count:", v["count"])
        print("signal:", v["signal"])
        print("meaning:", v["meaning"])

        # 🔥 NEW: trend layer
        trend = trends.get(k, {})

        print("previous:", trend.get("previous", 0))
        print("change:", trend.get("change", 0))
        print("direction:", trend.get("direction", "NEW"))
        print("-" * 40)
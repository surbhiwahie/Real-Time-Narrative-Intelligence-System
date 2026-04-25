from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from storage import save_signals, get_previous_signals
from processor import compute_narratives, generate_insights, compute_trends

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")


def fetch_youtube(query="AI news"):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=5,
        type="video"
    )

    response = request.execute()

    return [item["snippet"]["title"] for item in response["items"]]


if __name__ == "__main__":
    videos = fetch_youtube()

    print("\nYouTube Raw Data:\n")
    for v in videos:
        print("-", v)

    results = compute_narratives([v.lower() for v in videos])

    save_signals(results)
    previous = get_previous_signals()
    insights = generate_insights(results)
    trends = compute_trends(insights, previous)

    print("\nAI-STYLE INSIGHTS (YouTube):\n")

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
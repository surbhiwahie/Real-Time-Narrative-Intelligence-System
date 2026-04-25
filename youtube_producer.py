from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

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

    results = []

    for item in response["items"]:
        title = item["snippet"]["title"]
        results.append(title)

    return results


if __name__ == "__main__":
    videos = fetch_youtube()

    print("\nYouTube Raw Data:\n")
    for v in videos:
        print("-", v)

    # send to processor
    from processor import compute_narratives

    results = compute_narratives([v.lower() for v in videos])

    print("\nNarrative Signals (YouTube):\n")

    for k, v in results.items():
        print(k, "->", v)
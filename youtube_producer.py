from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")


def fetch_youtube(query="OpenAI", max_results=5):
    """
    Producer layer:
    ONLY responsible for fetching raw data from YouTube API
    """

    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )

    response = request.execute()

    return [
        item["snippet"]["title"]
        for item in response["items"]
    ]


# This is Optional - for local test only
if __name__ == "__main__":
    data = fetch_youtube()

    print("\nRAW YOUTUBE DATA:\n")
    for d in data:
        print("-", d)


def fetch_multi_topic():

    queries = [
        "AI news",
        "US politics news",
        "world news geopolitics",
        "science discovery",
        "crime breaking news"
    ]

    all_titles = []

    for q in queries:
        results = fetch_youtube(query=q, max_results=5)
        all_titles.extend(results)

    return all_titles
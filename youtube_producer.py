from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
import os
import time

load_dotenv()


CACHE_FILE = "cache.json"
CACHE_TTL = 300  # seconds (5 minutes)

API_KEY = os.getenv("YOUTUBE_API_KEY")


def fetch_youtube(query="AI news", max_results=5):
    """
    Safe producer layer with quota protection
    """

    if not API_KEY:
        print("WARNING: No API key found, using mock data")
        return [f"{query} sample video {i}" for i in range(max_results)]

    try:
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
            for item in response.get("items", [])
        ]

    except Exception as e:
        print("YouTube API failed, switching to fallback mode:", e)
        return [f"{query} fallback video {i}" for i in range(max_results)]


def fetch_multi_topic():
    queries = [
            "AI news",
            "politics US",
            "technology latest",
            "world news",
            "science discovery" ]

    all_titles = []

    for q in queries:
        all_titles.extend(fetch_youtube(q, 3))  # reduced = quota saver

    return all_titles

# Fallback synthetic data generator - Trying because it will be useful for testing and also to ensure the system can run even if API calls fail. This will generate a fixed set of titles that mimic real YouTube trends, allowing us to test the processing and analysis components without relying on live data.
def synthetic_data():
    """
    Fallback data when YouTube API fails
    """
    return [
        "AI breakthrough in healthcare",
        "New AI model beats humans",
        "Crime rates rising in major cities",
        "Scientific discovery shocks researchers",
        "US politics heating up before elections",
        "Global tensions increase between nations"
    ]

    
# This function computes narrative signals based on keyword matching in titles
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        data = json.load(f)

    # check expiry
    if time.time() - data["timestamp"] > CACHE_TTL:
        return None

    return data["titles"]

# This function saves fetched titles to cache with timestamp
def save_cache(titles):
    data = {
        "timestamp": time.time(),
        "titles": titles
    }

    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

# This function computes narrative signals based on keyword matching in titles
def fetch_multi_topic_cached():
    """
    Cached version of multi-topic fetch
    """

    cached = load_cache()

    if cached:
        print("\n Using cached data (avoiding API call)\n")
        return cached

    print("\n Fetching fresh data from API...\n")

    titles = fetch_multi_topic()

    save_cache(titles)

    return titles

def get_data_source():
    try:
        titles = fetch_multi_topic_cached()
        return titles, "API/CACHE"
    except Exception as e:
        print(f"\n API FAILED → Switching to FALLBACK mode\n")
        return synthetic_data(), "FALLBACK"
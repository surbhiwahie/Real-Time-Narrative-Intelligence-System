import requests
import xml.etree.ElementTree as ET

def fetch_news():
    url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    titles = []

    for item in root.findall(".//item"):
        title = item.find("title").text.lower()
        titles.append(title)

    return titles
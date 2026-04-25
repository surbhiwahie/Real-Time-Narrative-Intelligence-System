import requests
import xml.etree.ElementTree as ET

url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

response = requests.get(url)
root = ET.fromstring(response.content)

titles = []

for item in root.findall(".//item"):
    title = item.find("title").text
    titles.append(title)

print("Entries found:", len(titles))

for t in titles[:10]:
    print(t)
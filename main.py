import requests
import xml.etree.ElementTree as ET

url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

response = requests.get(url)
root = ET.fromstring(response.content)

narratives = {
    "politics": ["kushner", "trump", "election", "government", "doj"],
    "crime": ["murder", "charges", "death", "court"],
    "science": ["scientists", "research", "study"],
    "tech": ["ai", "windows", "model", "google"],
    "geopolitics": ["pakistan", "iran", "china", "israel"]
}

scores = {k: 0 for k in narratives}

titles = []

for item in root.findall(".//item"):
    title = item.find("title").text.lower()
    titles.append(title)

    for n, keywords in narratives.items():
        if any(word in title for word in keywords):
            scores[n] += 1

print("Narrative Strength:\n")

total = len(titles)

for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    intensity = round((v / total) * 100, 2)
    print(k, "->", v, f"({intensity}%)")
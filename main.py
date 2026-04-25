from youtube_producer import fetch_youtube
from processor import compute_narratives

titles = fetch_youtube()
scores = compute_narratives(titles)

print("Narrative Signals:\n")

for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(k, "->", v)
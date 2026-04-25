from youtube_producer import fetch_youtube
from processor import compute_narratives
from storage import save_signals, get_previous_signals

def main():
    # 1. Fetch
    titles = fetch_youtube()

    # 2. Process
    scores = compute_narratives([t.lower() for t in titles])

    # 3. Load history
    previous = get_previous_signals()

    # 4. Save current run
    save_signals(scores)

    # 5. Compare current vs previous
    print("\nTREND ANALYSIS:\n")

    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        prev = previous.get(k, 0)
        change = v - prev

        if change > 0:
            direction = "RISING"
        elif change < 0:
            direction = "FALLING"
        else:
            direction = "STABLE"

        print(f"{k.upper():<15}")
        print(f"current: {v}")
        print(f"previous: {prev}")
        print(f"change: {change}")
        print(f"trend: {direction}")
        print("-" * 40)
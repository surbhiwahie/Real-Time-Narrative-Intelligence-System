from youtube_producer import fetch_youtube
from processor import compute_narratives

def main():
    # 1. Fetch data
    titles = fetch_youtube()

    print("\nRAW DATA:\n")
    for t in titles:
        print("-", t)

    # 2. Process
    scores = compute_narratives([t.lower() for t in titles])

    # 3. Normalize
    total = sum(scores.values()) or 1

    print("\nNARRATIVE SIGNALS:\n")

    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        percent = (v / total) * 100
        print(f"{k.upper():<15} -> {v:<3} ({percent:.2f}%)")

    print("\nPIPELINE COMPLETE ✓")


if __name__ == "__main__":
    main()
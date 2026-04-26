from youtube_producer import fetch_youtube, fetch_multi_topic
from processor import compute_narratives, generate_insights, compute_trends
from storage import save_signals, get_recent_signals
from ai_insights import explain_trends


print("main.py started")

def main():
    # 1. Fetch
    titles = fetch_multi_topic()

    
    # 2. Process
    scores = compute_narratives([t.lower() for t in titles])

    # 3. Load history
    previous = get_recent_signals()

    
    # 4. Save current run
    save_signals(scores)

    # 5. Compare current vs previous
    print("\nTREND ANALYSIS:\n")

    trend_summary = ""

    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        prev = previous.get(k, 0)
        change = v - prev
        percent_change = (change / (prev + 1)) * 100

        trend_summary += f"{k}: current={v}, previous={prev}, change={change}\n"

        if change > 0:
            direction = "RISING"
        elif change < 0:
            direction = "FALLING"
        else:
            direction = "STABLE"

        print(f"{k.upper():<15}")
        print(f"current: {v}")
        print(f"rolling avg: {prev:.2f}")
        print(f"change: {change}")
        print(f"trend strength: {percent_change:.2f}%")
        print("-" * 40)

    print("\nAI ANALYSIS:\n")
    analysis = explain_trends(trend_summary)
    print(analysis)

if __name__ == "__main__":
    main()
from youtube_producer import get_data_source
from processor import compute_narratives, get_top_narratives
from storage import save_signals, get_recent_signals
from ai_insights import explain_trends

print("\n=== REAL-TIME NARRATIVE INTELLIGENCE SYSTEM ===\n")


def main():

    # 1. Fetch data (API or fallback)
    titles, source = get_data_source()
    print(f"\nDATA SOURCE: {source}\n")

    # 2. Compute current scores
    scores = compute_narratives([t.lower() for t in titles])

    # 3. Load time-series history
    history = get_recent_signals(limit_runs=5)

    # 4. Save current snapshot
    save_signals(scores)

    # 5. TREND ANALYSIS
    print("\nTREND ANALYSIS:\n")

    trend_summary = ""

    for topic, current_value in scores.items():

        series = history.get(topic, [])

        # extract past values safely
        past_values = [
            item[1] for item in series
            if isinstance(item, tuple) and len(item) >= 2
        ]

        prev_avg = sum(past_values) / len(past_values) if past_values else 0

        change = current_value - prev_avg
        trend_strength = (change / (prev_avg + 1)) * 100

        trend_summary += (
            f"{topic}: current={current_value}, "
            f"prev_avg={prev_avg:.2f}, change={change:.2f}\n"
        )

        print(f"{topic.upper():<15}")
        print(f"current: {current_value}")
        print(f"previous avg: {prev_avg:.2f}")
        print(f"change: {change:.2f}")
        print(f"trend strength: {trend_strength:.2f}%")
        print("-" * 40)

    # 6. TOP narratives
    print("\nTOP NARRATIVES OF THE DAY:\n")
    for name, value in get_top_narratives(scores, top_k=3):
        print(f"{name.upper():<15} -> {value}")

    # 7. AI insights
    print("\nAI INSIGHT:\n")
    print(explain_trends(trend_summary))


if __name__ == "__main__":
    main()
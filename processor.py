# This function computes narrative signals based on keyword matching in news titles (Keyword Counting)
def compute_narratives(titles):
    narratives = {
    "politics": [
        "trump", "biden", "election", "government", "white house",
        "congress", "senate", "policy", "doj", "court", "minister"
    ],

    "crime": [
        "murder", "arrest", "charges", "court", "police",
        "investigation", "shooting", "fraud", "crime"
    ],

    "science": [
        "scientists", "research", "study", "discovery",
        "experiment", "physics", "biology", "paper", "nasa"
    ],

    "tech": [
        "google", "microsoft", "apple", "amazon",
        "software", "cloud", "model", "algorithm",
        "chip", "nvidia", "data", "platform"
    ],

    "ai_narrative": [
        "ai", "artificial intelligence", "openai", "chatgpt",
        "gpt", "claude", "gemini", "llm", "agi",
        "machine learning", "deep learning",
        "robot", "automation", "neural", "transformer",
        "future", "revolution", "crash", "boom", "breakthrough"
    ],

    "geopolitics": [
        "china", "india", "russia", "usa", "america",
        "ukraine", "nato", "israel", "iran", "pakistan",
        "war", "conflict", "tension", "sanctions"
    ]
}

    scores = {k: 0 for k in narratives}

    for title in titles:
        for n, keywords in narratives.items():
            if any(word.lower() in title.lower() for word in keywords):
                scores[n] += 1

    return {
    "scores": scores
}

# This function generates insights based on the computed narrative signals → percent + signal + meaning
def generate_insights(results):
    total = sum(results.values()) or 1

    insights = {}

    for k, v in results.items():
        percent = (v / total) * 100

        if percent >= 70:
            signal = "STRONG SIGNAL"
            meaning = f"{k} is dominating current attention"
        elif percent >= 30:
            signal = "EMERGING SIGNAL"
            meaning = f"{k} is moderately present in discourse"
        else:
            signal = "WEAK SIGNAL"
            meaning = f"{k} is low presence"

        insights[k] = {
            "count": v,
            "percent": round(percent, 2),
            "signal": signal,
            "meaning": meaning
        }

    return insights

# This function computes trends by comparing current signals with previous signals
def compute_trends(current, history):
    trends = {}

    # latest and previous runs
    latest = history[0]["data"] if history else {}
    prev = history[1]["data"] if len(history) > 1 else {}

    for topic, data in current.items():
        current_count = data["count"]

        previous_count = prev.get(topic, 0)

        change = current_count - previous_count

        # trend strength (avoid divide by zero)
        trend_strength = (change / (previous_count + 1)) * 100

        direction = (
            "RISING" if change > 0 else
            "FALLING" if change < 0 else
            "STABLE"
        )

        trends[topic] = {
            "current": current_count,
            "previous": previous_count,
            "change": change,
            "trend_strength": round(trend_strength, 2),
            "direction": direction
        }

    return trends

# This function returns top N narratives sorted by current score
def get_top_narratives(scores, top_k=3):
    """
    Returns top N narratives sorted by current score
    """
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_k]
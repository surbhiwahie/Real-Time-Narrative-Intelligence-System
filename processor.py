# This function computes narrative signals based on keyword matching in news titles (Keyword Counting)
def compute_narratives(titles):
    narratives = {
        "politics": ["kushner", "trump", "election", "government", "doj"],
        "crime": ["murder", "charges", "death", "court"],
        "science": ["scientists", "research", "study"],
        "tech": ["ai", "windows", "model", "google"],
        "geopolitics": ["pakistan", "iran", "china", "israel"]
    }

    scores = {k: 0 for k in narratives}

    for title in titles:
        for n, keywords in narratives.items():
            if any(word in title for word in keywords):
                scores[n] += 1

    return scores

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
def compute_trends(current, previous):
    trends = {}

    for topic, data in current.items():
        current_count = data["count"]
        previous_count = previous.get(topic, 0)

        change = current_count - previous_count

        if change > 0:
            direction = "RISING"
        elif change < 0:
            direction = "FALLING"
        else:
            direction = "STABLE"

        trends[topic] = {
            "current": current_count,
            "previous": previous_count,
            "change": change,
            "direction": direction
        }

    return trends
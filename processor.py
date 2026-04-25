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
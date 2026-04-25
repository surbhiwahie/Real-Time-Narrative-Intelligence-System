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
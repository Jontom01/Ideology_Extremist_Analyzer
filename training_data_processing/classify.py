# classifier/classify.py
def label_classification(d: dict) -> str:
    w = 1/5 #weight
    score = 0
    for feature in d['features'].values():
        score += w*feature

    if score >= 0 and score < 0.2:
        d['label'] = "ideologically_very_mild"
    elif score >= 0.2 and score < 0.4:
        d['label'] = "ideologically_mild"
    elif score >= 0.4 and score < 0.6:
        d['label'] = "ideologically_intermediate"
    elif score >= 0.6 and score <= 1:
        d['label'] = "ideologically_extreme"

    return d

if __name__ == "__main__":
    test_features =  {
            'text': "The original Reddit message or comment here.",
            'features': {
                'cognitive_rigid_score': 0.8,
                'external_blame_score': 0.6,
                'social_hostility_score': 0.6,
                'emotional_intensity': 0.8,
                'conspiratorial_thinking_score': 0.6
            }
    }
    label = label_classification(test_features)
    print(label)

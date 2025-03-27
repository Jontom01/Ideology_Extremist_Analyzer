# classifier/classify.py
def label_classification(d: dict) -> str:
    w = 1/7 #weight
    score = 0
    for feature in d['features'].values():
        score += w*feature
    if score < 0.6: 
        d['label'] = "ideologically_moderate"
    else:
        d['label'] = "ideologically_extreme"
    return d
def classify_features(features: dict) -> str:
    """
    Given a dictionary of feature scores, return a label:
      - 'ideologically_extreme' or 'ideologically_moderate'
    Uses simple threshold-based logic.
    """
    # Example thresholds (you can adjust these as needed)
    extreme_threshold = 0.8

    # Check if most of the "extreme" features are high
    certainty = features.get("certainty_score", 0)
    blame = features.get("external_blame_score", 0)
    condescension = features.get("condescension_score", 0)
    nuance = features.get("nuance_score", 1)  # Lower nuance implies extremity
    buzzword = features.get("buzzword_density", 0)
    agreeability = features.get("agreeability_score", 1)  # Lower agreeability implies extremity

    # Count how many "extreme" signals there are:
    extreme_signals = sum([
        1 if certainty >= extreme_threshold else 0,
        1 if blame >= extreme_threshold else 0,
        1 if condescension >= extreme_threshold else 0,
        1 if buzzword >= extreme_threshold else 0,
        1 if nuance < (1 - extreme_threshold) else 0,
        1 if agreeability < (1 - extreme_threshold) else 0
    ])

    # For instance, if 3 or more signals indicate extremity, classify as extreme.
    if extreme_signals >= 3:
        return "ideologically_extreme"
    else:
        return "ideologically_moderate"

# Example usage (for testing):
if __name__ == "__main__":
    test_features =  {
            'text': "The original Reddit message or comment here.",
            'features': {
                'cognitive_rigid_score': 0.8,
                'external_blame_score': 0.6,
                'social_hostility_score': 0.6,
                'buzzword_density': 0.7,
                'emotional_intensity': 0.8,
                'identity_fusion_score': 0.3,
                'conspiratorial_thinking_score': 0.6
            }
    }
    label = label_classification(test_features)
    print(label)

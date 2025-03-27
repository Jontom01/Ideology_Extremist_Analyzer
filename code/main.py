# main.py
from feature_extraction import eval_features
from classify import classify_features
from reddit_scraper import scrape_subreddit
from csv_processing import dict_to_csv

def process_text(text: str):
    print("Input Text:")
    print(text)
    print("\nExtracting features...")
    features = extract_features(text)
    print("Features:", features)
    label = classify_features(features)
    print("Predicted Label:", label)

if __name__ == "__main__":
    # Example: input text. In practice, you might loop over a dataset.
    subreddit_names = ["politics", "NeutralPolitics", "LateStageCapitalism", "FemaleDatingStrategy", "askFeminists", "Conservative", "EnoughLibertarianSpam", "TrueOffMyChest", "TwoXChromosomes", "natureisbeautiful", "ChangeMyView"]
    posts, comments = scrape_subreddit(subreddit_names, limit=7)
    features_dict_list = eval_features(comments)
    dict_to_csv(features_dict_list)
    #i = 0
   # for comment in comments:
    #    print(i, ": ", comment)
     #   print("\n")
     #   i += 1
    
    #sample_text = "These people are brainwashed and the system is rigged against us. Only idiots would disagree with this obvious truth."
    #process_text(sample_text)

# main.py
from feature_extraction import eval_features
from reddit_scraper import scrape_subreddit
from csv_processing import dict_to_csv

if __name__ == "__main__":
    # Example: input text. In practice, you might loop over a dataset.
    subreddit_names = [
        "Hobbies", "CasualConversation", "Vegan", "MensRights", "TheRedPill", "NeutralPolitics", 
    "LateStageCapitalism", "FemaleDatingStrategy", "Conservative", "EnoughLibertarianSpam", 
    "TrueOffMyChest", "TwoXChromosomes", "natureisbeautiful", "ChangeMyView", "politics", "askFeminists"
    ]
    posts, comments = scrape_subreddit(subreddit_names, limit=10)
    features_dict_list = eval_features(comments)
    dict_to_csv(features_dict_list)
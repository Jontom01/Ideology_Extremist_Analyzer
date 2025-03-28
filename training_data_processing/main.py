# main.py
from feature_extraction import eval_features
from reddit_scraper import scrape_subreddit
from csv_processing import dict_to_csv

"""
This file puts it all together and ultimately creates the training data.
"""

if __name__ == "__main__":
    subreddit_names = [
        "Hobbies", "CasualConversation", "Vegan", "MensRights", "NeutralPolitics", 
    "LateStageCapitalism", "FemaleDatingStrategy", "Conservative", "EnoughLibertarianSpam", 
    "TrueOffMyChest", "TwoXChromosomes", "natureisbeautiful", "ChangeMyView", "politics", "askFeminists"
    ]
    posts, comments = scrape_subreddit(subreddit_names, limit=1)
    features_dict_list = eval_features(comments)
    dict_to_csv(features_dict_list)
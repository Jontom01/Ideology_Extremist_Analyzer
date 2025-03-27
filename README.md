# Ideology_Extremist_Analyzer

Description:

This project builds a supervised learning system designed to detect ideological extremity in online written communication—particularly from informal sources like Reddit. Instead of relying on political keywords or partisan alignment, the system focuses on how people express their beliefs, modeling psychological traits that research has strongly linked to ideological rigidity.

Each message is scored across a set of psychologically grounded features, such as cognitive rigidity, external blame attribution, emotional intensity, moral absolutism, and conspiratorial thinking. These features are extracted using a language model (e.g., GPT-4o via ChatGPT API) via prompt-based analysis, then stored as structured numerical vectors for training. Labeled data is used to classify each message as either ideologically moderate or ideologically extreme based on aggregated feature scores.

The system supports flexible integration with Reddit scraping (via Reddit API using PRAW), data labeling, and CSV conversion modules, making it suitable for both exploratory research and production-scale classification tasks. By emphasizing psychological language patterns over surface-level political content, the model is designed to generalize across political, cultural, and identity-based ideological domains.

Software structure/architecture and details:

The first section of this program we will be looking at is that of the training_data_processing. The integration of this section's modules follows a pipe-and-filter style architecture.

----------------------------------------------------------------------------------------------------------------------------


Obtain Online Messages -----> Extract Linguistic Features -----> Classify Ideological Extremity -----> Convert to CSV Output


----------------------------------------------------------------------------------------------------------------------------

Obtain Online Messages (scrape_reddit.py):
In order to obtain the online messages required to train the data. I used Reddit API's PRAW module to hundreds of comments off of different posts and subreddits (some likely containing extreme comments and others more neutrally toned).

Extract Linguistic Features (feature_extraction.py):
Now, once having a large list of messages, this module defines and extracts the features of each message. I used the model 4o ChatGPT API (along with a very lengthy and detailed prompt) in order to give each message accurate feature scores.

Classify Ideological Extremity (classify.py):
Based off a linear combination of the feature scores, each message is also given a binary label, of either "ideologically_extreme" or "ideologically_moderate".

Convert to CSV Output (csv_processing.py):
Finally, the list of messages (which are dicts with fields: text, features, label) with feature scores and labels are converted into a CSV file.


NEXT MUST TALK ABOUT SECTION THAT HAS THE ACTUAL CLASSIFIER

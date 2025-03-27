# Ideology_Extremist_Analyzer

**Description:**

This project aims to detect and classify ideological extremity in online discussions. It gathers text data from Reddit using the **Reddit API**, then applies ChatGPT (via **OpenAI’s API**) to extract psychologically grounded features (e.g., cognitive rigidity, emotional intensity, conspiratorial thinking). The resulting feature vectors are used to train a **Random Forest Classifier (RFC)**, a supervised learning model that predicts whether a given comment is ideologically moderate, intermediate, or extreme.

The training features chosen are based off of well-established research from political psychology, social cognition, and behavioral science. Decades of empirical studies have identified psychological traits that are strongly associated with ideological extremity, regardless of political orientation or topic domain. These traits form the basis of the linguistic features extracted from Reddit comments using ChatGPT API.

Traits: Cognitive Rigidity, Group-Based Identity Fusion, Conspiratorial Mindset, Authoritarian Personality, Intolerance of Ambiguity, Moral Outrage, Emotional Intensity, Victimhood Narrative, Dogmatism, Social DominanceOrientation, Ideological Buzzword Usage.

All of these are captured through the features used to train the RFC.

**Software structure/architecture and details:**

The first section of this program we will be looking at is that of the training_data_processing. The integration of this section's modules follows a pipe-and-filter style architecture.

----------------------------------------------------------------------------------------------------------------------------


Obtain Messages -----> Extract Linguistic Features -----> Classify Ideological Extremity -----> Convert to CSV Output


----------------------------------------------------------------------------------------------------------------------------

Obtain Messages (scrape_reddit.py):
In order to obtain the online messages required to train the data. I used Reddit API's PRAW module to hundreds of comments off of different posts and subreddits (some likely containing extreme comments and others more neutrally toned).

Extract Linguistic Features (feature_extraction.py):
Now, once having a large list of messages, this module defines and extracts the features of each message. I used the model 4o ChatGPT API (along with a very lengthy and detailed prompt) in order to give each message accurate feature scores.

Classify Ideological Extremity (classify.py):
Based off a linear combination of the feature scores, each message is also given a binary label, of either "ideologically_extreme", "ideologically_intermediate", "ideologically_mild", "ideologically_very_mild".

Convert to CSV Output (csv_processing.py):
Finally, the list of messages (which are dicts with fields: text, features, label) with feature scores and labels are converted into a CSV file.


NEXT MUST TALK ABOUT SECTION THAT HAS THE ACTUAL CLASSIFIER

The 

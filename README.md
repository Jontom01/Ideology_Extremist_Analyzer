# Ideology_Extremist_Analyzer

**Description:**

This project detects and analyzes ideological extremity in online discussions. It gathers conversational data from Reddit using the **Reddit API**, then applies ChatGPT (**via OpenAI’s API**) to extract psychologically grounded behavioural traits through these messages (such as cognitive rigidity, dogmatism, and conspiratorial thinking). These extracted features are used to build a structured dataset that includes each message, its psychological features, the originating subreddit, and a timestamp. This dataset enables detailed analysis of ideological extremity trends across communities, individuals, and time periods.

The features chosen are based off of well-established research from political psychology, social cognition, and behavioral science. Decades of empirical studies have identified psychological traits that are strongly associated with ideological extremity, regardless of political orientation or topic domain. These traits form the basis of the linguistic features extracted from Reddit comments using ChatGPT API.

Traits being captured: Cognitive Rigidity, Group-Based Identity Fusion, Conspiratorial Mindset, Authoritarian Personality, Emotional Intensity, Victimhood Narrative, Dogmatism, Social Dominance Orientation.

**Software structure/architecture and details:**

**Training Data Processing:**

The first section of this program we will be looking at is that of the training_data_processing. The integration of this section's modules follows a pipe-and-filter style architecture.

----------------------------------------------------------------------------------------------------------------------------


Obtain Messages -----> Extract Linguistic Features -----> Classify Ideological Extremity -----> Convert to CSV Output


----------------------------------------------------------------------------------------------------------------------------

Obtain Messages (*scrape_reddit.py*):
In order to obtain the online messages required to train the data. I used Reddit API's PRAW module to hundreds of comments off of different posts and subreddits (some likely containing extreme comments and others more neutrally toned). Returns dictionary containing comment, subreddit, utc_time.

Extract Linguistic Features (*feature_extraction.py*):
Now, once having a large list of messages, this module defines and extracts the features of each message. I used the model 4o ChatGPT API (along with a very lengthy and detailed prompt) in order to give each message accurate feature scores.

Classify Ideological Extremity (*classify.py*):
Based off a linear combination of the feature scores, each message is also given a label, of either "ideologically_extreme", "ideologically_intermediate", "ideologically_mild", "ideologically_very_mild".

Convert to CSV Output (*csv_processing.py*):
Finally, the list of messages (which are dicts with fields: text, subreddit, utc_time, features, label) are converted into a CSV file.

**Use Cases and Hypothesis Testing:**

One key use case is analyzing how ideological extremity evolves over time within specific communities. By tracking psychological features extracted from subreddit comments across different time periods, we can uncover temporal patterns, such as shifts toward increased polarization or moderation. This temporal analysis may reveal correlations between real-world events and changes in subreddit dynamics, offering insights into the factors influencing ideological trends within online communities.

*not done*
# data/scrape_reddit.py
import praw
from config import REDDIT_CLIENT_SECRET, REDDIT_CLIENT_ID, REDDIT_USER_AGENT
def scrape_subreddit(subreddit_names: list[str], limit: int = 10) -> tuple[list, list[dict]]:
    """
    Scrapes posts from a specified subreddit.
    
    Parameters:
        subreddit_name (str): Name of the subreddit (e.g., "politics").
        limit (int): Number of posts to retrieve.
    
    Returns:
        List of dictionaries, each containing the title and selftext of a post.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,        
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    comment_list = []
    for subreddit_name in subreddit_names:
        subredditVar = reddit.subreddit(subreddit_name)
        for submission in subredditVar.hot(limit=limit): #get submission objects from subreddit object
            posts.append(submission.title)
            comments_in_post = submission.comments #get comment objects from submission object
            if len(comments_in_post) < 10:
                for comment in comments_in_post:
                    comment_list.append({'comment': comment.body, 'subreddit': subreddit_name, 'utc_time': comment.created_utc})
            else:
                for i in range(1,10):
                    comment_list.append({'comment': comments_in_post[i].body, 'subreddit': subreddit_name, 'utc_time': comments_in_post[i].created_utc})

    return posts, comment_list

if __name__ == "__main__":
    subreddit_names = [
        "Hobbies", "CasualConversation", "Vegan", "MensRights", "NeutralPolitics", 
    "LateStageCapitalism", "FemaleDatingStrategy", "Conservative", "EnoughLibertarianSpam", 
    "TrueOffMyChest"
    ]    
    posts, comments = scrape_subreddit(subreddit_names, limit=2)
    '''
    for post in posts:
        print(post)
        print("\n")
    print("\n")
    print("-------------------------------")
    print("\n")
    #print(comments)
    i = 0
    '''
    i = 0
    for comment in comments:
        print(i, ": ", comment)
        print("\n")
        i += 1
   # for post in posts:
       # print("Title:", post["title"])
       # print("Content:", post["selftext"])
       # print("-----")

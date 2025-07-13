import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="crypto-trend-detector"
)

def get_reddit_mentions(coin, limit=50):
    subreddits = ["CryptoCurrency", "CryptoMarkets", "Bitcoin", "ethtrader", "CryptoMoonShots"]
    posts = []
    for sub in subreddits:
        for submission in reddit.subreddit(sub).search(coin, sort="new", limit=limit):
            if coin.lower() in submission.title.lower():
                posts.append(submission.title)
    # print(posts)
    return posts


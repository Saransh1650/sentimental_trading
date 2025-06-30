import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID", "LUDn15dl17ur4pg7SOlDlg"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET", "6vtoomm5cVVSXEyE1hQ0BFowop9faA"),
    user_agent="crypto-trend-detector"
)

def get_reddit_mentions(coin, limit=50):
    subreddits = ["CryptoCurrency", "CryptoMarkets", "Bitcoin", "ethtrader", "CryptoMoonShots"]
    posts = []
    for sub in subreddits:
        for submission in reddit.subreddit(sub).search(coin, sort="new", limit=limit):
            if coin.lower() in submission.title.lower():
                posts.append(submission.title)
    print(posts)
    return posts


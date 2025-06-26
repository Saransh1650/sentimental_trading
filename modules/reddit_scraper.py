# modules/reddit_scraper.py
import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID", "LUDn15dl17ur4pg7SOlDlg"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET", "6vtoomm5cVVSXEyE1hQ0BFowop9faA"),
    user_agent="crypto-trend-detector"
)

def get_reddit_mentions(coin, limit=50):
    subreddit = reddit.subreddit("CryptoCurrency")
    posts = []
    for post in subreddit.new(limit=limit):
        if coin.lower() in post.title.lower():
            posts.append(post.title)
    return posts

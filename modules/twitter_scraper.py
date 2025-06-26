import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta

def get_tweets(coin, minutes=15, max_tweets=100):
    query = f'${coin}'
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append(tweet.content)
    return tweets

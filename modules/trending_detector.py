# modules/trending_detector.py
from modules.twitter_scraper import get_tweets
from modules.reddit_scraper import get_reddit_mentions
from modules.sentiment_analyzer import analyze_sentiment

def analyze_coin(coin):
    # tweets = get_tweets(coin)
    reddit = get_reddit_mentions(coin)
    all_text = reddit
    mention_count = len(all_text)
    sentiment_score = analyze_sentiment(all_text)
    trend_score = round(mention_count * (1 + sentiment_score), 2)
    
    return {
        "coin": coin,
        "mentions": mention_count,
        "sentiment": sentiment_score,
        "score": trend_score
    }

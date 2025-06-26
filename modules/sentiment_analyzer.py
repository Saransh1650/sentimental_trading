from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(texts):
    scores = [analyzer.polarity_scores(t)["compound"] for t in texts]
    avg_score = sum(scores) / len(scores) if scores else 0
    return round(avg_score, 3)

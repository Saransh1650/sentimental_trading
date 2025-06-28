# utils/spike_detector.py
from collections import deque
import csv
from collections import defaultdict

def read_last_two_snapshots(filepath='data/logs.csv'):
    # For each coin, keep a deque of its last two records
    coin_history = defaultdict(lambda: deque(maxlen=2))

    with open(filepath, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            coin = row['coin']
            coin_history[coin].append({
                'coin': coin,
                'mentions': int(row['mentions']),
                'sentiment': float(row['sentiment']),
                'score': float(row['trend_score'])
            })

    prev, curr = [], []
    for coin, records in coin_history.items():
        if len(records) == 2:
            prev.append(records[0])
            curr.append(records[1])
    if not prev or not curr:
        return None, None
    return prev, curr

def detect_spikes(prev, curr, sentiment_thresh=0.2, mention_thresh=50):
    spikes = []
    prev_map = {c['coin']: c for c in prev}

    for c in curr:
        coin = c['coin']
        if coin not in prev_map:
            continue

        prev_c = prev_map[coin]
        sentiment_diff = c['sentiment'] - prev_c['sentiment']
        mention_diff = c['mentions'] - prev_c['mentions']

        if sentiment_diff > sentiment_thresh or mention_diff > mention_thresh:
            spikes.append({
                'coin': coin,
                'sentiment_change': sentiment_diff,
                'mention_change': mention_diff,
                'score': c['score']
            })

    return spikes

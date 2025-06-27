# utils/spike_detector.py
import csv
from collections import defaultdict

def read_last_two_snapshots(filepath='data/logs.csv'):
    snapshots = defaultdict(list)

    with open(filepath, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        if len(rows) < 2:
            return None, None  # Not enough data

        # group by timestamp
        for row in rows[-100:]:  # limit to last 100 entries
            ts = row['timestamp']
            snapshots[ts].append({
                'coin': row['coin'],
                'mentions': int(row['mentions']),
                'sentiment': float(row['sentiment']),
                'score': float(row['trend_score'])
            })

    timestamps = sorted(snapshots.keys())
    return snapshots[timestamps[-2]], snapshots[timestamps[-1]]

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

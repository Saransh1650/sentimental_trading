# utils/spike_detector.py
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

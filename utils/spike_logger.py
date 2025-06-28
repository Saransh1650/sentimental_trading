import csv
from datetime import datetime

def log_spike_and_trend(spikes, trends, filepath='data/spike_trends.csv'):
    """
    Logs detected spikes and current trend info for each coin.
    spikes: list of dicts from detect_spikes
    trends: list of dicts with current trend info (coin, score, mentions, sentiment)
    """
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if f.tell() == 0:
            writer.writerow([
                'timestamp', 'coin', 'spike', 'sentiment_change', 'mention_change',
                'score', 'mentions', 'sentiment'
            ])
        now = datetime.now().isoformat()
        # Log spikes
        for spike in spikes:
            trend = next((t for t in trends if t['coin'] == spike['coin']), {})
            writer.writerow([
                now,
                spike['coin'],
                'YES',
                round(spike['sentiment_change'], 3),
                spike['mention_change'],
                trend.get('score', ''),
                trend.get('mentions', ''),
                trend.get('sentiment', '')
            ])
        # Log non-spike trends
        spiked_coins = {s['coin'] for s in spikes}
        for trend in trends:
            if trend['coin'] not in spiked_coins:
                writer.writerow([
                    now,
                    trend['coin'],
                    'NO',
                    '',
                    '',
                    trend['score'],
                    trend['mentions'],
                    trend['sentiment']
                ])
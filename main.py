import json
import time
import schedule
from modules.trending_detector import analyze_coin
from utils.google_sheets_client import log_coin_data, read_last_two_snapshots, log_spike_and_trend
from utils.detect_spike import detect_spikes
from datetime import datetime

def job():
    with open("config/coins.json") as f:
        coins = json.load(f)

    results = []
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    for coin in coins:
        data = analyze_coin(coin)
        data['timestamp'] = timestamp
        print(f"{coin}: 🔥 Trend Score: {data['score']} (Mentions: {data['mentions']}, Sentiment: {data['sentiment']})")
        results.append(data)

    # ✅ Log this round's results to Google Sheets
    log_coin_data(results)

    # Detect and print spikes
    prev, curr = read_last_two_snapshots()
    if prev and curr:
        spikes = detect_spikes(prev, curr)
        if spikes:
            print("\n🚨 Spike Alerts:")
            for s in spikes:
                s['timestamp'] = timestamp
                print(f"- {s['coin']}: Sentiment Δ {s['sentiment_change']:.2f}, Mentions Δ {s['mention_change']}, Score: {s['score']}")
            log_spike_and_trend(spikes, results)
        else:
            print("\nNo significant spikes detected.")

    # Optional: show top trending coins
    top = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
    print("\n🚨 Trending Coins:")
    for c in top:
        print(f"- {c['coin']} → Score: {c['score']}")

# Schedule the job to run every 15 minutes
schedule.every(15).minutes.do(job)

# Run the job immediately at startup
job()

while True:
    schedule.run_pending()
    time.sleep(1)

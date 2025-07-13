import json
from modules.trending_detector import analyze_coin
from utils.google_sheets_client import log_coin_data, read_last_two_snapshots, log_spike_and_trend
from utils.detect_spike import detect_spikes
from datetime import datetime, timedelta, timezone

def run_job():
    with open("config/coins.json") as f:
        coins = json.load(f)

    results = []
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    timestamp = ist_now.strftime('%Y-%m-%d %H:%M:%S')

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
        print(f"spikes: {spikes}")
        if spikes:
            print("\n🚨 Spike Alerts:")
            for s in spikes:
                s['timestamp'] = timestamp
                print(f"- {s['coin']}: Sentiment Δ {s['sentiment_change']:.2f}, Mentions Δ {s['mention_change']}, Score: {s['score']}")
        else:
            print("\nNo significant spikes detected.")
        log_spike_and_trend(spikes, results)

    # Optional: show top trending coins
    top = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
    print("\n🚨 Trending Coins:")
    for c in top:
        print(f"- {c['coin']} → Score: {c['score']}") 

if __name__ == "__main__":
    run_job()

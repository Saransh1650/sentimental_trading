import json
from modules.trending_detector import analyze_coin
from utils.logger import log_coin_data
from utils.detect_spike import read_last_two_snapshots, detect_spikes
from utils.spike_logger import log_spike_and_trend

with open("config/coins.json") as f:
    coins = json.load(f)

results = []

for coin in coins:
    data = analyze_coin(coin)
    print(f"{coin}: 🔥 Trend Score: {data['score']} (Mentions: {data['mentions']}, Sentiment: {data['sentiment']})")
    results.append(data)

# ✅ Log this round's results to logs.csv
log_coin_data(results)

# Detect and print spikes
prev, curr = read_last_two_snapshots()
if prev and curr:
    spikes = detect_spikes(prev, curr)
    if spikes:
        print("\n🚨 Spike Alerts:")
        for s in spikes:
            print(f"- {s['coin']}: Sentiment Δ {s['sentiment_change']:.2f}, Mentions Δ {s['mention_change']}, Score: {s['score']}")
    else:
        print("\nNo significant spikes detected.")
        
log_spike_and_trend(spikes, results)

# Optional: show top trending coins
top = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
print("\n🚨 Trending Coins:")
for c in top:
    print(f"- {c['coin']} → Score: {c['score']}")

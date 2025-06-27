import json
from modules.trending_detector import analyze_coin
from utils.logger import log_coin_data

with open("config/coins.json") as f:
    coins = json.load(f)

results = []

for coin in coins:
    data = analyze_coin(coin)
    print(f"{coin}: 🔥 Trend Score: {data['score']} (Mentions: {data['mentions']}, Sentiment: {data['sentiment']})")
    results.append(data)

# ✅ Log this round's results to logs.csv
log_coin_data(results)

# Optional: show top trending coins
top = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
print("\n🚨 Trending Coins:")
for c in top:
    print(f"- {c['coin']} → Score: {c['score']}")

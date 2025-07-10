import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spike_trends.csv", parse_dates=["timestamp"])
pivot_df = df.pivot(index="timestamp", columns="coin", values="sentiment")

plt.figure(figsize=(14, 7))
for coin in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[coin], label=coin)

plt.title("Sentiment Over Time for Top Coins")
plt.xlabel("Timestamp")
plt.ylabel("Sentiment Score")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

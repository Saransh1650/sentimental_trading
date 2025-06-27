import os
import csv
from datetime import datetime

def log_coin_data(coin_data, filepath='data/logs.csv'):
    file_exists = os.path.isfile(filepath)
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header only if file does not exist
        if not file_exists:
            writer.writerow(['timestamp', 'coin', 'mentions', 'sentiment', 'trend_score'])

        # Write each coin's data
        for data in coin_data:
            writer.writerow([now, data['coin'], data['mentions'], data['sentiment'], data['score']])

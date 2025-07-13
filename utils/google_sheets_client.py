import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict, deque

# Set up credentials using the recommended google-auth library
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Open the spreadsheet by name, or create it if it doesn't exist
SPREADSHEET_NAME = "Crypto Trading Logs"
try:
    spreadsheet = client.open(SPREADSHEET_NAME)
except gspread.exceptions.SpreadsheetNotFound:
    spreadsheet = client.create(SPREADSHEET_NAME)

# Get worksheets by name, or create them if they don't exist
try:
    coin_data_sheet = spreadsheet.worksheet("Coin Data")
except gspread.exceptions.WorksheetNotFound:
    coin_data_sheet = spreadsheet.add_worksheet(title="Coin Data", rows="1000", cols="20")

try:
    spike_trends_sheet = spreadsheet.worksheet("Spike Trends")
except gspread.exceptions.WorksheetNotFound:
    spike_trends_sheet = spreadsheet.add_worksheet(title="Spike Trends", rows="1000", cols="20")

def log_coin_data(coin_data):
    """Logs a list of coin data to the 'Coin Data' worksheet."""
    # If the sheet is empty, add the header row
    if not coin_data_sheet.get_all_values():
        header = ['timestamp', 'coin', 'mentions', 'sentiment', 'score']
        coin_data_sheet.append_row(header, value_input_option='USER_ENTERED')

    rows = []
    for data in coin_data:
        rows.append([data['timestamp'], data['coin'], data['mentions'], data['sentiment'], data['score']])
    
    # Append all rows and use USER_ENTERED to ensure correct data parsing
    coin_data_sheet.append_rows(rows, value_input_option='USER_ENTERED')

def log_spike_and_trend(spikes, trends):
    """Logs detected spikes and current trend info to the 'Spike Trends' worksheet."""
    # If the sheet is empty, add the header row
    if not spike_trends_sheet.get_all_values():
        header = ['timestamp', 'coin', 'spike', 'sentiment_change', 'mention_change', 'score', 'mentions', 'sentiment']
        spike_trends_sheet.append_row(header, value_input_option='USER_ENTERED')

    rows = []
    for spike in spikes:
        trend = next((t for t in trends if t['coin'] == spike['coin']), {})
        rows.append([
            spike['timestamp'],
            spike['coin'],
            'YES',
            round(spike.get('sentiment_change', 0), 3),
            spike.get('mention_change', 0),
            trend.get('score', ''),
            trend.get('mentions', ''),
            trend.get('sentiment', '')
        ])

    spiked_coins = {s['coin'] for s in spikes}
    for trend in trends:
        if trend['coin'] not in spiked_coins:
            rows.append([
                trend['timestamp'],
                trend['coin'],
                'NO',
                '',
                '',
                trend['score'],
                trend['mentions'],
                trend['sentiment']
            ])
            
    # Append all rows and use USER_ENTERED to ensure correct data parsing
    spike_trends_sheet.append_rows(rows, value_input_option='USER_ENTERED')

def read_last_two_snapshots():
    """
    Reads all data from the 'Coin Data' worksheet and returns the last two snapshots for each coin.
    Returns None, None if no coin has at least two data points for comparison.
    """
    records = coin_data_sheet.get_all_records()

    # Group all records by coin, keeping only the last two for each
    coin_history = defaultdict(lambda: deque(maxlen=2))
    for record in records:
        try:
            # Ensure data from the sheet is in the correct format
            record['mentions'] = int(record['mentions'])
            record['sentiment'] = float(record['sentiment'])
            record['score'] = float(record['score'])
            coin_history[record['coin']].append(record)
        except (ValueError, KeyError):
            # Skip rows with malformed data
            continue

    prev, curr = [], []
    for coin, history in coin_history.items():
        # Only add to the list if a coin has two snapshots to compare
        if len(history) == 2:
            prev.append(history[0])
            curr.append(history[1])

    # If no coins had enough data for a comparison, return None
    if not prev:
        return None, None

    return prev, curr

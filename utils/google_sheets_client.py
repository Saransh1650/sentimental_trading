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

def log_coin_data(coin_data):
    """
    Logs a list of coin data to the 'Coin Data' worksheet, keeping only the last two snapshots per coin.
    """
    # Get all existing data from the sheet
    try:
        all_values = coin_data_sheet.get_all_values()
        # More robust header check to avoid errors on empty sheets/rows
        header = all_values[0] if all_values and all_values[0] else ['timestamp', 'coin', 'mentions', 'sentiment', 'score']
    except gspread.exceptions.APIError as e:
        print(f"Error accessing the sheet: {e}")
        return

    # Create a dictionary of records from the existing data
    existing_records = []
    if len(all_values) > 1:
        for row in all_values[1:]:
            # Skip empty rows
            if not row or not any(row):
                continue
            while len(row) < len(header):
                row.append('')
            existing_records.append(dict(zip(header, row)))

    # Add the new data to the records
    for data in coin_data:
        existing_records.append(data)

    # Group records by coin
    coin_snapshots = defaultdict(list)
    for record in existing_records:
        try:
            if record.get('coin') and record.get('timestamp'):
                coin_snapshots[record['coin']].append(record)
        except KeyError:
            continue

    # Keep only the last two snapshots for each coin
    final_rows = []
    for coin, snapshots in coin_snapshots.items():
        snapshots.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        last_two = snapshots[:2]
        for record in last_two:
            final_rows.append([str(record.get(h, '')) for h in header])
            
    # Safely sort the final list by coin name (the second column)
    final_rows.sort(key=lambda x: x[1] if len(x) > 1 else None)

    # Add the header back
    final_rows.insert(0, header)

    # Clear the sheet and write the updated data
    try:
        coin_data_sheet.clear()
        coin_data_sheet.update('A1', final_rows, value_input_option='USER_ENTERED')
    except gspread.exceptions.APIError as e:
        print(f"Error updating the sheet: {e}")

def log_spike_and_trend(spikes, trends):
    """Logs detected spikes and current trend info to a separate worksheet for each coin."""
    spiked_coins_map = {s['coin']: s for s in spikes}

    for trend in trends:
        coin_name = trend['coin']
        try:
            worksheet = spreadsheet.worksheet(coin_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=coin_name, rows="1000", cols="20")

        is_spike = 'NO'
        sentiment_change = 0
        mention_change = 0

        if trend['coin'] in spiked_coins_map:
            spike_info = spiked_coins_map[trend['coin']]
            is_spike = 'YES'
            sentiment_change = round(spike_info.get('sentiment_change', 0), 3)
            mention_change = spike_info.get('mention_change', 0)

        row_to_log = [
            trend['timestamp'],
            is_spike,
            sentiment_change,
            mention_change,
            trend.get('score', 0),
            trend['mentions'],
            trend['sentiment']
        ]

        all_values = worksheet.get_all_values()
        if not all_values or not all_values[0]:
            header = ['timestamp', 'spike', 'sentiment_change', 'mention_change', 'score', 'mentions', 'sentiment']
            worksheet.append_row(header, value_input_option='USER_ENTERED')
        
        worksheet.append_row(row_to_log, value_input_option='USER_ENTERED')

def read_last_two_snapshots(recent_rows_to_check=200):
    """
    Reads the last `recent_rows_to_check` from the 'Coin Data' worksheet 
    and returns the last two snapshots for each coin. This is an optimized 
    function to avoid reading the entire sheet.
    Returns None, None if no coin has at least two data points for comparison.
    """
    try:
        all_first_col_values = coin_data_sheet.col_values(1)
        total_rows = len(all_first_col_values)
    except gspread.exceptions.APIError as e:
        print(f"Error getting row count from Google Sheets: {e}")
        return None, None

    if total_rows < 2:
        return None, None

    # Determine the range to read
    start_row = max(2, total_rows - recent_rows_to_check + 1)
    
    try:
        header = coin_data_sheet.row_values(1)
        range_to_get = f'A{start_row}:{chr(ord("A")+len(header)-1)}{total_rows}'
        recent_values = coin_data_sheet.get(range_to_get)
    except gspread.exceptions.APIError as e:
        print(f"Error getting recent data from Google Sheets: {e}")
        return None, None

    records = []
    for row in recent_values:
        # Pad the row with empty strings if it's shorter than the header
        while len(row) < len(header):
            row.append('')
        records.append(dict(zip(header, row)))

    coin_snapshots = defaultdict(list)
    for record in records:
        try:
            if record.get('coin'): # Ensure there is a coin name
                record['mentions'] = int(record['mentions'])
                record['sentiment'] = float(record['sentiment'])
                record['score'] = float(record['score'])
                coin_snapshots[record['coin']].append(record)
        except (ValueError, KeyError, TypeError):
            continue

    prev, curr = [], []
    for coin, snapshots in coin_snapshots.items():
        if len(snapshots) >= 2:
            prev.append(snapshots[-2])
            curr.append(snapshots[-1])

    if not prev:
        return None, None

    return prev, curr

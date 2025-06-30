"""
modules/onchain_monitor.py
Functions to monitor on-chain and exchange activity for a given cryptocurrency.
Uses mock data for demonstration; replace with real API calls as needed.
"""
import requests
import random
from datetime import datetime, timedelta


def get_whale_transactions(coin):
    """
    Fetch large on-chain transactions (whale transactions) for a given coin.
    For ETH, uses Etherscan API. For other coins, returns empty list.
    """
    if coin.upper() != "ETH":
        return []
    ETHERSCAN_API_KEY = "YourApiKeyToken"  # Replace with your Etherscan API key
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    resp = requests.get(url)
    txs = []
    if resp.status_code == 200:
        for tx in resp.json().get("result", [])[:10]:
            if float(tx["value"]) / 1e18 > 100:  # Only large txs
                txs.append({
                    "timestamp": datetime.utcfromtimestamp(int(tx["timeStamp"])).isoformat(),
                    "amount": float(tx["value"]) / 1e18,
                    "from_address": tx["from"],
                    "to_address": tx["to"],
                    "tx_hash": tx["hash"]
                })
    return txs


def get_exchange_flows(coin):
    """
    Fetch exchange inflows/outflows for the given coin in the past hour.
    Uses mock data. Replace with Glassnode or similar API for real data.
    Args:
        coin (str): Symbol of the coin (e.g., 'BTC', 'ETH')
    Returns:
        dict: {'inflow': float, 'outflow': float, 'net_flow': float}
    """
    # --- MOCK DATA ---
    # In production, use Glassnode or CryptoQuant API here.
    inflow = round(random.uniform(1000, 10000), 2)
    outflow = round(random.uniform(1000, 10000), 2)
    net_flow = inflow - outflow
    return {'inflow': inflow, 'outflow': outflow, 'net_flow': net_flow}


def get_volume_spikes(coin):
    """
    Check for sudden large trading volume spikes for the coin in the past hour.
    Uses mock data. Replace with exchange API or CoinGecko for real data.
    Args:
        coin (str): Symbol of the coin (e.g., 'BTC', 'ETH')
    Returns:
        tuple: (spike_detected (bool), current_volume (float))
    """
    # --- MOCK DATA ---
    # In production, fetch recent and historical volume, compare for spike.
    current_volume = round(random.uniform(1_000_000, 10_000_000), 2)
    # Simulate a spike if volume is above a threshold
    spike_detected = current_volume > 8_000_000
    return spike_detected, current_volume

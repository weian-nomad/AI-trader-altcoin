"""
exchange_data_collector.py
用於從交易所 (Binance, OKX, etc.) 抓取行情資料 (K線, OrderBook, Trades等)。
"""

import requests
import time
from typing import Optional, List

class ExchangeDataCollector:
    def __init__(self, base_url: str):
        """
        :param base_url: 交易所 API 的基底網址 (e.g. https://api.binance.com)
        """
        self.base_url = base_url
    
    def get_klines(self, symbol: str, interval: str = "1h", limit: int = 100) -> Optional[List]:
        """
        取得 K 線資料
        :param symbol: 如 'BTCUSDT'
        :param interval: K 線週期 (e.g. '1m', '15m', '1h', '1d')
        :param limit: 取得多少根 K 線
        :return: list of klines or None
        """
        endpoint = "/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        url = self.base_url + endpoint
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()  # 若狀態碼非 200，拋出例外
            return resp.json()
        except Exception as e:
            print(f"Error fetching klines: {e}")
            return None

    def get_orderbook(self, symbol: str, limit: int = 10) -> Optional[dict]:
        """
        取得委託簿資料
        :param symbol: 如 'BTCUSDT'
        :param limit: 要多少檔位 (e.g. 10, 100, 500)
        :return: orderbook dict or None
        """
        endpoint = "/api/v3/depth"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        url = self.base_url + endpoint
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error fetching orderbook: {e}")
            return None

if __name__ == "__main__":
    # 簡單測試
    binance = ExchangeDataCollector(base_url="https://api.binance.com")
    klines = binance.get_klines("BTCUSDT", "1h", 5)
    print("Klines:", klines[:1] if klines else "No data")
    
    orderbook = binance.get_orderbook("BTCUSDT", 5)
    print("OrderBook:", orderbook if orderbook else "No data")
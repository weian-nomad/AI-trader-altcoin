"""
sentiment_data_collector.py
用於抓取市場或社群平台的情緒相關數據 (如 Fear & Greed Index, Twitter, Reddit, etc.)。
"""

import requests
from typing import Optional

class SentimentDataCollector:
    def __init__(self):
        pass
    
    def get_fear_greed_index(self) -> Optional[dict]:
        """
        範例：從 Alternative.me 抓取 Fear & Greed Index
        API文件: https://alternative.me/crypto/fear-and-greed-index/
        
        :return: 回傳情緒指數數據 (JSON 格式) 或 None
        """
        url = "https://api.alternative.me/fng/"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
            return None

    def get_twitter_sentiment(self, keyword: str):
        """
        範例：抓取 Twitter 上某關鍵字的情緒分數 (可用第三方 API 或自建爬蟲)
        """
        # TODO: 待實做
        pass
    
    def get_reddit_sentiment(self, subreddit: str):
        """
        範例：抓取 Reddit 某個版上的情緒狀況
        """
        # TODO: 待實做
        pass

if __name__ == "__main__":
    collector = SentimentDataCollector()
    fng_data = collector.get_fear_greed_index()
    print(fng_data)
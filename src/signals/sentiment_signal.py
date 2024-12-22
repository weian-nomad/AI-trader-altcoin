"""
sentiment_signal.py
用於根據抓取到的情緒數據 (社群、新聞等) 做量化評分、情緒指標計算等。
"""

class SentimentSignal:
    def __init__(self, sentiment_data):
        """
        :param sentiment_data: 可能是一個 dict、或 DataFrame，儲存爬回來的情緒資訊
        """
        self.sentiment_data = sentiment_data

    def calculate_score(self) -> float:
        """
        將情緒資料轉換為量化指標或分數
        :return: 例如回傳 0~100 的分數
        """
        # TODO: 根據情緒資料計算分數
        return 50.0  # 僅示意

if __name__ == "__main__":
    # 範例測試
    mock_data = {"fear_greed_index": "56", "updated_at": "2024-01-01"}
    sentiment_signal = SentimentSignal(mock_data)
    score = sentiment_signal.calculate_score()
    print(f"Sentiment Score: {score}")
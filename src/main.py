"""
main.py
整個程式的主進入點 (若需要)。可以在此結合 collectors/signals/risk 等模組做流程控制。
"""

from collectors.exchange_data_collector import ExchangeDataCollector
from collectors.sentiment_data_collector import SentimentDataCollector
from signals.technical_signal import TechnicalSignal
from signals.sentiment_signal import SentimentSignal
from risk.risk_management import RiskManager
from utils.db_utils import DBUtils
from utils.config_loader import Config
import pandas as pd

def main():
    # 1. 載入設定
    config = Config()

    # 2. 建立資料收集器
    binance_collector = ExchangeDataCollector(base_url="https://api.binance.com")
    sentiment_collector = SentimentDataCollector()

    # 3. 抓取 K 線資料 (示例)
    klines = binance_collector.get_klines("BTCUSDT", "1h", 10)
    if klines is not None:
        # 將 kline 資料轉成 DataFrame
        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", 
            "volume", "close_time", "quote_asset_volume", 
            "trades_count", "taker_buy_base_asset_volume", 
            "taker_buy_quote_asset_volume", "ignore"
        ])
        # 轉換數值欄位
        numeric_cols = ["open", "high", "low", "close", "volume"]
        df[numeric_cols] = df[numeric_cols].astype(float)

        # 4. 技術指標
        tech_signal = TechnicalSignal(df)
        tech_signal.add_ma()
        tech_signal.add_rsi()
        result_df = tech_signal.get_signal_data()
        print(result_df.head())

    # 5. 抓取情緒資料 (示例)
    fng_data = sentiment_collector.get_fear_greed_index()
    sentiment_signal = SentimentSignal(fng_data)
    sentiment_score = sentiment_signal.calculate_score()
    print("Sentiment Score:", sentiment_score)

    # 6. 風控檢查 (示例)
    risk_manager = RiskManager(0.1, 10000)  # max_position_size = 10%, balance=10000
    can_trade = risk_manager.check_order_size(1500)
    print("可否下單？", can_trade)

    # 7. 資料庫操作 (示例)
    db = DBUtils(
        host=config.db_host, 
        user=config.db_user, 
        password=config.db_password, 
        database=config.db_name
    )
    db.connect_mysql()
    # 可進行資料庫操作...
    db.close()

if __name__ == "__main__":
    main()
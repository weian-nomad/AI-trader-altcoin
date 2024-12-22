"""
technical_signal.py
用於計算各種技術分析指標，如 MA, RSI, MACD 等。
"""

import pandas as pd
import talib

class TechnicalSignal:
    def __init__(self, df: pd.DataFrame):
        """
        :param df: 需包含 open, high, low, close, volume 欄位的 DataFrame
        """
        self.df = df

    def add_ma(self, period: int = 20, column_name: str = "MA_20"):
        """
        新增均線欄位
        """
        self.df[column_name] = talib.SMA(self.df['close'], timeperiod=period)

    def add_rsi(self, period: int = 14, column_name: str = "RSI_14"):
        """
        新增 RSI 欄位
        """
        self.df[column_name] = talib.RSI(self.df['close'], timeperiod=period)

    def add_macd(self, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        新增 MACD, MACD signal, MACD hist 欄位
        """
        macd, macdsignal, macdhist = talib.MACD(
            self.df['close'], 
            fastperiod=fastperiod, 
            slowperiod=slowperiod, 
            signalperiod=signalperiod
        )
        self.df['MACD'] = macd
        self.df['MACD_signal'] = macdsignal
        self.df['MACD_hist'] = macdhist

    def get_signal_data(self) -> pd.DataFrame:
        """
        回傳已加入技術指標的 DataFrame
        """
        return self.df

if __name__ == "__main__":
    # 範例用法 (以假資料測試)
    data = {
        'open':   [100, 110, 105, 115, 120],
        'high':   [110, 115, 108, 118, 125],
        'low':    [95, 105, 100, 110, 115],
        'close':  [108, 107, 106, 116, 122],
        'volume': [1000, 1200, 800, 1500, 2000]
    }
    df = pd.DataFrame(data)
    tech = TechnicalSignal(df)
    tech.add_ma()
    tech.add_rsi()
    tech.add_macd()
    print(tech.get_signal_data())
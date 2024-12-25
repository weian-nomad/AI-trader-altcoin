"""
technical_signal.py

提供技術指標計算與交易訊號產生的函式。
可藉由 TA-Lib 或自行撰寫指標公式 (e.g. RSI, MACD, Bollinger Bands)。
"""

import pandas as pd
import numpy as np
import talib

def compute_technical_indicators(df: pd.DataFrame,
                                 price_col: str = "close",
                                 high_col: str = "high",
                                 low_col: str = "low",
                                 volume_col: str = "volume") -> pd.DataFrame:
    """
    為 DataFrame 新增常見技術指標欄位:
    - RSI
    - MACD (MACD, MACD Signal, MACD Hist)
    - Bollinger Bands (upper, middle, lower)
    - 其他指標可自行加上

    參數:
    -------
    df : pd.DataFrame
        包含 K線或歷史價格的 DataFrame，至少需包含 [price_col, high_col, low_col, volume_col]
    price_col : str
        收盤價欄位名稱，預設為 "close"
    high_col : str
        最高價欄位名稱，預設為 "high"
    low_col : str
        最低價欄位名稱，預設為 "low"
    volume_col : str
        成交量欄位名稱，預設為 "volume"

    回傳:
    -------
    pd.DataFrame
        新增各種技術指標欄位的 DataFrame
    """

    # 複製一份避免改動原 DataFrame
    df = df.copy()

    # 檢查欄位
    required_cols = [price_col, high_col, low_col, volume_col]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame 缺少必要欄位: {col}")

    close = df[price_col].astype(float).values
    high = df[high_col].astype(float).values
    low = df[low_col].astype(float).values
    volume = df[volume_col].astype(float).values

    # 1. RSI (預設週期14)
    df["RSI"] = talib.RSI(close, timeperiod=14)

    # 2. MACD
    #    macd: MACD值
    #    macdsignal: "訊號線"
    #    macdhist:   MACD柱狀圖(差值)
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df["MACD"] = macd
    df["MACD_SIGNAL"] = macdsignal
    df["MACD_HIST"] = macdhist

    # 3. Bollinger Bands (預設週期20, 2標準差)
    upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df["BB_UPPER"] = upper
    df["BB_MID"] = middle
    df["BB_LOWER"] = lower

    # 其他常見指標 (例: MA、EMA、ADX、OBV...) 都可在這裡加入
    # df["MA_20"] = talib.SMA(close, timeperiod=20)
    # df["EMA_50"] = talib.EMA(close, timeperiod=50)
    # df["ADX"] = talib.ADX(high, low, close, timeperiod=14)
    # df["OBV"] = talib.OBV(close, volume)

    return df


def generate_trading_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    依據技術指標結果，產生簡易的交易訊號(買進/賣出/觀望)。
    此處範例僅示意，實際策略可能需要更多判斷條件或風控。

    策略範例：
    - RSI < 30 視為超賣，給予 "BUY" 建議
    - RSI > 70 視為超買，給予 "SELL" 建議
    - MACD 由負翻正，給予 "BUY"；由正翻負，給予 "SELL"
    - Bollinger Bands 中，若收盤價 < BB_LOWER，視為超跌，給予 "BUY"；若 > BB_UPPER，給予 "SELL"
    
    回傳:
    -------
    pd.DataFrame
        多一欄 "signal" (或多欄) 表示該筆 K 線的交易訊號
    """

    # 複製一份避免改動原 DataFrame
    df = df.copy()

    # 需要先檢查指標是否已存在
    necessary_cols = ["RSI", "MACD", "MACD_HIST", "BB_UPPER", "BB_LOWER", "close"]
    for col in necessary_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame 缺少必要技術指標欄位: {col}，請先呼叫 compute_technical_indicators")

    # 建立一個欄位 signal 來儲存交易建議
    signals = []
    for i in range(len(df)):
        rsi = df.loc[df.index[i], "RSI"]
        macd = df.loc[df.index[i], "MACD"]
        macd_hist = df.loc[df.index[i], "MACD_HIST"]
        bb_upper = df.loc[df.index[i], "BB_UPPER"]
        bb_lower = df.loc[df.index[i], "BB_LOWER"]
        close_price = df.loc[df.index[i], "close"]

        signal = "HOLD"  # 預設持有觀望

        # RSI 超賣/超買範例
        if rsi < 30:
            signal = "BUY"
        elif rsi > 70:
            signal = "SELL"

        # MACD 柱狀圖由負轉正(多頭交叉) -> BUY；由正轉負(空頭交叉) -> SELL
        # 為了簡化，我們直接用當下柱狀圖值做判斷 (實務上應該要觀察前一筆跟本筆的差異)
        if macd_hist > 0:
            # 若本來是 "SELL" 狀態，可以視策略需求決定是否要覆蓋
            signal = "BUY"
        elif macd_hist < 0:
            signal = "SELL"

        # Bollinger Bands 超出上下軌
        if close_price < bb_lower:
            signal = "BUY"
        elif close_price > bb_upper:
            signal = "SELL"

        signals.append(signal)

    df["signal"] = signals

    return df


def run_technical_signals_process(df: pd.DataFrame) -> pd.DataFrame:
    """
    封裝「計算技術指標」與「產生交易訊號」的流程。
    回傳含所有技術欄位 + signal 欄位的 DataFrame。
    """

    df = compute_technical_indicators(df)
    df = generate_trading_signals(df)
    return df


if __name__ == "__main__":
    """
    簡易測試: 需要準備一份含有 open, high, low, close, volume 欄位的 K 線資料
    這裡以隨機產生假資料模擬流程，只示範程式能否正常跑。
    """

    # 假資料
    data = {
        "open": np.random.randint(100, 200, size=100),
        "high": np.random.randint(100, 200, size=100),
        "low": np.random.randint(100, 200, size=100),
        "close": np.random.randint(100, 200, size=100),
        "volume": np.random.randint(500, 2000, size=100),
    }
    df_mock = pd.DataFrame(data)

    # 排序一下，假設時間序列 (index 代表時間)
    df_mock.sort_index(inplace=True)

    # 計算技術指標 & 產生交易訊號
    result_df = run_technical_signals_process(df_mock)

    print(result_df.head(10))

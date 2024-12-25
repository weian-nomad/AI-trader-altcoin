"""
sentiment_signal.py

使用 Hugging Face Transformers 的情感分析 (Sentiment Analysis) pipeline，
來對文本進行情緒評估並產生簡易的交易信號或情緒分數。

示例採用 distilbert-base-uncased-finetuned-sst-2-english 模型，適用英文文本。
若需要中文或多語種，請更換適當的模型。
"""

import pandas as pd
from transformers import pipeline

# 在模組初始化時，就先建立一個 sentiment-analysis pipeline
# （模型只需在初始化時載入一次，避免重複載入浪費時間）
sentiment_analyzer = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
    # 若有其他需求，可自行指定更多參數，例如 device=0 (使用GPU)
)

def compute_sentiment_scores(df: pd.DataFrame,
                             text_col: str = "text") -> pd.DataFrame:
    """
    使用 Hugging Face 的 sentiment-analysis pipeline 來計算情緒分數。
    會在 DataFrame 中新增以下欄位:
      - hf_label: e.g. POSITIVE / NEGATIVE
      - hf_score: 範圍在 0~1 的信心分數 (score)

    參數:
    -------
    df : pd.DataFrame
        需包含文本欄位 (text_col)。
    text_col : str
        要做情感分析的文本欄位，預設 "text"。

    回傳:
    -------
    pd.DataFrame
        原始 df + hf_label, hf_score 欄位
    """
    df = df.copy()

    if text_col not in df.columns:
        raise ValueError(f"DataFrame 缺少文字欄位: {text_col}")

    # 將所有文本收集成 list，送入 pipeline 做 batch 處理
    texts = df[text_col].astype(str).tolist()

    # sentiment_analyzer 回傳的結果是一個 list[ { 'label':..., 'score':...}, ...]
    results = sentiment_analyzer(texts, truncation=True)

    hf_labels = []
    hf_scores = []

    for res in results:
        # res 例如: {'label': 'POSITIVE', 'score': 0.9867688417434692}
        hf_labels.append(res["label"])
        hf_scores.append(res["score"])

    df["hf_label"] = hf_labels
    df["hf_score"] = hf_scores

    return df


def generate_sentiment_signals(df: pd.DataFrame,
                               label_col: str = "hf_label",
                               score_col: str = "hf_score",
                               threshold: float = 0.8) -> pd.DataFrame:
    """
    依據 Hugging Face sentiment 分析結果，產生簡易訊號: BUY / SELL / HOLD。
    示範策略:
      - 若 label=POSITIVE 且 score > threshold -> BUY
      - 若 label=NEGATIVE 且 score > threshold -> SELL
      - 其餘 -> HOLD (或可視為中性)

    參數:
    -------
    df : pd.DataFrame
        已包含 hf_label, hf_score 欄位 (可由 compute_sentiment_scores 產生)。
    label_col : str
        模型預測的情感標籤欄位 (預設 hf_label)。
    score_col : str
        模型對該標籤的信心分數 (預設 hf_score)。
    threshold : float
        超過此分數才視為強烈看多/看空。

    回傳:
    -------
    pd.DataFrame
        新增 sentiment_signal 欄位表示交易訊號。
    """
    df = df.copy()

    if label_col not in df.columns or score_col not in df.columns:
        raise ValueError(
            f"DataFrame 缺少必要欄位: {label_col}, {score_col} (請先呼叫 compute_sentiment_scores)")

    signals = []
    for i, row in df.iterrows():
        label = row[label_col]
        score = row[score_col]

        # 預設訊號
        signal = "HOLD"

        # 簡易示例: 僅當分數>threshold 時，才做明確買賣
        if label == "POSITIVE" and score > threshold:
            signal = "BUY"
        elif label == "NEGATIVE" and score > threshold:
            signal = "SELL"

        signals.append(signal)

    df["sentiment_signal"] = signals
    return df


def run_sentiment_analysis_process(df: pd.DataFrame,
                                   text_col: str = "text") -> pd.DataFrame:
    """
    封裝「計算情緒分數」與「產生情感訊號」的流程。
    預期 DataFrame 至少包含可用來做情感分析的文字欄位 (text_col)。
    依據需求可客製化 threshold 或其他條件。
    """
    df = compute_sentiment_scores(df, text_col=text_col)
    df = generate_sentiment_signals(df)
    return df


if __name__ == "__main__":
    # 簡易測試: 模擬一些英文文本，驗證情感分析流程
    data = {
        "text": [
            "I absolutely love the new product! It's a game-changer for crypto.",
            "This is the worst update ever. I'm extremely disappointed!",
            "It's okay, nothing too special. Could be better.",
            "Bitcoin to the moon! I'm so bullish right now!",
            "Seems quite complicated, but I'm not entirely sure."
        ]
    }

    df_mock = pd.DataFrame(data)
    df_result = run_sentiment_analysis_process(df_mock, text_col="text")
    print(df_result)

# System Design

## Overview
本系統主要目標為整合多種數據源 (交易所、鏈上、情緒、宏觀經濟等) 並產生多因子訊號，提供初步風控檢查後，進行投資決策支持。

## Architecture
1. **Data Collectors**
   - `exchange_data_collector.py` 抓取交易所行情、訂單簿、交易量
   - `sentiment_data_collector.py` 抓取情緒指標
   - (可擴充鏈上、宏觀數據的 collector)

2. **Signals**
   - `technical_signal.py`：多種技術因子 (MA, RSI, MACD…)
   - `sentiment_signal.py`：情緒因子 (Fear & Greed, Twitter/Reddit…)
   - (可擴充鏈上與宏觀因子)

3. **Risk Management**
   - `risk_management.py`：最初步的部位控管、流動性檢查等

4. **Database & Storage**
   - `db_utils.py`：資料庫存取 (MySQL, PostgreSQL, MongoDB…)
   - 也可用 CSV/Parquet 做暫存

5. **Configurations**
   - `config_loader.py`：負責載入 API Key、DB 連線等設定

6. **Main Workflow**
   - `main.py`：整合上述功能，完成資料抓取、訊號計算、風控檢查等流程。

## Data Flow
1. **Collector**：呼叫外部 API 取得資料
2. **Signals**：技術指標 & 情緒分數計算
3. **Risk**：基本風控檢查
4. **Decision**：後續可再整合策略模組，決定是否下單

## Future Work
- 加入更豐富的因子 (鏈上活動、大戶地址追蹤、衍生品持倉量…)
- 風控升級 (止損機制、熔斷機制…)
- 自動化交易 (下單與倉位管理)
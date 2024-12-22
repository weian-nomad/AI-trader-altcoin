"""
config_loader.py
用於載入專案配置、API Key等。可結合 .env 或其他 YAML/JSON 配置檔。
"""

import os
from dotenv import load_dotenv

class Config:
    def __init__(self, env_file: str = ".env"):
        """
        :param env_file: 指定 .env 檔案路徑
        """
        load_dotenv(env_file)  # 讀取 .env
        self.binance_api_key = os.getenv("BINANCE_API_KEY", "")
        self.binance_secret_key = os.getenv("BINANCE_SECRET_KEY", "")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "root")
        self.db_password = os.getenv("DB_PASSWORD", "root")
        self.db_name = os.getenv("DB_NAME", "testdb")

if __name__ == "__main__":
    # 測試
    config = Config()
    print("Binance API Key:", config.binance_api_key)
    print("DB Host:", config.db_host)
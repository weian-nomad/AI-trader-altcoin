#!/usr/bin/env python3
import os

# 預計建立的資料夾路徑
directories = [
    "src/collectors",
    "src/signals",
    "src/risk",
    "src/utils",
    "docs",
    "tests"
]

# 預計建立的檔案路徑 (根目錄檔案在最外層)
files = [
    ".gitignore",
    ".env.example",
    "requirements.txt",
    "src/collectors/exchange_data_collector.py",
    "src/collectors/sentiment_data_collector.py",
    "src/signals/technical_signal.py",
    "src/signals/sentiment_signal.py",
    "src/risk/risk_management.py",
    "src/utils/db_utils.py",
    "src/utils/config_loader.py",
    "src/main.py",
    "docs/system_design.md",
    "tests/__init__.py"
]

def create_directories_and_files():
    """建立指定的資料夾與檔案結構"""
    for d in directories:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")
    
    for f in files:
        dirpath = os.path.dirname(f)
        # 如果 dirpath 不為空，就先建立其父資料夾
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        # 建立空白檔案 (若檔案不存在才建立)
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as fp:
                pass
            print(f"Created file: {f}")
        else:
            print(f"File already exists: {f}")

if __name__ == "__main__":
    create_directories_and_files()
"""
db_utils.py
用於處理與資料庫的連線/讀寫邏輯，可搭配 MySQL、PostgreSQL、MongoDB...等
"""

import mysql.connector
# from pymongo import MongoClient
# import psycopg2

class DBUtils:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        :param host: 資料庫主機
        :param user: 資料庫用戶
        :param password: 資料庫密碼
        :param database: 資料庫名稱
        :param port: 資料庫連接埠 (預設 3306 for MySQL)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect_mysql(self):
        """
        連接 MySQL，並建立 self.conn
        """
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def create_table(self, sql: str):
        """
        建立表格範例
        :param sql: CREATE TABLE 語法
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

    def insert_data(self, sql: str, data_tuple):
        """
        插入資料範例
        :param sql: INSERT 語法
        :param data_tuple: (val1, val2, ...)
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, data_tuple)
        self.conn.commit()

    def close(self):
        """
        關閉連線
        """
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # 簡單測試 (需先在 MySQL 建立對應的 database)
    db = DBUtils(host="localhost", user="root", password="root", database="testdb")
    db.connect_mysql()
    
    # 建立範例 table
    create_sql = """
    CREATE TABLE IF NOT EXISTS test_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        value FLOAT
    )
    """
    db.create_table(create_sql)

    # 插入範例資料
    insert_sql = "INSERT INTO test_table (name, value) VALUES (%s, %s)"
    db.insert_data(insert_sql, ("test_item", 123.45))

    db.close()
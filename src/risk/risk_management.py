"""
risk_management.py
用於做最初步的風控檢查，如下單金額限制、資金部位控管等。
"""

class RiskManager:
    def __init__(self, max_position_size: float, account_balance: float):
        """
        :param max_position_size: 單筆交易的最大限制 (e.g. 不超過總資金 10%)
        :param account_balance: 帳戶總資金
        """
        self.max_position_size = max_position_size
        self.account_balance = account_balance

    def check_order_size(self, order_amount: float) -> bool:
        """
        檢查下單金額是否合理
        :param order_amount: 當前計畫下單金額
        :return: 若 order_amount 超過限制，則回傳 False
        """
        if order_amount > self.account_balance * self.max_position_size:
            return False
        return True

    def check_liquidity(self, symbol: str):
        """
        檢查交易對的流動性，如太小的幣種可設定額外限制
        """
        # TODO: 可結合成交量、深度等資料做風控
        pass

if __name__ == "__main__":
    # 範例測試
    risk_manager = RiskManager(max_position_size=0.1, account_balance=10000)
    can_trade = risk_manager.check_order_size(1500)
    print("可否下單？", can_trade)
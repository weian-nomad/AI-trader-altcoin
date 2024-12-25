"""
risk_management.py

簡易風控機制示範，包括部位大小計算、停損停利檢查、資金池控管等。
實際可再加入更完整的槓桿、保證金、維持率等檢查機制。
"""

import pandas as pd
import numpy as np

class RiskManager:
    """
    用於管理交易策略的風險與資金配置。
    你可以將此類別整合到策略流程中，對交易訊號做最後一道審核/調整。
    """

    def __init__(self,
                 total_capital: float,
                 risk_per_trade: float = 0.01,
                 max_daily_drawdown: float = 0.05,
                 stop_loss_rate: float = 0.02,
                 take_profit_rate: float = 0.05):
        """
        初始化風控參數:
          - total_capital: 初始總資金 (假設 = 100,000 USD)
          - risk_per_trade: 單筆交易可承受的最大虧損比例 (預設 1%)
          - max_daily_drawdown: 當日資金最大回撤比例 (預設 5%)
          - stop_loss_rate: 預設停損比率 (相對於進場價格, 2%)
          - take_profit_rate: 預設停利比率 (相對於進場價格, 5%)
        """
        self.initial_capital = total_capital
        self.current_capital = total_capital
        self.risk_per_trade = risk_per_trade
        self.max_daily_drawdown = max_daily_drawdown
        self.stop_loss_rate = stop_loss_rate
        self.take_profit_rate = take_profit_rate

        # 追蹤當日淨損益，以便判斷是否達到每日最大回撤
        self.daily_pl = 0.0  # profit/loss

        # 標記是否達到今日的最大回撤限制
        self.daily_limit_reached = False

    def reset_daily_pl(self):
        """每天開始時重置當日損益與 daily_limit_reached"""
        self.daily_pl = 0.0
        self.daily_limit_reached = False

    def update_daily_pl(self, profit_or_loss: float):
        """
        在每次交易結束後更新當日盈虧。
        若達到最大回撤限制 (max_daily_drawdown)，則標記 daily_limit_reached。
        """
        self.daily_pl += profit_or_loss
        # 相對於當日開始時的資金
        daily_drawdown_ratio = -self.daily_pl / self.current_capital

        if daily_drawdown_ratio >= self.max_daily_drawdown:
            self.daily_limit_reached = True
            print("[RiskManager] 已達當日最大回撤限制，停止交易。")

        # 更新當前資金 (簡化處理)
        self.current_capital += profit_or_loss

    def compute_position_size(self, entry_price: float) -> float:
        """
        計算部位大小(數量)。方法: 每筆交易的最大虧損 = (entry_price - stop_loss_price) * position_size
        但這裡僅使用一個簡化公式:
          - 期望承受的最大虧損 = current_capital * risk_per_trade
          - 預設停損 % = self.stop_loss_rate
          => position_size = (當筆可承受虧損金額) / (entry_price * stop_loss_rate)

        回傳:
          - position_size (數量)
        """
        if entry_price <= 0:
            return 0.0

        # 單筆可承受的最大虧損金額
        max_loss = self.current_capital * self.risk_per_trade

        # 以預設的 stop_loss_rate 為停損比率
        # (例如 0.02 => 2% 停損 => (entry_price - stop_price) / entry_price = 0.02)
        # => actual stop_loss_price = entry_price * (1 - stop_loss_rate)
        # => potential loss per unit = entry_price - (entry_price * (1 - stop_loss_rate)) = entry_price * stop_loss_rate
        # => position_size = max_loss / (entry_price * stop_loss_rate)

        position_size = max_loss / (entry_price * self.stop_loss_rate)
        return position_size

    def check_stop_loss_take_profit(self, entry_price: float, current_price: float):
        """
        檢查當前價是否觸發停損/停利 (以預設比率計算)。
        回傳:
          - "STOP_LOSS" / "TAKE_PROFIT" / None
        """
        if entry_price <= 0:
            return None

        # 計算當前相對 entry_price 的漲跌幅
        change_ratio = (current_price - entry_price) / entry_price

        # 若跌幅 >= stop_loss_rate，判定停損
        if change_ratio <= -self.stop_loss_rate:
            return "STOP_LOSS"

        # 若漲幅 >= take_profit_rate，判定停利
        if change_ratio >= self.take_profit_rate:
            return "TAKE_PROFIT"

        return None

    def can_trade(self):
        """
        檢查是否允許當前再進行交易。
        若已達到當日最大回撤限制，回傳 False。
        """
        return not self.daily_limit_reached


# 以下為一個示範流程
def demo_risk_management():
    """
    簡易示範如何使用 RiskManager:
      1. 初始化 RiskManager
      2. 每筆交易前檢查是否可交易 (daily_limit_reached)
      3. 計算部位大小
      4. 做完交易後更新當日盈虧
    """
    rm = RiskManager(total_capital=100000, risk_per_trade=0.01, max_daily_drawdown=0.05,
                     stop_loss_rate=0.02, take_profit_rate=0.05)

    # 假設一天有多筆交易，這裡以簡單序列示範
    # 每筆交易的entry_price, exit_price, ...
    trades = [
        {"entry_price": 100, "exit_price": 110},  # 漲10%
        {"entry_price": 110, "exit_price": 105},  # 跌約4.5%
        {"entry_price": 105, "exit_price": 98},   # 跌約6.7% (可超過預設停損?)
        {"entry_price": 90, "exit_price": 95},    # 漲5.5%
        # ...
    ]

    rm.reset_daily_pl()  # 新的一天開始

    for idx, t in enumerate(trades):
        if not rm.can_trade():
            print(f"[Demo] 已達當日最大回撤，跳過交易 #{idx+1}")
            continue

        entry_price = t["entry_price"]
        exit_price = t["exit_price"]

        # 計算部位大小
        position_size = rm.compute_position_size(entry_price)

        print(f"\n[Demo] 進行交易 #{idx+1}, 進場價={entry_price}, 預計下單數量={position_size:.3f}")

        # 模擬交易：最終盈虧 = (exit_price - entry_price) * position_size
        trade_pl = (exit_price - entry_price) * position_size

        # 更新當日盈虧
        rm.update_daily_pl(trade_pl)
        print(f"[Demo] 該筆交易損益={trade_pl:.2f}, 當日損益合計={rm.daily_pl:.2f}, 当前資金={rm.current_capital:.2f}")

    print(f"\n[Demo] 今日結束。是否觸及最大回撤限制? {rm.daily_limit_reached}\n")


if __name__ == "__main__":
    # 若只想測試該檔案，可執行 demo_risk_management
    demo_risk_management()

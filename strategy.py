import pandas as pd

class Strategy:
    def __init__(self):
        self.fast = 10
        self.slow = 20

    def signal(self, df):
        df["ma_fast"] = df["close"].rolling(self.fast).mean()
        df["ma_slow"] = df["close"].rolling(self.slow).mean()

        if df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1]:
            return "BUY"

        if df["ma_fast"].iloc[-1] < df["ma_slow"].iloc[-1]:
            return "SELL"

        return "WAIT"

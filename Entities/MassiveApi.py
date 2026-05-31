from typing import TypedDict

class AggData(TypedDict):
    timestamp: int
    number_of_transactions: int
    volume: float
    close: float
    high: float
    low: float
    open: float
    vwap: float
    stock_name: str

import cProfile
import time
from pymongo.synchronous.database import Database
from typing import Any, Mapping
from FirstTimer.Services import MassiveService, DatabaseService

STOCKS = [
    # Tech
    "AAPL", "GOOGL", "MSFT", "META", "NFLX", "NVDA", "AMD", "INTC", "TSLA", "AMZN",
    "ORCL", "CRM", "ADBE", "QCOM", "TXN", "SHOP", "SNOW", "PLTR", "UBER", "LYFT",
    # Finance
    "JPM", "BAC", "GS", "MS", "V", "MA", "PYPL", "AXP", "BLK", "C",
    # Health
    "JNJ", "PFE", "MRK", "ABBV", "UNH", "CVS", "AMGN", "GILD", "BMY", "LLY",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG",
    # Consumer
    "WMT", "TGT", "COST", "MCD", "SBUX", "NKE", "DIS", "AMZN", "HD", "LOW",
    # ETFs
    "SPY", "QQQ", "IWM", "DIA", "VTI",
]

def init_everything(database: Database[Mapping[str, Any]]):
    for i, stock in enumerate(STOCKS):
        try:
            print(f"Fetching {stock}...")
            data = MassiveService.get_stock_market_data(stock)
            formattedData = MassiveService.format_stock_market_data(data)
            print(f"{stock}: {len(formattedData)} records")
            if len(formattedData) > 0:
                database[DatabaseService.DEFAULT_TABLE].insert_many(formattedData)
                print(f"{stock} saved")
        except Exception as e:
            print(f"Error fetching {stock}: {e}")

        # 5 calls/min = 1 call per 12s, wait after every call except the last
        if i < len(STOCKS) - 1:
            print("Waiting 12s (rate limit)...")
            time.sleep(12)

def handling_data(database: Database[Mapping[str, Any]]):
    print(list(database[DatabaseService.DEFAULT_TABLE].find()))

def main():
    database = DatabaseService.init_db()
    if database is None:
        return
    if database[DatabaseService.DEFAULT_TABLE].find_one() is None:
        print("The collection does not exists")
        init_everything(database)
    handling_data(database)


if __name__ == "__main__":
    # cProfile.run('main()')
    main()

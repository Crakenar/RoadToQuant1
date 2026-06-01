import random
import time
from datetime import datetime, timedelta

from FirstTimer.Entities import MassiveApiInterface
from FirstTimer.Services import DatabaseService
import json

def load_stocks_json():
    try:
        with open('Config/stocks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The file 'Config/stocks.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")


def generate_fake_candle(stock_id: str, timestamp: int, base_price: float) -> MassiveApiInterface.AggData:
    change = random.uniform(-0.5, 0.5)
    open_price = round(base_price + change, 2)
    high = round(open_price + random.uniform(0, 1.5), 2)
    low = round(open_price - random.uniform(0, 1.5), 2)
    close = round(random.uniform(low, high), 2)
    volume = random.randint(100, 100000)
    transactions = random.randint(10, 500)
    vwap = round((high + low + close) / 3, 4)

    return MassiveApiInterface.AggData(
        timestamp=timestamp,
        number_of_transactions=transactions,
        volume=volume,
        close=close,
        high=high,
        low=low,
        open=open_price,
        vwap=vwap,
        stock_id=stock_id,
    )

def generate_fake_data(batch_size: int = 10000, total_rows: int = 10_000_000):
    database = DatabaseService.init_db()
    collection = database[DatabaseService.DEFAULT_TABLE]
    # idk let put it there for now
    collection.create_index("timestamp")
    collection.create_index("stock_id")

    stocks = load_stocks_json()['stocks']
    # base prices per stock
    base_prices = {stock: random.uniform(50, 1000) for stock in stocks}
    # start from 2020-01-01, one candle per minute
    start_ts = int(datetime(2020, 1, 1).timestamp() * 1000)
    minute_ms = 60 * 1000

    inserted = 0
    batch = []

    print(f"Generating {total_rows:,} rows...")

    while inserted < total_rows:
        for stock in stocks:
            ts = start_ts + (inserted // len(stocks)) * minute_ms
            base_prices[stock] += random.uniform(-2, 2)  # random walk
            base_prices[stock] = max(1, base_prices[stock])  # prevent negative
            batch.append(generate_fake_candle(stock, ts, base_prices[stock]))

        if len(batch) >= batch_size:
            collection.insert_many(batch)
            inserted += len(batch)
            batch = []
            print(f"Inserted {inserted:,} / {total_rows:,}")

    if batch:
        collection.insert_many(batch)
        inserted += len(batch)

    print(f"Done. Total inserted: {inserted:,}")
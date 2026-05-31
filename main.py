import cProfile
from pymongo.synchronous.database import Database
from typing import Any, Mapping
from FirstTimer.Services import MassiveService, DatabaseService

def init_everything(database: Database[Mapping[str, Any]]):
    try:
        data = MassiveService.get_stock_market_data()
        formattedData = MassiveService.format_stock_market_data(data)
        print(len(formattedData))
        if len(formattedData) > 0:
            database[DatabaseService.DEFAULT_TABLE].insert_many(formattedData)
    except Exception as e:
        print("An error occurred:", e)

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

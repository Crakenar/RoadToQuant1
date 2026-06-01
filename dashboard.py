import pandas as pd
from FirstTimer.Services import DatabaseService
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


def display_transactions(df_hour: pd.DataFrame, df_dow: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    df_hour.plot(kind='bar', x='hour', y='number_of_transactions', ax=axes[0], color='steelblue', legend=False)
    axes[0].set_title('Transactions by Hour')
    axes[0].set_xlabel('Hour')
    axes[0].set_ylabel('Total Transactions')

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df_dow.set_index('day_of_week').reindex(day_order).plot(kind='bar', y='number_of_transactions', ax=axes[1], color='coral', legend=False)
    axes[1].set_title('Transactions by Day of Week')
    axes[1].set_xlabel('Day')

    plt.tight_layout()
    plt.show()


def fetch_hour_data(collection):
    pipeline = [
        {"$project": {"hour": {"$hour": {"$toDate": "$timestamp"}}, "number_of_transactions": 1}},
        {"$group": {"_id": "$hour", "total": {"$sum": "$number_of_transactions"}}},
        {"$sort": {"_id": 1}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline, allowDiskUse=True))) \
        .rename(columns={"_id": "hour", "total": "number_of_transactions"})

def fetch_dow_data(collection):
    day_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
    pipeline = [
        {"$project": {"day_of_week": {"$dayOfWeek": {"$toDate": "$timestamp"}}, "number_of_transactions": 1}},
        {"$group": {"_id": "$day_of_week", "total": {"$sum": "$number_of_transactions"}}},
        {"$sort": {"_id": 1}},
        # {"created_at": {
        # "$gte": ISODate("2010-04-29T00:00:00.000Z"),
        # "$lt": ISODate("2010-05-01T00:00:00.000Z")}
        # }
    ]
    df = pd.DataFrame(list(collection.aggregate(pipeline, allowDiskUse=True))) \
        .rename(columns={"_id": "day_of_week", "total": "number_of_transactions"})
    df['day_of_week'] = df['day_of_week'].map(day_map)
    return df

def main():
    database = DatabaseService.init_db()
    collection = database[DatabaseService.DEFAULT_TABLE]

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_hour = executor.submit(fetch_hour_data, collection)
        future_dow = executor.submit(fetch_dow_data, collection)
        df_hour = future_hour.result()
        df_dow = future_dow.result()

    display_transactions(df_hour, df_dow)


if __name__ == "__main__":
    main()
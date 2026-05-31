import pandas as pd

from FirstTimer.Services import DatabaseService
import matplotlib.pyplot as plt


def display_transactions_by_hour(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # by hour
    df.groupby('hour')['number_of_transactions'].sum().plot(
        kind='bar', ax=axes[0], color='steelblue'
    )
    axes[0].set_title('Transactions by Hour')
    axes[0].set_xlabel('Hour')
    axes[0].set_ylabel('Total Transactions')

    # by day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df.groupby('day_of_week')['number_of_transactions'].sum() \
        .reindex(day_order).plot(kind='bar', ax=axes[1], color='coral')
    axes[1].set_title('Transactions by Day of Week')
    axes[1].set_xlabel('Day')

    plt.tight_layout()
    plt.show()

def main():
    print('hello dashboard')
    database = DatabaseService.init_db()
    data = list(database[DatabaseService.DEFAULT_TABLE].find({}, {"_id": 0}))

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()

    display_transactions_by_hour(df)

if __name__ == "__main__":
    main()

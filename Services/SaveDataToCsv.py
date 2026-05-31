import csv

def save_market_data_to_csv(data: list) -> None:
    with open('market_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'number_of_transactions', 'volume', 'close',
                      'high', 'low', 'open', 'vwap']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
from FirstTimer.Helpers import GenerateFakeData
from concurrent.futures import ThreadPoolExecutor

NUM_THREADS = 8

def main():
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for i in range(NUM_THREADS):
            executor.submit(GenerateFakeData.generate_fake_data, batch_size=100000, total_rows=1_000_000_000 // NUM_THREADS)

if __name__ == "__main__":
    main()
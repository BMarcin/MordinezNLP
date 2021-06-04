import time

from tqdm.auto import tqdm

if __name__ == '__main__':
    for _ in tqdm(range(100)):
        time.sleep(0.05)
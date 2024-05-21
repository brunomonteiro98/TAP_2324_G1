import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np
np.random.seed(9487)

n_workers = multiprocessing.cpu_count() // 2

n_samples = 40000000
xs = np.random.uniform(low=0.0, high=10, size=(n_samples)).astype(int)
ys = np.random.uniform(low=0.0, high=10, size=(n_samples)).astype(int)
zs = np.random.uniform(low=0.0, high=10, size=(n_samples)).astype(int)

def process_samples(xs, ys, zs):
    processed = []
    with tqdm(total=len(xs), ascii=True) as pbar:
        for x, y, z in zip(xs, ys, zs):
            processed.append(process_sample(x, y, z))
            pbar.update(1)
    return processed

def process_sample(x, y, z):
    processed = max(x, y, z)
    return processed

if __name__ == "__main__":
    results = [None] * n_workers
    with Pool(processes=n_workers) as pool:
        for i in range(n_workers):
            batch_start = (len(xs) // n_workers) * i
            if i == n_workers - 1:
                batch_end = len(xs)
            else:
                batch_end = (len(xs) // n_workers) * (i + 1)

            batch_x = xs[batch_start: batch_end]
            batch_y = ys[batch_start: batch_end]
            batch_z = zs[batch_start: batch_end]
            results[i] = pool.apply_async(process_samples, (batch_x, batch_y, batch_z))

        pool.close()
        pool.join()

    processed = []
    for result in results:
        processed += result.get()
        print(results)
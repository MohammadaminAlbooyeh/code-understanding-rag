import time


def benchmark():
    print("Running benchmarks...")
    start = time.time()
    time.sleep(0.1)
    elapsed = time.time() - start
    print(f"Benchmark complete in {elapsed:.2f}s")


if __name__ == "__main__":
    benchmark()

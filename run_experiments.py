import random
import time
import statistics
import matplotlib.pyplot as plt


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def generate_array(size):
    return [random.randint(0, 100000) for _ in range(size)]


def generate_nearly_sorted_array(size, noise_percent):
    arr = list(range(size))
    num_swaps = int(size * noise_percent / 100)

    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


def measure_time(sort_func, arr):
    start = time.time()
    sort_func(arr.copy())
    end = time.time()
    return end - start


def run_experiment(sizes, repetitions, algorithms, array_generator):
    avg_results = {name: [] for name, _ in algorithms}
    std_results = {name: [] for name, _ in algorithms}

    for size in sizes:
        print(f"\nArray size: {size}")
        results = {name: [] for name, _ in algorithms}

        for _ in range(repetitions):
            base_array = array_generator(size)

            for name, func in algorithms:
                t = measure_time(func, base_array)
                results[name].append(t)

        for name in results:
            avg_time = statistics.mean(results[name])
            std_dev = statistics.stdev(results[name])

            avg_results[name].append(avg_time)
            std_results[name].append(std_dev)

            print(f"{name}: avg={avg_time:.6f}, std={std_dev:.6f}")

    return avg_results, std_results


def plot_results(sizes, avg_results, std_results, title, filename):
    plt.figure()

    for name in avg_results:
        plt.errorbar(
            sizes,
            avg_results[name],
            yerr=std_results[name],
            marker='o',
            capsize=5,
            label=name
        )

    plt.title(title)
    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()


if __name__ == "__main__":
    sizes = [100, 500, 1000, 3000]
    repetitions = 5

    algorithms = [
        ("Bubble", bubble_sort),
        ("Insertion", insertion_sort),
        ("Quick", quick_sort)
    ]

    print("=== Part B: Random Arrays ===")
    avg_results_random, std_results_random = run_experiment(
        sizes,
        repetitions,
        algorithms,
        generate_array
    )

    plot_results(
        sizes,
        avg_results_random,
        std_results_random,
        "Runtime Comparison (Random Arrays)",
        "result1.png"
    )

    print("\n=== Part C: Nearly Sorted Arrays (5% Noise) ===")
    avg_results_nearly, std_results_nearly = run_experiment(
        sizes,
        repetitions,
        algorithms,
        lambda size: generate_nearly_sorted_array(size, 5)
    )

    plot_results(
        sizes,
        avg_results_nearly,
        std_results_nearly,
        "Runtime Comparison (Nearly Sorted, 5% Noise)",
        "result2.png"
    )
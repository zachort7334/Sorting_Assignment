import random
import time
import statistics
import argparse
import matplotlib.pyplot as plt


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break

    return a


def insertion_sort(arr):
    a = arr.copy()

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1

        a[j + 1] = key

    return a


def quick_sort(arr):
    a = arr.copy()

    def sort(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr

        pivot = sub_arr[len(sub_arr) // 2]
        left = [x for x in sub_arr if x < pivot]
        middle = [x for x in sub_arr if x == pivot]
        right = [x for x in sub_arr if x > pivot]

        return sort(left) + middle + sort(right)

    return sort(a)


def generate_random_array(size):
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
    start = time.perf_counter()
    sorted_arr = sort_func(arr)
    end = time.perf_counter()

    if sorted_arr != sorted(arr):
        raise ValueError("Sorting algorithm returned incorrect result.")

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
                runtime = measure_time(func, base_array)
                results[name].append(runtime)

        for name in results:
            avg_time = statistics.mean(results[name])
            std_dev = statistics.stdev(results[name]) if len(results[name]) > 1 else 0.0

            avg_results[name].append(avg_time)
            std_results[name].append(std_dev)

            print(f"{name}: avg={avg_time:.6f}, std={std_dev:.6f}")

    return avg_results, std_results


def plot_results(sizes, avg_results, std_results, title, filename):
    plt.figure(figsize=(10, 6))

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
    plt.close()


def get_algorithms(selected_ids):
    mapping = {
        1: ("Bubble Sort", bubble_sort),
        3: ("Insertion Sort", insertion_sort),
        5: ("Quick Sort", quick_sort)
    }

    algorithms = []

    for algo_id in selected_ids:
        if algo_id not in mapping:
            raise ValueError(
                f"Invalid algorithm ID: {algo_id}. "
                f"Use only 1 (Bubble), 3 (Insertion), 5 (Quick)."
            )
        algorithms.append(mapping[algo_id])

    return algorithms


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Compare Bubble Sort, Insertion Sort, and Quick Sort."
    )

    parser.add_argument(
        "-a", "--algorithms",
        nargs="+",
        type=int,
        required=True,
        help="Algorithm IDs: 1=Bubble Sort, 3=Insertion Sort, 5=Quick Sort"
    )

    parser.add_argument(
        "-s", "--sizes",
        nargs="+",
        type=int,
        required=True,
        help="Array sizes, for example: 100 500 1000 3000"
    )

    parser.add_argument(
        "-e", "--experiment",
        type=int,
        required=True,
        choices=[0, 1, 2, 3],
        help=(
            "Experiment type: "
            "0=run all three experiments, "
            "1=random arrays, "
            "2=nearly sorted 5%% noise, "
            "3=nearly sorted 20%% noise"
        )
    )

    parser.add_argument(
        "-r", "--repetitions",
        type=int,
        required=True,
        help="Number of repetitions for each array size"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    algorithms = get_algorithms(args.algorithms)
    sizes = args.sizes
    repetitions = args.repetitions

    if args.experiment == 0 or args.experiment == 1:
        print("=== Experiment 1: Random Arrays ===")
        avg_results, std_results = run_experiment(
            sizes=sizes,
            repetitions=repetitions,
            algorithms=algorithms,
            array_generator=generate_random_array
        )
        plot_results(
            sizes=sizes,
            avg_results=avg_results,
            std_results=std_results,
            title="Runtime Comparison (Random Arrays)",
            filename="result1.png"
        )
        print("Saved graph as result1.png")

    if args.experiment == 0 or args.experiment == 2:
        print("\n=== Experiment 2: Nearly Sorted Arrays (5% Noise) ===")
        avg_results, std_results = run_experiment(
            sizes=sizes,
            repetitions=repetitions,
            algorithms=algorithms,
            array_generator=lambda size: generate_nearly_sorted_array(size, 5)
        )
        plot_results(
            sizes=sizes,
            avg_results=avg_results,
            std_results=std_results,
            title="Runtime Comparison (Nearly Sorted, 5% Noise)",
            filename="result2.png"
        )
        print("Saved graph as result2.png")

    if args.experiment == 0 or args.experiment == 3:
        print("\n=== Experiment 3: Nearly Sorted Arrays (20% Noise) ===")
        avg_results, std_results = run_experiment(
            sizes=sizes,
            repetitions=repetitions,
            algorithms=algorithms,
            array_generator=lambda size: generate_nearly_sorted_array(size, 20)
        )
        plot_results(
            sizes=sizes,
            avg_results=avg_results,
            std_results=std_results,
            title="Runtime Comparison (Nearly Sorted, 20% Noise)",
            filename="result3.png"
        )
        print("Saved graph as result3.png")
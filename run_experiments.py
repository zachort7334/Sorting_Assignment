import random
import time

# ===== Sorting Algorithms =====

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
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# ===== Utility =====

def generate_array(size):
    return [random.randint(0, 100000) for _ in range(size)]


def measure_time(sort_func, arr):
    start = time.time()
    sort_func(arr.copy())
    end = time.time()
    return end - start


# ===== Main (temporary) =====

if __name__ == "__main__":
    sizes = [100, 500, 1000]

    for size in sizes:
        arr = generate_array(size)
        print(f"\nArray size: {size}")

        for name, func in [
            ("Bubble", bubble_sort),
            ("Insertion", insertion_sort),
            ("Quick", quick_sort)
        ]:
            t = measure_time(func, arr)
            print(f"{name}: {t:.6f} sec")

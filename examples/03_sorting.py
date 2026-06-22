import random
import time


def bubble_sort(arr):
    n = len(arr)
    data = arr[:]
    swaps = 0
    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
    return data, swaps


def insertion_sort(arr):
    data = arr[:]
    swaps = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
            swaps += 1
        data[j + 1] = key
    return data, swaps


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def benchmark(name, func, data):
    start = time.perf_counter()
    result = func(data)
    elapsed = (time.perf_counter() - start) * 1000
    sorted_result = result[0] if isinstance(result, tuple) else result
    ok = sorted_result == sorted(data)
    swaps = result[1] if isinstance(result, tuple) else "-"
    print(f"  {name:<16} {elapsed:6.2f} ms  swaps={swaps}  ok={ok}")
    return sorted_result


def main():
    random.seed(42)
    sizes = [100, 500, 1000]

    for size in sizes:
        data = [random.randint(0, 10000) for _ in range(size)]
        print(f"\n--- n={size} ---")
        benchmark("bubble_sort", bubble_sort, data)
        benchmark("insertion_sort", insertion_sort, data)
        benchmark("merge_sort", lambda d: (merge_sort(d), "-"), data)
        benchmark("quick_sort", lambda d: (quick_sort(d), "-"), data)


if __name__ == "__main__":
    main()

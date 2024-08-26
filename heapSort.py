import random
import time

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def generate_random_array(count):
    return [random.randint(1, count+1) for _ in range(count+1)]

count = 10000  # 배열의 크기
arr = generate_random_array(count)
#print("Original array:", arr)

start_time = time.time()
heap_sort(arr)
end_time = time.time()

#print("Sorted array:", arr)
print(f"Time taken to sort: {end_time - start_time:.6f} seconds")

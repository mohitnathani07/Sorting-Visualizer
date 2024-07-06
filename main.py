import matplotlib.pyplot as plt
import random
import numpy as np
import streamlit as st
import time

st.title("Sorting Visualizer")
n = st.slider("select the number of elements in the array", 5, 30, step=5)
speed = st.select_slider(
    "Select the speed",
    options=["slow", "medium", "fast"]
)
select_algorithm = st.selectbox(
    "Select the Sorting Algorithm",
    ("Bubble Sort", "Merge Sort", "Selection Sort","Insertion Sort")
)
start = st.button("Start")

numbers = [random.randint(10, 1000) for i in range(n)]
x = np.arange(0, n)
sorted_indices = []
plot_placeholder = st.empty()


def bubble_sort(numbers):
    color_list = ['blue'] * n
    plot_numbers(numbers, color_list)
    for i in range(n):
        for j in range(n - i - 1):
            color_list = ['blue'] * n
            if i != 0:
                for color in range(n - i, n):
                    color_list[color] = "green"
            color_list[j] = 'red'
            plot_numbers(numbers, color_list)
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

    color_list = ['green' for k in range(n)]
    plot_numbers(numbers, color_list)

    return numbers


def plot_numbers(numbers, color_list):
    plt.clf()  # Clear the previous plot
    plt.bar(x, numbers, color=color_list)
    plot_placeholder.pyplot(plt.gcf())
    time.sleep(speed_dic[speed])


def merge_visualizer(numbers, list_of_index, n, speed):
    def mergeSort(a, index):
        if len(a) == 1:
            return a
        mid = len(a) // 2
        left = mergeSort(a[:mid], index[:mid])
        right = mergeSort(a[mid:], index[mid:])
        return merge(left, right, index)

    def merge(left, right, index):
        i = j = 0
        merged = []
        sorted_indices = []

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                sorted_indices.append(index[i])
                i += 1
            else:
                merged.append(right[j])
                sorted_indices.append(index[len(left) + j])
                j += 1

            # Update the plot
            color_list = ['blue'] * n
            for idx in sorted_indices:
                color_list[idx] = 'green'
            if i < len(left):
                color_list[index[i]] = 'red'
            if j < len(right):
                color_list[index[len(left) + j]] = 'red'
            plot_numbers(numbers, color_list)

        while i < len(left):
            merged.append(left[i])
            sorted_indices.append(index[i])
            i += 1
            color_list = ['blue'] * n
            for idx in sorted_indices:
                color_list[idx] = 'green'
            if i < len(left):
                color_list[index[i]] = 'red'
            plot_numbers(numbers, color_list)

        while j < len(right):
            merged.append(right[j])
            sorted_indices.append(index[len(left) + j])
            j += 1
            color_list = ['blue'] * n
            for idx in sorted_indices:
                color_list[idx] = 'green'
            if j < len(right):
                color_list[index[len(left) + j]] = 'red'
            plot_numbers(numbers, color_list)

        # Update the original array and color list
        for idx, val in zip(sorted_indices, merged):
            numbers[idx] = val
            color_list[idx] = 'green'  # Mark as sorted

        return merged

    ans = mergeSort(numbers, list_of_index)

    color_list = ['green'] * n
    plot_numbers(numbers, color_list)
    return ans


def selection_sort(numbers):
    for i in range(len(numbers)):
        color_list = ["blue"] * len(numbers)
        for color in range(i):
            color_list[color] = "green"
        plot_numbers(numbers, color_list)
        hold = i
        color_list[i] = "orange"
        min_element = numbers[i]
        for j in range(i + 1, len(numbers)):
            color_list[j] = "red"
            plot_numbers(numbers, color_list)
            if numbers[j] < min_element:
                min_element = numbers[j]
                hold = j

        color_list[hold] = "orange"
        plot_numbers(numbers, color_list)
        numbers[i], numbers[hold] = numbers[hold], numbers[i]
        color_list[i], color_list[hold] = color_list[hold], color_list[i]
        plot_numbers(numbers, color_list)

    return numbers


def insertion_sort(array):
    length = len(array)
    temp = []
    for step in range(1, len(array)):
        key = array[step]
        j = step - 1
        color_list = ["blue"] * length
        for t in temp:
            color_list[t] = "green"

        while j >= 0 and key < array[j]:
            color_list = ["blue"] * length
            for t in temp:

                color_list[t] = "green"
            color_list[j] = "orange"
            plot_numbers(numbers, color_list)
            array[j + 1] = array[j]
            j = j - 1

        # Place key at after the element just smaller than it.
        array[j + 1] = key
        temp.append(j+1)
    for i in range(len(color_list)):
        color_list[i] = "green"
        plot_numbers(numbers, color_list)

    return numbers

speed_dic = {"slowest": 0.7,
             "medium": 0.3,
             "fast": 0.2,
             }


if start:
    st.write("Initial array:", f"{numbers}")
    ans = []
    if select_algorithm == "Bubble Sort":
        ans = bubble_sort(numbers)
    elif select_algorithm == "Merge Sort":
        ans = merge_visualizer(numbers, x, n, speed_dic[speed])
    elif select_algorithm == "Selection Sort":
        ans = selection_sort(numbers)
    elif select_algorithm == "Insertion Sort":
        ans = insertion_sort(numbers)
    # Sorted array
    color_list = ['green'] * n
    plot_numbers(ans, color_list)
    st.write("Sorted array:", f"{ans}")

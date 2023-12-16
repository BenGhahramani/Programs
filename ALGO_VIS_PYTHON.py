import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def generate_data(data_size=50):
    return random.sample(range(1, 100), data_size)

def create_window():
    window = tk.Tk()
    window.title("Sorting Algorithm Visualizer")

    data = generate_data()

    def draw_data(data, colorArray):
        ax.clear()
        ax.bar(range(len(data)), data, color=colorArray)
        canvas.draw_idle()

    def bubble_sort(data, draw_data):
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    draw_data(data, ['green' if x == j or x == j + 1 else 'red' for x in range(len(data))])
                    window.update_idletasks()

    def quick_sort(data, draw_data, start, end):
        if start >= end:
            return

        pivot = data[end]
        index = start

        for i in range(start, end):
            if data[i] < pivot:
                data[i], data[index] = data[index], data[i]
                index += 1
                draw_data(data, ['green' if x == i or x == index else 'red' for x in range(len(data))])
                window.update_idletasks()

        data[index], data[end] = data[end], data[index]
        quick_sort(data, draw_data, start, index - 1)
        quick_sort(data, draw_data, index + 1, end)

    def insertion_sort(data, draw_data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
                data[j + 1] = key
                draw_data(data, ['green' if x == j or x == i else 'red' for x in range(len(data))])
                window.update_idletasks()

    def selection_sort(data, draw_data):
        for i in range(len(data)):
            min_idx = i
            for j in range(i+1, len(data)):
                if data[min_idx] > data[j]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            draw_data(data, ['green' if x == i or x == min_idx else 'red' for x in range(len(data))])
            window.update_idletasks()

    def merge_sort(data, draw_data):
        merge_sort_alg(data, 0, len(data) - 1, draw_data)

    def merge_sort_alg(data, left, right, draw_data):
        if left < right:
            middle = (left + right) // 2
            merge_sort_alg(data, left, middle, draw_data)
            merge_sort_alg(data, middle + 1, right, draw_data)
            merge(data, left, middle, right, draw_data)

    def merge(data, left, middle, right, draw_data):
        left_part = data[left:middle + 1]
        right_part = data[middle + 1:right + 1]

        left_idx, right_idx = 0, 0
        for data_idx in range(left, right + 1):
            if left_idx < len(left_part) and (right_idx >= len(right_part) or left_part[left_idx] <= right_part[right_idx]):
                data[data_idx] = left_part[left_idx]
                left_idx += 1
            else:
                data[data_idx] = right_part[right_idx]
                right_idx += 1

            draw_data(data, ['green' if x == data_idx else 'red' for x in range(len(data))])
            window.update_idletasks()

    def heap_sort(data, draw_data):
        n = len(data)

        for i in range(n // 2 - 1, -1, -1):
            heapify(data, n, i, draw_data)

        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            heapify(data, i, 0, draw_data)

    def heapify(data, n, i, draw_data):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and data[largest] < data[left]:
            largest = left

        if right < n and data[largest] < data[right]:
            largest = right

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            heapify(data, n, largest, draw_data)

            draw_data(data, ['green' if x == largest or x == i else 'red' for x in range(len(data))])
            window.update_idletasks()

    # Start sorting
    def start_sorting():
        if alg_menu.get() == 'Bubble Sort':
            bubble_sort(data, draw_data)
        elif alg_menu.get() == 'Quick Sort':
            quick_sort(data, draw_data, 0, len(data) - 1)
        elif alg_menu.get() == 'Insertion Sort':
            insertion_sort(data, draw_data)
        elif alg_menu.get() == 'Selection Sort':
            selection_sort(data, draw_data)
        elif alg_menu.get() == 'Merge Sort':
            merge_sort(data, draw_data)
        elif alg_menu.get() == 'Heap Sort':
            heap_sort(data, draw_data)
        draw_data(data, ['green' for x in range(len(data))])

    def reset_data():
        nonlocal data
        data = generate_data()
        draw_data(data, ['red' for x in range(len(data))])

    # Create a toolbar frame
    toolbar = tk.Frame(window)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    # Dropdown to select the sorting algorithm
    alg_label = tk.Label(toolbar, text="Algorithm: ")
    alg_label.pack(side=tk.LEFT, padx=10, pady=5)

    alg_menu = ttk.Combobox(toolbar, values=['Bubble Sort', 'Quick Sort', 'Insertion Sort', 'Selection Sort', 'Merge Sort', 'Heap Sort'])
    alg_menu.pack(side=tk.LEFT, padx=5, pady=5)
    alg_menu.current(0)

    # Sort button
    sort_button = tk.Button(toolbar, text="Sort", command=start_sorting)
    sort_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Reset button
    reset_button = tk.Button(toolbar, text="Reset", command=reset_data)
    reset_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Canvas to draw the sorting visualizations
    canvas_frame = tk.Frame(window)
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Matplotlib setup for the graph
    fig, ax = plt.subplots()
    ax.set_title("Sorting Visualization")
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Draw the initial unsorted data
    draw_data(data, ['red' for x in range(len(data))])

    def on_closing():
        """Function to be called when window is closed."""
        window.quit()  # First quit the mainloop
        window.destroy()  # Then destroy the window

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()

create_window()
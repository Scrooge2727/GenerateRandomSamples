import tkinter as tk
from tkinter import Label, Entry, Button, Listbox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_samples():
    n_elements = int(elements_entry.get())
    mean_time = float(mean_time_entry.get())

    lmbda = 1 / mean_time
    sigma = 0.3 * mean_time

    uniform_sample = np.random.rand(n_elements)
    exponential_sample = -np.log(1 - uniform_sample) / lmbda
    normal_sample = np.random.normal(mean_time, sigma, n_elements)

    # Очищаем Listbox перед добавлением новых значений
    listbox.delete(0, tk.END)

    for i in range(n_elements):
        listbox.insert(tk.END, f"Uniform: {uniform_sample[i]:.4f}, Exponential: {exponential_sample[i]:.4f}, Normal: {normal_sample[i]:.4f}")

    min_uniform, max_uniform = uniform_sample.min(), uniform_sample.max()
    min_exponential, max_exponential = exponential_sample.min(), exponential_sample.max()
    min_normal, max_normal = normal_sample.min(), normal_sample.max()

    num_intervals = int(5 * np.log10(n_elements))

    interval_width_uniform = (max_uniform - min_uniform) / num_intervals
    interval_width_exponential = (max_exponential - min_exponential) / num_intervals
    interval_width_normal = (max_normal - min_normal) / num_intervals

    intervals = np.linspace(min_uniform, max_uniform, num_intervals + 1)

    hist_uniform, _ = np.histogram(uniform_sample, bins=intervals)
    hist_exponential, _ = np.histogram(exponential_sample, bins=intervals)
    hist_normal, _ = np.histogram(normal_sample, bins=intervals)

    hist_uniform = hist_uniform / n_elements
    hist_exponential = hist_exponential / n_elements
    hist_normal = hist_normal / n_elements

    # Создаем значения плотности вероятности для нормального распределения
    x = np.linspace(min_normal, max_normal, num_intervals)
    normal_pdf = np.exp(-(x - mean_time)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))

    ax.clear()
    ax.plot(intervals[:-1], hist_uniform, label='Uniform', linestyle='-', marker='o')
    ax.set_xlabel('Интервалы')
    ax.set_ylabel('Частота')
    ax.set_title('График выборок - Uniform')
    ax.legend()

    ax2.clear()
    ax2.plot(intervals[:-1], hist_exponential, label='Exponential', linestyle='-', marker='o')
    ax2.set_xlabel('Интервалы')
    ax2.set_ylabel('Частота')
    ax2.set_title('График выборок - Exponential')
    ax2.legend()

    ax3.clear()
    ax3.plot(x, normal_pdf, label='Normal', linestyle='-', marker='o', color='red')
    ax3.set_xlabel('Интервалы')
    ax3.set_ylabel('Плотность вероятности')
    ax3.set_title('График выборок - Normal')
    ax3.legend()

    canvas.draw()

# Создаем главное окно
root = tk.Tk()
root.title("Генерация выборок")

# Создаем метки и поля для ввода параметров
Label(root, text="Количество элементов:").grid(row=0, column=0)
elements_entry = Entry(root)
elements_entry.grid(row=0, column=1)
Label(root, text="Среднее время:").grid(row=1, column=0)
mean_time_entry = Entry(root)
mean_time_entry.grid(row=1, column=1)

# Создаем кнопку для генерации выборок
generate_button = Button(root, text="Генерировать выборки", command=generate_samples)
generate_button.grid(row=2, column=0, columnspan=2)

# Создаем фигуры и холсты для отображения графиков
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=3)

# Создаем Listbox для вывода значений
listbox = Listbox(root, width=60, height=10)
listbox.grid(row=0, column=3, rowspan=3)

root.mainloop()

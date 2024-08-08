import tkinter as tk
from tkinter import Label, Entry, Button
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

    # Создаем приближенные значения плотности вероятности для нормального распределения
    x = np.linspace(min_normal, max_normal, num_intervals)
    normal_pdf = np.exp(-(x - mean_time)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))

    ax.clear()
    ax.bar(intervals[:-1], hist_uniform, width=interval_width_uniform, alpha=0.5, label='Uniform')
    ax.bar(intervals[:-1], hist_exponential, width=interval_width_exponential, alpha=0.5, label='Exponential')
    ax.plot(x, normal_pdf, label='Normal', color='red')
    ax.legend()
    ax.set_xlabel('Интервалы')
    ax.set_ylabel('Частота')
    ax.set_title('Гистограмма выборок')
    canvas.draw()

# Создаем главное окно
root = tk.Tk()
root.title("Генерация выборок")

# Создаем метки и поля для ввода параметров
Label(root, text="Количество элементов:").pack()
elements_entry = Entry(root)
elements_entry.pack()
Label(root, text="Среднее время:").pack()
mean_time_entry = Entry(root)
mean_time_entry.pack()

# Создаем кнопку для генерации выборок
generate_button = Button(root, text="Генерировать выборки", command=generate_samples)
generate_button.pack()

# Создаем фигуру и холст для отображения графика
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()

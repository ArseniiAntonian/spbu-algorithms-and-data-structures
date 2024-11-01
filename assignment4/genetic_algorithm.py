import tkinter as tk
from tkinter import ttk
import numpy as np
import random

def f(x, y):
    return 100 * (y - x**2)**2 + (1 - x)**2

BOUNDS = (-50, 50)

def initialize_population(size, bounds):
    return [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])) for _ in range(size)]

def select(population):
    selected = []
    for _ in range(len(population)):
        i, j = random.sample(range(len(population)), 2)
        selected.append(min(population[i], population[j], key=lambda ind: f(ind[0], ind[1])))
    return selected

def crossingover(parent1, parent2, crossingover_prob):
    if random.random() < crossingover_prob:
        alpha = random.random()
        child1 = (alpha * parent1[0] + (1 - alpha) * parent2[0], alpha * parent1[1] + (1 - alpha) * parent2[1])
        child2 = ((1 - alpha) * parent1[0] + alpha * parent2[0], (1 - alpha) * parent1[1] + alpha * parent2[1])
        return child1, child2
    return parent1, parent2

def mutate(individual, bounds, mutation_prob):
    if random.random() < mutation_prob:
        individual = (
            individual[0] + random.uniform(-0.1, 0.1),
            individual[1] + random.uniform(-0.1, 0.1)
        )
        individual = (np.clip(individual[0], bounds[0], bounds[1]), np.clip(individual[1], bounds[0], bounds[1]))
    return individual

def genetic_algorithm(bounds, generations, population_size, crossingover_prob, mutation_prob, elite_size, display_callback):
    population = initialize_population(population_size, bounds)
    for generation in range(generations):
    
        population = sorted(population, key=lambda ind: f(ind[0], ind[1]))

        elite = population[:elite_size]

        selected = select(population[elite_size:])

        next_population = elite.copy()
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[(i + 1) % len(selected)]
            child1, child2 = crossingover(parent1, parent2, crossingover_prob)
            next_population.append(mutate(child1, bounds, mutation_prob))
            next_population.append(mutate(child2, bounds, mutation_prob))

        population = next_population[:population_size]
        
        best_individual = min(population, key=lambda ind: f(ind[0], ind[1]))
        display_callback(generation, best_individual, f(best_individual[0], best_individual[1]))
        if(f(best_individual[0], best_individual[1]) < 0.001): break

    best_individual = min(population, key=lambda ind: f(ind[0], ind[1]))
    return best_individual, f(best_individual[0], best_individual[1])


class GeneticAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генетический алгоритм для функции Розенброка")

        self.create_widgets()

    def create_widgets(self):
        parameter_frame = tk.LabelFrame(self.root, text="Параметры", padx=10, pady=10)
        parameter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(parameter_frame, text="Размер популяции:").grid(row=0, column=0, sticky="e")
        self.population_entry = tk.Entry(parameter_frame)
        self.population_entry.insert(0, "50")
        self.population_entry.grid(row=0, column=1)

        tk.Label(parameter_frame, text="Число поколений:").grid(row=1, column=0, sticky="e")
        self.generations_entry = tk.Entry(parameter_frame)
        self.generations_entry.insert(0, "100")
        self.generations_entry.grid(row=1, column=1)

        tk.Label(parameter_frame, text="Вероятность кроссовера:").grid(row=2, column=0, sticky="e")
        self.crossingover_entry = tk.Entry(parameter_frame)
        self.crossingover_entry.insert(0, "0.8")
        self.crossingover_entry.grid(row=2, column=1)

        tk.Label(parameter_frame, text="Вероятность мутации:").grid(row=3, column=0, sticky="e")
        self.mutation_entry = tk.Entry(parameter_frame)
        self.mutation_entry.insert(0, "0.02")
        self.mutation_entry.grid(row=3, column=1)

        tk.Label(parameter_frame, text="Размер элиты:").grid(row=4, column=0, sticky="e")
        self.elite_entry = tk.Entry(parameter_frame)
        self.elite_entry.insert(0, "5")
        self.elite_entry.grid(row=4, column=1)

        self.run_button = tk.Button(self.root, text="Запустить алгоритм", command=self.run_algorithm)
        self.run_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        result_frame = tk.LabelFrame(self.root, text="Результаты", padx=10, pady=10)
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(result_frame, text="Лучшее решение:").grid(row=0, column=0, sticky="w")
        self.best_solution_label = tk.Label(result_frame, text="")
        self.best_solution_label.grid(row=0, column=1, sticky="w")

        tk.Label(result_frame, text="Значение функции:").grid(row=1, column=0, sticky="w")
        self.best_value_label = tk.Label(result_frame, text="")
        self.best_value_label.grid(row=1, column=1, sticky="w")

        self.population_table = ttk.Treeview(self.root, columns=("Generation", "Best X", "Best Y", "Fitness"), show="headings")
        self.population_table.heading("Generation", text="Поколение")
        self.population_table.heading("Best X", text="Лучший X")
        self.population_table.heading("Best Y", text="Лучший Y")
        self.population_table.heading("Fitness", text="Функция")
        self.population_table.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    def display_generation(self, generation, best_individual, fitness):
        self.population_table.insert("", "end", values=(generation, f"{best_individual[0]:.4f}", f"{best_individual[1]:.4f}", f"{fitness:.4f}"))

    def run_algorithm(self):
        self.population_table.delete(*self.population_table.get_children())

        population_size = int(self.population_entry.get())
        generations = int(self.generations_entry.get())
        crossingover_prob = float(self.crossingover_entry.get())
        mutation_prob = float(self.mutation_entry.get())
        elite_size = int(self.elite_entry.get())

        best_solution, best_fitness = genetic_algorithm(
            BOUNDS, generations, population_size, crossingover_prob, mutation_prob, elite_size, self.display_generation
        )

        self.best_solution_label.config(text=f"X: {best_solution[0]:.4f}, Y: {best_solution[1]:.4f}")
        self.best_value_label.config(text=f"{best_fitness:.4f}")

root = tk.Tk()
app = GeneticAlgorithmApp(root)
root.mainloop()

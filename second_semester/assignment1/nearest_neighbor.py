import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def nearest_neighbor(G: nx.DiGraph, start_node):
    visited = set([start_node])
    path = [start_node]
    total_distance = 0
    v = start_node

    while len(visited) < len(G.nodes):
        neighbors = list(G.neighbors(v))
        min_distance = float('inf')
        nearest_node = None

        for u in neighbors:
            if u not in visited and G[v][u]['weight'] < min_distance:
                min_distance = G[v][u]['weight']
                nearest_node = u

        if nearest_node is None:
            return "Нет решения", path, total_distance

        path.append(nearest_node)
        visited.add(nearest_node)
        total_distance += min_distance
        v = nearest_node

    if G.has_edge(v, start_node):
        total_distance += G[v][start_node]['weight']
        path.append(start_node)
    else:
        return "Невозможно вернуться", path, total_distance

    return path, total_distance

G = None

def build_graph_from_input():
    global G
    G = nx.DiGraph()
    input_text = text_edges.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showerror("Ошибка", "Пожалуйста, введите данные для графа.")
        return
    lines = input_text.splitlines()
    edges = []
    for line in lines:
        parts = line.split(',')
        if len(parts) != 3:
            messagebox.showerror("Ошибка", f"Неверный формат строки:\n{line}")
            return
        u = parts[0].strip()
        v = parts[1].strip()
        try:
            weight = float(parts[2].strip())
        except ValueError:
            messagebox.showerror("Ошибка", f"Неверный вес в строке:\n{line}")
            return
        edges.append((u, v, weight))
    G.add_weighted_edges_from(edges)
    messagebox.showinfo("Успех", "Граф успешно создан!")
    draw_graph(G, path_edges=None)

def draw_graph(G, path_edges=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='blue', node_size=400)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=2, arrows=True, arrowsize=10, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color='white')
    if path_edges:
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, ax=ax,
            edge_color='red', width=2, arrows=True, connectionstyle='arc3,rad=0.1'
        )
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
    ax.set_axis_off()

    for widget in frame_canvas.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_algorithm():
    global G
    if G is None or len(G.nodes) == 0:
        messagebox.showerror("Ошибка", "Граф не создан. Сначала создайте граф.")
        return
    start_node = entry_start.get().strip()
    if start_node == "":
        messagebox.showerror("Ошибка", "Введите начальный узел.")
        return
    if start_node not in G.nodes:
        messagebox.showerror("Ошибка", f"Узел '{start_node}' отсутствует в графе.")
        return
    result = nearest_neighbor(G, start_node)
    if isinstance(result[0], str):  # Обнаружена ошибка
        path, distance = result[1], result[2]
        result_message = f"Ошибка: {result[0]}\nПуть: {' -> '.join(path)}\nОбщая длина: {distance}"
    else:
        path, distance = result
        result_message = f"Путь: {' -> '.join(path)}, общая длина: {distance}"
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result_message)
    path_edges = list(zip(path[:-1], path[1:])) if len(path) > 1 else None
    draw_graph(G, path_edges)

root = tk.Tk()
root.title("Интерфейс алгоритма ближайшего соседа")
root.geometry("1920x1080")

frame_input = tk.Frame(root)
frame_input.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

lbl_edges = tk.Label(frame_input, text="Введите ребра графа (формат: узел1, узел2, вес):", font=("Arial", 12))
lbl_edges.pack(anchor=tk.W, padx=5, pady=5)

text_edges = tk.Text(frame_input, height=8, font=("Arial", 12))
text_edges.pack(fill=tk.X, padx=5, pady=5)
example = "a, b, 3\na, c, 5\nb, c, 2\nc, a, 4\nc, b, 8\nd, a, 1\nc, d, 7"
text_edges.insert(tk.END, example)

btn_create = tk.Button(frame_input, text="Создать граф", font=("Arial", 12), command=build_graph_from_input)
btn_create.pack(padx=5, pady=5)

frame_canvas = tk.Frame(root)
frame_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

lbl_start = tk.Label(frame_controls, text="Начальный узел:", font=("Arial", 12))
lbl_start.pack(side=tk.LEFT, padx=5, pady=5)

entry_start = tk.Entry(frame_controls, font=("Arial", 12))
entry_start.pack(side=tk.LEFT, padx=5, pady=5)
entry_start.insert(0, "a")

btn_run = tk.Button(frame_controls, text="Выполнить алгоритм", font=("Arial", 12), command=run_algorithm)
btn_run.pack(side=tk.LEFT, padx=5, pady=5)

text_result = tk.Text(frame_controls, height=4, font=("Arial", 12))
text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()

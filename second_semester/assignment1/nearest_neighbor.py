import sys
import random
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QLabel, QLineEdit, QMessageBox, QHBoxLayout, QSpinBox
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen
import networkx as nx


class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.G = nx.DiGraph()
        self.node_positions = {}
        self.last_clicked_node = None
        self.use_knn = False
        self.K = 2

    def initUI(self):
        layout = QVBoxLayout()

        self.graph_area = GraphArea(self)
        layout.addWidget(self.graph_area)

        controls_layout = QHBoxLayout()
        self.label_start = QLabel("Начальный узел:")
        controls_layout.addWidget(self.label_start)

        self.entry_start = QLineEdit()
        controls_layout.addWidget(self.entry_start)

        self.btn_run = QPushButton("Выполнить алгоритм")
        self.btn_run.clicked.connect(self.run_algorithm)
        controls_layout.addWidget(self.btn_run)

        self.btn_toggle_knn = QPushButton("Вкл k-NN")
        self.btn_toggle_knn.clicked.connect(self.toggle_knn)
        controls_layout.addWidget(self.btn_toggle_knn)

        self.spin_k = QSpinBox()
        self.spin_k.setMinimum(1)
        self.spin_k.setValue(2)
        self.spin_k.valueChanged.connect(self.update_k)
        controls_layout.addWidget(QLabel("K:"))
        controls_layout.addWidget(self.spin_k)

        layout.addLayout(controls_layout)

        graph_gen_layout = QHBoxLayout()
        self.spin_nodes = QSpinBox()
        self.spin_nodes.setMinimum(3)
        self.spin_nodes.setMaximum(100)
        self.spin_nodes.setValue(10)
        graph_gen_layout.addWidget(QLabel("Число узлов:"))
        graph_gen_layout.addWidget(self.spin_nodes)

        self.btn_generate_graph = QPushButton("Создать случайный граф")
        self.btn_generate_graph.clicked.connect(self.generate_random_graph)
        graph_gen_layout.addWidget(self.btn_generate_graph)

        layout.addLayout(graph_gen_layout)

        self.text_result = QTextEdit()
        self.text_result.setReadOnly(True)
        layout.addWidget(self.text_result)

        self.setLayout(layout)
        self.setWindowTitle("Алгоритм ближайшего соседа / k-NN")
        self.resize(1200, 800)

    def add_node(self, x, y):
        node_name = f"N{len(self.G.nodes) + 1}"
        self.G.add_node(node_name)
        self.node_positions[node_name] = (x, y)
        self.graph_area.update()

    def add_edge(self, node1, node2):
        if node1 == node2:
            return
        weight = random.randint(1, 20)
        self.G.add_edge(node1, node2, weight=weight)
        self.graph_area.update()

    def generate_random_graph(self):
        self.G.clear()
        self.node_positions.clear()
        self.graph_area.update()

        num_nodes = self.spin_nodes.value()
        probability = 0.7
        width, height = 800, 500

        for i in range(num_nodes):
            x, y = random.randint(50, width - 50), random.randint(50, height - 50)
            node_name = f"N{i+1}"
            self.G.add_node(node_name)
            self.node_positions[node_name] = (x, y)

        for node1 in self.G.nodes:
            for node2 in self.G.nodes:
                if node1 != node2 and random.random() < probability:
                    weight = random.randint(1, 20)
                    self.G.add_edge(node1, node2, weight=weight)

        self.graph_area.update()

    def run_algorithm(self):
        if not self.G.nodes:
            QMessageBox.critical(self, "Ошибка", "Граф не создан.")
            return

        start_node = self.entry_start.text().strip()
        if start_node not in self.G.nodes:
            QMessageBox.critical(self, "Ошибка", "Введите корректный начальный узел.")
            return

        start_time = time.time()
        if self.use_knn:
            path, distance = self.knn_algorithm(start_node)
            method = f"k-NN (k={self.K})"
        else:
            path, distance = self.nearest_neighbor(start_node)
            method = "Nearest Neighbor"
        elapsed_time = (time.time() - start_time) * 1000  

        if distance == float('inf'):
            result_message = f"{method}: Путь не найден. Время выполнения: {elapsed_time:.2f} мс."
        else:
            result_message = (
                f"{method}: {' -> '.join(path)}, Общая длина: {distance}, "
                f"Время выполнения: {elapsed_time:.6f} мс."
            )

        self.text_result.append(result_message)
        self.graph_area.update()

    def knn_algorithm(self, start_node):
        visited = {start_node}
        path = [start_node]
        total_distance = 0
        v = start_node

        while len(visited) < len(self.G.nodes):
            neighbors = sorted(
                [(u, self.G[v][u]['weight']) for u in self.G.neighbors(v) if u not in visited],
                key=lambda x: x[1]
            )

            if not neighbors:
                return path, float('inf')

            candidates = neighbors[:self.K]

            best_choice = None
            best_total_weight = float('inf')

            for candidate, edge_weight in candidates:
                temp_visited = visited.copy()
                temp_visited.add(candidate)
                temp_path_weight = edge_weight

                for next_neighbor in self.G.neighbors(candidate):
                    if next_neighbor not in temp_visited:
                        temp_path_weight += self.G[candidate][next_neighbor]['weight']
                        break  

                if temp_path_weight < best_total_weight:
                    best_total_weight = temp_path_weight
                    best_choice = candidate

            chosen_node = best_choice
            min_weight = self.G[v][chosen_node]['weight']

            path.append(chosen_node)
            visited.add(chosen_node)
            total_distance += min_weight
            v = chosen_node

        return path, total_distance

    def nearest_neighbor(self, start_node):
        visited = {start_node}
        path = [start_node]
        total_distance = 0
        v = start_node

        while len(visited) < len(self.G.nodes):
            neighbors = [(u, self.G[v][u]['weight']) for u in self.G.neighbors(v) if u not in visited]

            if not neighbors:
                return path, float('inf')

            chosen_node, min_weight = min(neighbors, key=lambda x: x[1])
            path.append(chosen_node)
            visited.add(chosen_node)
            total_distance += min_weight
            v = chosen_node

        return path, total_distance

    def toggle_knn(self):
        self.use_knn = not self.use_knn
        self.btn_toggle_knn.setText("Выкл k-NN" if self.use_knn else "Вкл k-NN")

    def update_k(self, value):
        self.K = value


class GraphArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(800, 500)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for (u, v, weight) in self.parent.G.edges(data='weight'):
            x1, y1 = self.parent.node_positions[u]
            x2, y2 = self.parent.node_positions[v]
            painter.drawLine(x1, y1, x2, y2)
            painter.drawText((x1 + x2) // 2, (y1 + y2) // 2, str(weight))

        for node, (x, y) in self.parent.node_positions.items():
            painter.setPen(QPen(Qt.black, 2))
            painter.drawEllipse(QPointF(x, y), 20, 20)
            painter.drawText(x - 10, y + 5, node)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        for node, (nx, ny) in self.parent.node_positions.items():
            if (nx - x) ** 2 + (ny - y) ** 2 <= 400:
                if self.parent.last_clicked_node:
                    self.parent.add_edge(self.parent.last_clicked_node, node)
                    self.parent.last_clicked_node = None
                else:
                    self.parent.last_clicked_node = node
                return

        self.parent.add_node(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())

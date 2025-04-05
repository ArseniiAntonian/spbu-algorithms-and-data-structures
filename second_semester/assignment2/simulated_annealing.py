import sys, random, time, math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen
import networkx as nx

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.G = nx.DiGraph()
        self.node_positions = {}
        self.last_clicked_node = None
        self.use_cauchy = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.graph_area = GraphArea(self)
        layout.addWidget(self.graph_area)

        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Метод:"))
        self.algo_group = QButtonGroup(self)
        self.radio_annealing = QRadioButton("Имитация отжига")
        self.radio_nn = QRadioButton("Ближайший сосед")
        self.radio_k_nn = QRadioButton("К ближайших соседей")
        self.radio_annealing.setChecked(True)
        self.algo_group.addButton(self.radio_annealing)
        self.algo_group.addButton(self.radio_nn)
        self.algo_group.addButton(self.radio_k_nn)
        algo_layout.addWidget(self.radio_annealing)
        algo_layout.addWidget(self.radio_nn)
        algo_layout.addWidget(self.radio_k_nn)
        
        self.chk_cauchy = QCheckBox("Отжиг Коши")
        algo_layout.addWidget(self.chk_cauchy)
        layout.addLayout(algo_layout)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Начальный узел:"))
        self.entry_start = QLineEdit()
        controls_layout.addWidget(self.entry_start)

        self.btn_run = QPushButton("Выполнить алгоритм")
        self.btn_run.clicked.connect(self.run_algorithm)
        controls_layout.addWidget(self.btn_run)
        layout.addLayout(controls_layout)

        
        graph_gen_layout = QHBoxLayout()
        self.spin_nodes = QSpinBox(minimum=3, maximum=100, value=10)
        graph_gen_layout.addWidget(QLabel("Число узлов:"))
        graph_gen_layout.addWidget(self.spin_nodes)
        self.btn_generate_graph = QPushButton("Создать случайный граф")
        self.btn_generate_graph.clicked.connect(self.generate_random_graph)
        graph_gen_layout.addWidget(self.btn_generate_graph)
        layout.addLayout(graph_gen_layout)

        
        hyper_group = QGroupBox("Гиперпараметры алгоритмов")
        hyper_form = QFormLayout()
        
        self.spin_T = QDoubleSpinBox()
        self.spin_T.setRange(1, 10000)
        self.spin_T.setDecimals(2)
        self.spin_T.setValue(1000)
        hyper_form.addRow("T:", self.spin_T)

        self.spin_Tmin = QDoubleSpinBox()
        self.spin_Tmin.setRange(0.0001, 100)
        self.spin_Tmin.setDecimals(4)
        self.spin_Tmin.setValue(0.001)
        hyper_form.addRow("Tmin:", self.spin_Tmin)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setRange(0.9, 1.0)
        self.spin_a.setSingleStep(0.001)
        self.spin_a.setDecimals(3)
        self.spin_a.setValue(0.995)
        hyper_form.addRow("alpha:", self.spin_a)

        self.spin_k = QSpinBox()
        self.spin_k.setRange(1, 100)
        self.spin_k.setValue(3)
        hyper_form.addRow("K:", self.spin_k)

        hyper_group.setLayout(hyper_form)
        layout.addWidget(hyper_group)

        self.text_result = QTextEdit(readOnly=True)
        layout.addWidget(self.text_result)

        self.setLayout(layout)
        self.setWindowTitle("Алгоритм имитации отжига")
        self.resize(1200, 800)

    def generate_random_graph(self):
        self.G.clear()
        self.node_positions.clear()
        for i in range(self.spin_nodes.value()):
            node_name = f"N{i+1}"
            x, y = random.randint(50,750), random.randint(50,450)
            self.G.add_node(node_name)
            self.node_positions[node_name] = (x, y)
        for u in self.G.nodes:
            for v in self.G.nodes:
                if u != v and random.random() < 0.8:
                    self.G.add_edge(u, v, weight=random.randint(1,20))
        self.graph_area.update()

    def run_algorithm(self):
        start_node = self.entry_start.text().strip()
        if start_node not in self.G.nodes:
            QMessageBox.critical(self, "Ошибка", "Введите корректный начальный узел.")
            return

        start_time = time.time()

        if self.radio_annealing.isChecked():
            path, dist = self.simulated_annealing(start_node, self.chk_cauchy.isChecked())
            method = "Отжиг (Коши)" if self.chk_cauchy.isChecked() else "Отжиг (обычный)"
        elif self.radio_nn.isChecked():
            path, dist = self.nearest_neighbor(start_node)
            method = "Ближайший сосед"
        elif self.radio_k_nn.isChecked():
            path, dist = self.k_nearest_neighbors(start_node)
            method = "К ближайших соседей"
        else:
            path, dist = [], float('inf')
            method = "Неизвестный метод"

        elapsed = (time.time() - start_time) * 1000
        if dist == float('inf'):
            res = f"{method}: Путь не найден. ({elapsed:.2f} ms)"
        else:
            res = f"{method}: {'->'.join(path)} | Длина: {dist} | {elapsed:.2f} ms"

        self.text_result.append(res)

    def nearest_neighbor(self, start):
        visited, path, v, dist = {start}, [start], start, 0
        while len(visited) < len(self.G):
            neighbors = [(u, self.G[v][u]['weight']) for u in self.G[v] if u not in visited]
            if not neighbors:
                return path, float('inf')
            u, w = min(neighbors, key=lambda x: x[1])
            path.append(u)
            visited.add(u)
            dist += w
            v = u
        return path, dist

    def k_nearest_neighbors(self, start):
        best_path = None
        best_dist = float('inf')
        k = self.spin_k.value()
        nodes_to_try = list(self.G.nodes)
    
        if k < len(nodes_to_try):
            nodes_to_try = random.sample(nodes_to_try, k)
        for node in nodes_to_try:
            path, dist = self.nearest_neighbor(node)
            if dist < best_dist:
                best_path = path
                best_dist = dist
        if best_path and start in best_path:
            i = best_path.index(start)
            best_path = best_path[i:] + best_path[:i]
        return best_path, best_dist

    def simulated_annealing(self, start, use_cauchy):
        
        nodes, dist = self.nearest_neighbor(start)
        T = self.spin_T.value()
        Tmin = self.spin_Tmin.value()
        a = self.spin_a.value()
        while T > Tmin:
            i, j = sorted(random.sample(range(len(nodes)), 2))
            n = nodes[:]
            n[i:j] = n[i:j][::-1]
            d = self.path_distance(n)
            delta = d - dist
            if delta < 0 or math.exp(-delta/T) > random.random():
                nodes, dist = n, d
            T = T/(1+0.01 * T) if use_cauchy else T * a
        if start in nodes:
            i = nodes.index(start)
            nodes = nodes[i:] + nodes[:i]
        return nodes, dist

    def path_distance(self, path):
        total = 0
        for i in range(len(path)-1):
            if self.G.has_edge(path[i], path[i+1]):
                total += self.G[path[i]][path[i+1]]['weight']
            else:
                return float('inf')
        return total

    def toggle_cauchy(self, state):
        self.use_cauchy = state == Qt.Checked

    def add_node(self, x, y):
        node_name = f"N{len(self.G.nodes) + 1}"
        self.G.add_node(node_name)
        self.node_positions[node_name] = (x, y)
        self.graph_area.update()

    def add_edge(self, node1, node2):
        if node1 != node2:
            self.G.add_edge(node1, node2, weight=random.randint(1,20))
            self.graph_area.update()

class GraphArea(QWidget):
    def __init__(self, p):
        super().__init__(p)
        self.p = p
        self.setMinimumSize(800,500)

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        for u, v, d in self.p.G.edges(data='weight'):
            x1, y1 = self.p.node_positions[u]
            x2, y2 = self.p.node_positions[v]
            qp.drawLine(x1, y1, x2, y2)
            qp.drawText((x1+x2)//2, (y1+y2)//2, str(d))
        for n, (x, y) in self.p.node_positions.items():
            qp.setPen(QPen(Qt.black, 2))
            qp.drawEllipse(QPointF(x, y), 20, 20)
            qp.drawText(x-10, y+5, n)

    def mousePressEvent(self, e):
        x, y = e.x(), e.y()
        for n, (nx, ny) in self.p.node_positions.items():
            if (nx - x)**2 + (ny - y)**2 <= 400:
                if self.p.last_clicked_node:
                    self.p.add_edge(self.p.last_clicked_node, n)
                    self.p.last_clicked_node = None
                else:
                    self.p.last_clicked_node = n
                return
        self.p.add_node(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GraphApp()
    w.show()
    sys.exit(app.exec_())

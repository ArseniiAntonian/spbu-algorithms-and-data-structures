import sys
import random
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

BOUNDS = (-50, 50)

def f(x, y):
    return 100 * (y - x**2)**2 + (1 - x)**2

def initialize_swarm(size, bounds):
    swarm = []
    for _ in range(size):
        position = [random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])]
        velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        swarm.append({
            'position': position,
            'velocity': velocity,
            'best_position': position,
            'best_value': f(*position)
        })
    return swarm

def update_velocity(particle, global_best_position, inertia, cognitive, social):
    new_velocity = []
    for i in range(len(particle['position'])):
        r1 = random.random()
        r2 = random.random()
        cognitive_component = cognitive * r1 * (particle['best_position'][i] - particle['position'][i])
        social_component = social * r2 * (global_best_position[i] - particle['position'][i])
        new_velocity.append(inertia * particle['velocity'][i] + cognitive_component + social_component)
    particle['velocity'] = new_velocity

def update_position(particle, bounds):
    new_position = []
    for i in range(len(particle['position'])):
        new_pos = particle['position'][i] + particle['velocity'][i]
        new_pos = max(bounds[0], min(new_pos, bounds[1]))
        new_position.append(new_pos)
    particle['position'] = new_position

def particle_swarm_optimization(swarm_size, bounds, inertia, cognitive, social, max_iter, modify_inertia):
    swarm = initialize_swarm(swarm_size, bounds)
    global_best_position = min(swarm, key=lambda p: p['best_value'])['position']
    global_best_value = f(*global_best_position)
    
    for _ in range(max_iter):
        if modify_inertia:
            inertia = inertia * 0.99

        for particle in swarm:
            update_velocity(particle, global_best_position, inertia, cognitive, social)
            update_position(particle, bounds)
            
            current_value = f(*particle['position'])
            if current_value < particle['best_value']:
                particle['best_value'] = current_value
                particle['best_position'] = particle['position']
            
            if current_value < global_best_value:
                global_best_value = current_value
                global_best_position = particle['position']

    return global_best_position, global_best_value, swarm

class PSOInterface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.swarm = None

    def initUI(self):
        self.setWindowTitle("Роевой интеллект")
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        param_layout = QtWidgets.QFormLayout()
        self.inertia_input = QtWidgets.QLineEdit("0.5")
        self.cognitive_input = QtWidgets.QLineEdit("1.5")
        self.social_input = QtWidgets.QLineEdit("1.5")
        self.particle_count_input = QtWidgets.QSpinBox()
        self.particle_count_input.setRange(10, 1000)
        self.particle_count_input.setValue(30)
        self.iter_count_input = QtWidgets.QSpinBox()
        self.iter_count_input.setRange(1, 1000)
        self.iter_count_input.setValue(100)
        param_layout.addRow("Коэф. текущей скорости:", self.inertia_input)
        param_layout.addRow("Коэф. собственного лучшего значения:", self.cognitive_input)
        param_layout.addRow("Коэф. глобального лучшего значения:", self.social_input)
        param_layout.addRow("Количество частиц:", self.particle_count_input)
        param_layout.addRow("Количество итераций:", self.iter_count_input)
        self.create_particles_btn = QtWidgets.QPushButton("Создать частицы")
        self.create_particles_btn.clicked.connect(self.create_particles)
        self.calculate_btn = QtWidgets.QPushButton("Рассчитать")
        self.calculate_btn.clicked.connect(self.run_pso)
        self.modify_inertia_checkbox = QtWidgets.QCheckBox("Использовать модификацию коэффицента сжатия")
        self.result_display = QtWidgets.QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(100)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.addWidget(self.create_particles_btn)
        control_layout.addWidget(self.calculate_btn)
        main_layout.addLayout(param_layout)
        main_layout.addWidget(self.modify_inertia_checkbox)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(QtWidgets.QLabel("Результаты"))
        main_layout.addWidget(self.result_display)
        main_layout.addWidget(self.canvas)

    def create_particles(self):
        swarm_size = self.particle_count_input.value()
        self.swarm = initialize_swarm(swarm_size, BOUNDS)
        self.result_display.setText("Частицы созданы.")
        self.update_canvas(self.swarm)

    def run_pso(self):
        inertia = float(self.inertia_input.text())
        cognitive = float(self.cognitive_input.text())
        social = float(self.social_input.text())
        swarm_size = self.particle_count_input.value()
        max_iter = self.iter_count_input.value()
        modify_inertia = self.modify_inertia_checkbox.isChecked()
        best_position, best_value, self.swarm = particle_swarm_optimization(swarm_size, BOUNDS, inertia, cognitive, social, max_iter, modify_inertia)
        self.result_display.setText(f"Лучшее решение:\nX[0] = {best_position[0]}\nX[1] = {best_position[1]}\n\nЗначение функции: {best_value}")
        self.update_canvas(self.swarm)

    def update_canvas(self, swarm):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if swarm:
            x_vals = [p['position'][0] for p in swarm]
            y_vals = [p['position'][1] for p in swarm]
            ax.plot(x_vals, y_vals, 'k.')
        ax.set_title("Решения")
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        self.canvas.draw()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PSOInterface()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

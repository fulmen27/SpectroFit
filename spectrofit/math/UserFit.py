import numpy as np
from lmfit import Model
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QPushButton, QCheckBox
from PySide2.QtCore import Qt, SIGNAL, QObject


class UserFit(QWidget):
    def __init__(self, master, data):
        self.master = master
        self.window = QWidget()
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])

        self.solution = dict()

        self.model = None

        self.set_ui()
        self.window.show()

    def set_ui(self):

        self.layout = QGridLayout()
        mod_layout = QHBoxLayout()

        label = QLabel("Model : ")
        label.setFixedHeight(10)
        mod_layout.addWidget(label)
        self.mod = QLineEdit()
        mod_layout.addWidget(self.mod)
        mod_btn = QPushButton("OK")
        mod_btn.clicked.connect(self._train_model)
        mod_layout.addWidget(mod_btn)
        mod_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(mod_layout, 0, 0, Qt.AlignTop)
        self.window.setLayout(self.layout)

    def _train_model(self):
        model = self.mod.text()
        print(model)
        print(type(model))


class MixFit(QWidget):

    def __init__(self, master, data):
        self.master = master
        self.window = QWidget()
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])

        self.solution = dict()
        self.checkbox_states = dict()
        self.checkbox_states_fit_method = dict()
        self.parameters = dict()

        self.model = None

        self.set_ui()
        self.window.show()

    def set_ui(self):
        lay = QGridLayout(self.window)
        label = QLabel("Model to choose : ")
        lay.addWidget(label, 0, 0)
        label = QLabel("parameters : ")
        lay.addWidget(label, 0, 1)
        for i, (key, text) in enumerate(
                (
                        ("l", "linear"),
                        ("e", "exponential"),
                        ("de", "double exponential"),
                        ("lor", "lorentz"),
                        ("dlor", "double lorentz"),
                        ("gaus", "gaussian"),
                        ("dgaus", "double gaussian"),
                )
        ):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            lay.addWidget(checkbox, i + 1, 0)
            self.checkbox_states[key] = checkbox
            self.parameters[key] = QLineEdit()
            lay.addWidget(self.parameters[key], i+1, 1)

        label = QLabel("Method : ")
        lay.addWidget(label, 0, 2)
        for i, (key, text) in enumerate(
                (
                        ("leastsq", "Levenberg-Marquardt (default)"),
                        ("least_squares", "Least Squares"),
                        ("differential_evolution", "differential evolution"),
                        ("brute", "brute force (not to use)"),
                        ("basinhopping", "basinhopping"),
                        ("ampgo", "Adaptive Memory Programming for Global Optimization"),
                        ("nelder", "Nelder-Mead"),
                        ("lbfgsb", "L-BFGS-B"),
                        ("powell", "Powell"),
                        ("cg", "Conjugate-Gradient"),
                        ("newton", "Newton-CG"),
                        ("cobyla", "Cobyla"),
                        ("bfgs", "BFGS"),
                        ("tnc", "Truncated Newton"),
                        ("trust-ncg", "Newton-CG trust-region"),
                        ("trust-exact", "nearly exact trust-region"),
                        ("trust-krylov", "Newton GLTR trust-region"),
                        ("trust-constr", "trust-region for constrained optimization"),
                        ("dogleg", "Dog-leg trust-region"),
                        ("slsqp", "Sequential Linear Squares Programming"),
                        ("emcee", "Maximum likelihood via Monte-Carlo Markov Chain"),
                        ("shgo", "Simplicial Homology Global Optimization"),
                        ("dual_annealing", "Dual Annealing optimization"),
                )
        ):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            lay.addWidget(checkbox, i + 1, 2)
            self.checkbox_states_fit_method[key] = checkbox

        process_fit = QPushButton("Process")
        QObject.connect(process_fit, SIGNAL('clicked()'), self._on_process_fit)
        lay.addWidget(process_fit, i+2, 3)

    def _on_process_fit(self):
        s = 0
        method = ""
        for key, value in self.checkbox_states_fit_method.items():
            if value.isChecked():
                method = key
                s += 1

        print("you want to use method : {}".format(method))
        function_to_use = []
        if s > 1:
            self.master.error("To many method are checked. Check only one box")
        else:
            for key, value in self.checkbox_states.items():
                if value.isChecked():
                    function_to_use.append(key)

            print("you want to use functions : {}".format(function_to_use))

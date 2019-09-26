import numpy as np
from lmfit import Model
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt


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


from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PySide2.QtGui import QPen
from PySide2.QtCore import Qt

import spectrofit.math.mathFunction as mF
from spectrofit.ui.DoubleSlider import Slider
import numpy as np


class SliderLinear(QWidget):
    def __init__(self, master, curve, data):
        super().__init__()
        self.master = master
        self.curve = curve
        self.data = data
        self.lim = self.curve["lim"]
        self.pen = QPen(Qt.yellow, 0.01, Qt.DashDotLine)

        self.slider_b = Slider()
        self.slider_a = Slider()

        self.set_ui_lo()

        self.show()

    def set_ui_lo(self):
        lay = QGridLayout()

        self.slider_b.setTickPosition(QSlider.TicksBelow)
        self.slider_a.setTickPosition(QSlider.TicksBelow)

        self.slider_b.setTickInterval(0.01)
        self.slider_b.setSingleStep(0.01)
        self.slider_b.setTracking(True)

        self.slider_a.setTickInterval(0.001)
        self.slider_a.setSingleStep(0.001)
        self.slider_a.setTracking(True)

        self.slider_b.setMinimum(-100)
        self.slider_b.setMaximum(100)

        self.slider_a.setMinimum(-100)
        self.slider_a.setMaximum(100)

        self.slider_b.setOrientation(Qt.Horizontal)
        self.slider_a.setOrientation(Qt.Horizontal)

        label_title = QLabel("Parametrize Linear {}".format(self.curve["count"]))
        label1 = QLabel("Parameter b : ")
        label2 = QLabel("Parameter a : ")

        lay.addWidget(label_title, 0, 0, 1, 0, Qt.AlignCenter)
        lay.addWidget(label1, 1, 0)
        lay.addWidget(label2, 3, 0)

        # Add slider b and surronding widget to layout
        lay.addWidget(self.slider_b, 1, 3)
        slider_b_hbox = QHBoxLayout()
        label_b_minimum = QLabel("min : -100")
        label_b_actual = QLabel("Actual : ")
        self.label_b_actual_val = QLabel("0")
        label_b_maximum = QLabel("max : 100")
        self.slider_b.doubleValueChanged.connect(self._on_change_b)
        slider_b_hbox.addWidget(label_b_minimum, Qt.AlignLeft)
        slider_b_hbox.addWidget(label_b_actual, Qt.AlignCenter)
        slider_b_hbox.addWidget(self.label_b_actual_val, Qt.AlignCenter)
        slider_b_hbox.addWidget(label_b_maximum, Qt.AlignRight)
        lay.addLayout(slider_b_hbox, 2, 3)

        # Add slider a and surronding widget to layout
        lay.addWidget(self.slider_a, 3, 3)
        slider_a_hbox = QHBoxLayout()
        label_a_minimum = QLabel("min : -100")
        label_a_actual = QLabel("actual : ")
        self.label_a_actual_val = QLabel("0")
        label_a_maximum = QLabel("max : 100")
        self.slider_a.doubleValueChanged.connect(self._on_change_a)
        slider_a_hbox.addWidget(label_a_minimum, Qt.AlignLeft)
        slider_a_hbox.addWidget(label_a_actual, Qt.AlignCenter)
        slider_a_hbox.addWidget(self.label_a_actual_val, Qt.AlignCenter)
        slider_a_hbox.addWidget(label_a_maximum, Qt.AlignRight)
        v1 = QVBoxLayout()
        v1.addLayout(slider_a_hbox)
        v1.addStretch()
        lay.addLayout(v1, 4, 3)

        # buttons

        button1_b = QPushButton("<<")
        button1_b.clicked.connect(self.b_fast_minus)
        button2_b = QPushButton("<")
        button2_b.clicked.connect(self.b_slow_minus)
        button3_b = QPushButton(">>")
        button3_b.clicked.connect(self.b_fast_add)
        button4_b = QPushButton(">")
        button4_b.clicked.connect(self.b_slow_add)
        lay.addWidget(button1_b, 1, 1)
        lay.addWidget(button2_b, 1, 2)
        lay.addWidget(button4_b, 1, 4)
        lay.addWidget(button3_b, 1, 5)

        button1_a = QPushButton("<<")
        button1_a.clicked.connect(self.a_fast_minus)
        button2_a = QPushButton("<")
        button2_a.clicked.connect(self.a_slow_minus)
        button3_a = QPushButton(">>")
        button3_a.clicked.connect(self.a_fast_add)
        button4_a = QPushButton(">")
        button4_a.clicked.connect(self.a_slow_add)
        lay.addWidget(button1_a, 3, 1)
        lay.addWidget(button2_a, 3, 2)
        lay.addWidget(button4_a, 3, 4)
        lay.addWidget(button3_a, 3, 5)

        self.setLayout(lay)

    def b_slow_add(self):
        self.slider_b.setValue(self.slider_b.value() + 0.001)
        self._on_change_b(self.slider_b.value())

    def b_fast_add(self):
        self.slider_b.setValue(self.slider_b.value() + 0.01)
        self._on_change_b(self.slider_b.value())

    def b_slow_minus(self):
        self.slider_b.setValue(self.slider_b.value() - 0.001)
        self._on_change_b(self.slider_b.value())

    def b_fast_minus(self):
        self.slider_b.setValue(self.slider_b.value() - 0.01)
        self._on_change_b(self.slider_b.value())

    def a_slow_add(self):
        self.slider_a.setValue(self.slider_a.value() + 0.001)
        self._on_change_a(self.slider_a.value())

    def a_fast_add(self):
        self.slider_a.setValue(self.slider_a.value() + 0.01)
        self._on_change_a(self.slider_a.value())

    def a_slow_minus(self):
        self.slider_a.setValue(self.slider_a.value() - 0.001)
        self._on_change_a(self.slider_a.value())

    def a_fast_minus(self):
        self.slider_a.setValue(self.slider_a.value() - 0.01)
        self._on_change_a(self.slider_a.value())

    def _on_change_b(self, event):
        self.label_b_actual_val.setNum(event)
        y = mF.model_linear(np.asarray(self.data),
                                [self.slider_a.value(), event])
        self.update_curves(y)

    def _on_change_a(self, event):
        self.label_a_actual_val.setNum(event)
        y = mF.model_linear(np.asarray(self.data),
                                [event, self.slider_b.value()])
        self.update_curves(y)

    def update_curves(self, y):
        self.curve["curve"].setData(self.data, y, pen=self.pen)
        self.master.curves[self.curve["name"]]["y"] = y
        self.master.update_all()

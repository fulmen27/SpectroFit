from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PySide2.QtGui import QPen
from PySide2.QtCore import Qt

import spectrofit.math.mathFunction as mF
from spectrofit.ui.DoubleSlider import Slider
import numpy as np


class SliderGaussian(QWidget):
    def __init__(self, master, curve, data):
        super().__init__()
        self.master = master
        self.curve = curve
        self.data = data
        self.lim = self.curve["lim"]
        self.pen = QPen(Qt.blue, 0.01, Qt.DashDotLine)

        self.slider_mu = Slider()
        self.slider_sigma = Slider()
        self.slider_add = Slider()

        self.set_ui_lo()

        self.show()

    def set_ui_lo(self):
        # Set up all Layout :

        lay = QGridLayout()

        self.slider_mu.setTickPosition(QSlider.TicksBelow)
        self.slider_sigma.setTickPosition(QSlider.TicksBelow)

        self.slider_mu.setTickInterval(0.01)
        self.slider_mu.setSingleStep(0.01)
        self.slider_mu.setTracking(True)

        self.slider_sigma.setTickInterval(0.001)
        self.slider_sigma.setSingleStep(0.001)
        self.slider_sigma.setTracking(True)

        self.slider_add.setTickInterval(0.001)
        self.slider_add.setSingleStep(0.001)
        self.slider_add.setTracking(True)

        self.slider_mu.setMinimum(self.lim[0])
        self.slider_mu.setMaximum(self.lim[1])

        self.slider_sigma.setMinimum(0)
        self.slider_sigma.setMaximum(10)

        self.slider_add.setMinimum(0)
        self.slider_add.setMaximum(10)

        self.slider_mu.setOrientation(Qt.Horizontal)
        self.slider_sigma.setOrientation(Qt.Horizontal)
        self.slider_add.setOrientation(Qt.Vertical)

        label_title = QLabel("Parametrize Gaussian {}".format(self.curve["count"]))
        label1 = QLabel("Parameter mu : ")
        label2 = QLabel("Parameter sigma : ")
        label3 = QLabel("Parameter add : ")

        lay.addWidget(label_title, 0, 0, 1, 0, Qt.AlignCenter)
        lay.addWidget(label1, 1, 0)
        lay.addWidget(label2, 3, 0)
        lay.addWidget(label3, 5, 0)

        # Add slider mu and surronding widget to layout
        lay.addWidget(self.slider_mu, 1, 3)
        slider_mu_hbox = QHBoxLayout()
        label_mu_minimum = QLabel("min : {}".format(self.lim[0]))
        label_mu_actual = QLabel("Actual : ")
        self.label_mu_actual_val = QLabel("0")
        label_mu_maximum = QLabel("max : {}".format(self.lim[1]))
        self.slider_mu.doubleValueChanged.connect(self._on_change_mu)
        slider_mu_hbox.addWidget(label_mu_minimum, Qt.AlignLeft)
        slider_mu_hbox.addWidget(label_mu_actual, Qt.AlignCenter)
        slider_mu_hbox.addWidget(self.label_mu_actual_val, Qt.AlignCenter)
        slider_mu_hbox.addWidget(label_mu_maximum, Qt.AlignRight)
        lay.addLayout(slider_mu_hbox, 2, 3)

        # Add slider sigma and surronding widget to layout
        lay.addWidget(self.slider_sigma, 3, 3)
        slider_sigma_hbox = QHBoxLayout()
        label_sigma_minimum = QLabel("min : 0")
        label_sigma_actual = QLabel("actual : ")
        self.label_sigma_actual_val = QLabel("0")
        label_sigma_maximum = QLabel("max : 10")
        self.slider_sigma.doubleValueChanged.connect(self._on_change_sigma)
        slider_sigma_hbox.addWidget(label_sigma_minimum, Qt.AlignLeft)
        slider_sigma_hbox.addWidget(label_sigma_actual, Qt.AlignCenter)
        slider_sigma_hbox.addWidget(self.label_sigma_actual_val, Qt.AlignCenter)
        slider_sigma_hbox.addWidget(label_sigma_maximum, Qt.AlignRight)
        v1 = QVBoxLayout()
        v1.addLayout(slider_sigma_hbox)
        v1.addStretch()
        lay.addLayout(v1, 4, 3)

        # Add slider add and surronding widget to layout
        lay.addWidget(self.slider_add, 5, 3, Qt.AlignCenter)
        slider_add_hbox = QHBoxLayout()
        label_add_minimum = QLabel("min : 0")
        label_add_actual = QLabel("actual : ")
        self.label_add_actual_val = QLabel("0")
        label_add_maximum = QLabel("max : 10")
        self.slider_add.doubleValueChanged.connect(self._on_change_add)
        slider_add_hbox.addWidget(label_add_minimum, Qt.AlignLeft)
        slider_add_hbox.addWidget(label_add_actual, Qt.AlignCenter)
        slider_add_hbox.addWidget(self.label_add_actual_val, Qt.AlignCenter)
        slider_add_hbox.addWidget(label_add_maximum, Qt.AlignRight)
        v1 = QVBoxLayout()
        v1.addLayout(slider_add_hbox)
        v1.addStretch()
        lay.addLayout(v1, 6, 3)

        # buttons

        button1_mu = QPushButton("<<")
        button1_mu.clicked.connect(self.mu_fast_minus)
        button2_mu = QPushButton("<")
        button2_mu.clicked.connect(self.mu_slow_minus)
        button3_mu = QPushButton(">>")
        button3_mu.clicked.connect(self.mu_fast_add)
        button4_mu = QPushButton(">")
        button4_mu.clicked.connect(self.mu_slow_add)
        lay.addWidget(button1_mu, 1, 1)
        lay.addWidget(button2_mu, 1, 2)
        lay.addWidget(button4_mu, 1, 4)
        lay.addWidget(button3_mu, 1, 5)

        button1_sigma = QPushButton("<<")
        button1_sigma.clicked.connect(self.sigma_fast_minus)
        button2_sigma = QPushButton("<")
        button2_sigma.clicked.connect(self.sigma_slow_minus)
        button3_sigma = QPushButton(">>")
        button3_sigma.clicked.connect(self.sigma_fast_add)
        button4_sigma = QPushButton(">")
        button4_sigma.clicked.connect(self.sigma_slow_add)
        lay.addWidget(button1_sigma, 3, 1)
        lay.addWidget(button2_sigma, 3, 2)
        lay.addWidget(button4_sigma, 3, 4)
        lay.addWidget(button3_sigma, 3, 5)

        button1_add = QPushButton("<<")
        button1_add.clicked.connect(self.add_fast_minus)
        button2_add = QPushButton("<")
        button2_add.clicked.connect(self.add_slow_minus)
        button3_add = QPushButton(">>")
        button3_add.clicked.connect(self.add_fast_add)
        button4_add = QPushButton(">")
        button4_add.clicked.connect(self.add_slow_add)
        lay.addWidget(button1_add, 5, 1)
        lay.addWidget(button2_add, 5, 2)
        lay.addWidget(button4_add, 5, 4)
        lay.addWidget(button3_add, 5, 5)

        self.emis = QCheckBox("Is it an Emission spectrum ?")
        lay.addWidget(self.emis, 0, 7, 0, 5, Qt.AlignCenter)

        self.setLayout(lay)

    def mu_slow_add(self):
        """
            @brief:
                on mean :
                add 0.001 to slider when clicking slow add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mu.setValue(self.slider_mu.value() + 0.001)
        self._on_change_mu(self.slider_mu.value())

    def mu_fast_add(self):
        """
            @brief:
                on mean :
                add 0.01 to slider when clicking fast add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mu.setValue(self.slider_mu.value() + 0.01)
        self._on_change_mu(self.slider_mu.value())

    def mu_slow_minus(self):
        """
            @brief:
                on mean :
                minus 0.001 to slider when clicking slow minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mu.setValue(self.slider_mu.value() - 0.001)
        self._on_change_mu(self.slider_mu.value())

    def mu_fast_minus(self):
        """
            @brief:
                on mean :
                minus 0.01 to slider when clicking fast minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mu.setValue(self.slider_mu.value() - 0.01)
        self._on_change_mu(self.slider_mu.value())

    def sigma_slow_add(self):
        """
            @brief:
                on sigma :
                add 0.001 to slider when clicking slow add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_sigma.setValue(self.slider_sigma.value() + 0.001)
        self._on_change_sigma(self.slider_sigma.value())

    def sigma_fast_add(self):
        """
            @brief:
                on sigma :
                add 0.01 to slider when clicking fast add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_sigma.setValue(self.slider_sigma.value() + 0.01)
        self._on_change_sigma(self.slider_sigma.value())

    def sigma_slow_minus(self):
        """
            @brief:
                on sigma :
                minus 0.001 to slider when clicking slow minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_sigma.setValue(self.slider_sigma.value() - 0.001)
        self._on_change_sigma(self.slider_sigma.value())

    def sigma_fast_minus(self):
        """

            @brief:
                on sigma :
                minus 0.01 to slider when clicking fast minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_sigma.setValue(self.slider_sigma.value() - 0.01)
        self._on_change_sigma(self.slider_sigma.value())

    def add_slow_add(self):
        """

        @brief:
            on add :
            add 0.001 to slider when clicking slow add button

        :parameter:
            self

        :return:
            None
        """
        self.slider_add.setValue(self.slider_add.value() + 0.001)
        self._on_change_add(self.slider_add.value())

    def add_fast_add(self):
        """

            @brief:
                on add :
                add 0.01 to slider when clicking fast add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_add.setValue(self.slider_add.value() + 0.01)
        self._on_change_add(self.slider_add.value())

    def add_slow_minus(self):
        """

             @brief:
                 on add :
                 minus 0.001 to slider when clicking slow minus button

             :parameter:
                 self

             :return:
                 None
         """
        self.slider_add.setValue(self.slider_add.value() - 0.001)
        self._on_change_add(self.slider_add.value())

    def add_fast_minus(self):
        """

            @brief:
                on add :
                minus 0.01 to slider when clicking fast minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_add.setValue(self.slider_add.value() - 0.01)
        self._on_change_add(self.slider_add.value())

    def _on_change_mu(self, event):
        """
             Change mean value and update cursor position

             :param event: event that update the value

             :return: None
         """
        self.label_mu_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_simple_gaussian_emission(np.asarray(self.data),
                                            [self.slider_sigma.value() + 0.0001, event, self.slider_add.value()])
        else:
            y = mF.model_simple_gaussian(np.asarray(self.data),
                                [self.slider_sigma.value() + 0.0001, event, self.slider_add.value()])
        self.update_curves(y)

    def _on_change_add(self, event):
        """
            Change add value and update cursor position

            :param event: event that update the value

            :return: None
        """
        self.label_add_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_simple_gaussian_emission(np.asarray(self.data),
                                            [self.slider_sigma.value() + 0.0001, self.slider_mu.value(), event])
        else:
            y = mF.model_simple_gaussian(np.asarray(self.data),
                                [self.slider_sigma.value() + 0.0001, self.slider_mu.value(), event])
        self.update_curves(y)

    def _on_change_sigma(self, event):
        """
            Change sigma value and update cursor position

            :param event: event that update the value

            :return: None
        """
        self.label_sigma_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_simple_gaussian_emission(np.asarray(self.data),
                                            [event + 0.0001, self.slider_mu.value(), self.slider_add.value()])
        else:
            y = mF.model_simple_gaussian(np.asarray(self.data),
                                [event + 0.0001, self.slider_mu.value(), self.slider_add.value()])
        self.update_curves(y)

    def update_curves(self, y):
        """
            show the updated curve after one parameter have changed.

            :param y: new curve to show

            :return: None
        """
        self.curve["curve"].setData(self.data, y, pen=self.pen)
        self.master.curves[self.curve["name"]]["y"] = y
        self.master.update_all()


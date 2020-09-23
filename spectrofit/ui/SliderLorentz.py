from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PySide2.QtGui import QPen
from PySide2.QtCore import Qt

import spectrofit.math.mathFunction as mF
from spectrofit.ui.DoubleSlider import Slider
import numpy as np


class SliderLorentz(QWidget):
    def __init__(self, master, curve, data):
        super().__init__()
        self.master = master
        self.curve = curve
        self.data = data
        self.lim = self.curve["lim"]
        self.pen = QPen(Qt.green, 0.01, Qt.DashDotLine)

        self.slider_mean = Slider()
        self.slider_gamma = Slider()
        self.slider_add = Slider()

        self.set_ui_lo()

        self.show()

    def set_ui_lo(self):
        # Set up all Layout :

        lay = QGridLayout()

        self.slider_mean.setTickPosition(QSlider.TicksBelow)
        self.slider_gamma.setTickPosition(QSlider.TicksBelow)

        self.slider_mean.setTickInterval(0.01)
        self.slider_mean.setSingleStep(0.01)
        self.slider_mean.setTracking(True)

        self.slider_gamma.setTickInterval(0.001)
        self.slider_gamma.setSingleStep(0.001)
        self.slider_gamma.setTracking(True)

        self.slider_add.setTickInterval(0.001)
        self.slider_add.setSingleStep(0.001)
        self.slider_add.setTracking(True)

        self.slider_mean.setMinimum(self.lim[0])
        self.slider_mean.setMaximum(self.lim[1])

        self.slider_gamma.setMinimum(0)
        self.slider_gamma.setMaximum(3)

        self.slider_add.setMinimum(0)
        self.slider_add.setMaximum(10)

        self.slider_mean.setOrientation(Qt.Horizontal)
        self.slider_gamma.setOrientation(Qt.Horizontal)
        self.slider_add.setOrientation(Qt.Vertical)

        label_title = QLabel("Parametrize Lorentzian {}".format(self.curve["count"]))
        label1 = QLabel("Parameter mu : ")
        label2 = QLabel("Parameter gamma : ")
        label3 = QLabel("Parameter add : ")

        lay.addWidget(label_title, 0, 0, 1, 0, Qt.AlignCenter)
        lay.addWidget(label1, 1, 0)
        lay.addWidget(label2, 3, 0)
        lay.addWidget(label3, 5, 0)

        # Add slider mean and surronding widget to layout
        lay.addWidget(self.slider_mean, 1, 3)
        slider_mean_hbox = QHBoxLayout()
        label_mean_minimum = QLabel("min : {}".format(self.lim[0]))
        label_mean_actual = QLabel("Actual : ")
        self.label_mean_actual_val = QLabel("0")
        label_mean_maximum = QLabel("max : {}".format(self.lim[1]))
        self.slider_mean.doubleValueChanged.connect(self._on_change_mean)
        slider_mean_hbox.addWidget(label_mean_minimum, Qt.AlignLeft)
        slider_mean_hbox.addWidget(label_mean_actual, Qt.AlignCenter)
        slider_mean_hbox.addWidget(self.label_mean_actual_val, Qt.AlignCenter)
        slider_mean_hbox.addWidget(label_mean_maximum, Qt.AlignRight)
        lay.addLayout(slider_mean_hbox, 2, 3)

        # Add slider gamma and surronding widget to layout
        lay.addWidget(self.slider_gamma, 3, 3)
        slider_gamma_hbox = QHBoxLayout()
        label_gamma_minimum = QLabel("min : 0")
        label_gamma_actual = QLabel("actual : ")
        self.label_gamma_actual_val = QLabel("0")
        label_gamma_maximum = QLabel("max : 3")
        self.slider_gamma.doubleValueChanged.connect(self._on_change_gamma)
        slider_gamma_hbox.addWidget(label_gamma_minimum, Qt.AlignLeft)
        slider_gamma_hbox.addWidget(label_gamma_actual, Qt.AlignCenter)
        slider_gamma_hbox.addWidget(self.label_gamma_actual_val, Qt.AlignCenter)
        slider_gamma_hbox.addWidget(label_gamma_maximum, Qt.AlignRight)
        v1 = QVBoxLayout()
        v1.addLayout(slider_gamma_hbox)
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

        button1_mean = QPushButton("<<")
        button1_mean.clicked.connect(self.mean_fast_minus)
        button2_mean = QPushButton("<")
        button2_mean.clicked.connect(self.mean_slow_minus)
        button3_mean = QPushButton(">>")
        button3_mean.clicked.connect(self.mean_fast_add)
        button4_mean = QPushButton(">")
        button4_mean.clicked.connect(self.mean_slow_add)
        lay.addWidget(button1_mean, 1, 1)
        lay.addWidget(button2_mean, 1, 2)
        lay.addWidget(button4_mean, 1, 4)
        lay.addWidget(button3_mean, 1, 5)

        button1_gamma = QPushButton("<<")
        button1_gamma.clicked.connect(self.gamma_fast_minus)
        button2_gamma = QPushButton("<")
        button2_gamma.clicked.connect(self.gamma_slow_minus)
        button3_gamma = QPushButton(">>")
        button3_gamma.clicked.connect(self.gamma_fast_add)
        button4_gamma = QPushButton(">")
        button4_gamma.clicked.connect(self.gamma_slow_add)
        lay.addWidget(button1_gamma, 3, 1)
        lay.addWidget(button2_gamma, 3, 2)
        lay.addWidget(button4_gamma, 3, 4)
        lay.addWidget(button3_gamma, 3, 5)

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

    def mean_slow_add(self):
        """

        @brief:
            on mean :
            add 0.001 to slider when clicking slow add button

        :parameter:
            self

        :return:
            None
        """
        self.slider_mean.setValue(self.slider_mean.value() + 0.001)
        self._on_change_mean(self.slider_mean.value())

    def mean_fast_add(self):
        """

            @brief:
                on mean :
                add 0.01 to slider when clicking fast add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mean.setValue(self.slider_mean.value() + 0.01)
        self._on_change_mean(self.slider_mean.value())

    def mean_slow_minus(self):
        """

            @brief:
                on mean :
                minus 0.001 to slider when clicking slow minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mean.setValue(self.slider_mean.value() - 0.001)
        self._on_change_mean(self.slider_mean.value())

    def mean_fast_minus(self):
        """

            @brief:
                on mean :
                minus 0.01 to slider when clicking fast minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_mean.setValue(self.slider_mean.value() - 0.01)
        self._on_change_mean(self.slider_mean.value())

    def gamma_slow_add(self):
        """

        @brief:
            on gamma :
            add 0.001 to slider when clicking slow add button

        :parameter:
            self

        :return:
            None
        """
        self.slider_gamma.setValue(self.slider_gamma.value() + 0.001)
        self._on_change_gamma(self.slider_gamma.value())

    def gamma_fast_add(self):
        """

            @brief:
                on gamma :
                add 0.01 to slider when clicking fast add button

            :parameter:
                self

            :return:
                None
        """
        self.slider_gamma.setValue(self.slider_gamma.value() + 0.01)
        self._on_change_gamma(self.slider_gamma.value())

    def gamma_slow_minus(self):
        """

            @brief:
                on gamma :
                minus 0.001 to slider when clicking slow minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_gamma.setValue(self.slider_gamma.value() - 0.001)
        self._on_change_gamma(self.slider_gamma.value())

    def gamma_fast_minus(self):
        """

            @brief:
                on gamma :
                minus 0.01 to slider when clicking fast minus button

            :parameter:
                self

            :return:
                None
        """
        self.slider_gamma.setValue(self.slider_gamma.value() - 0.01)
        self._on_change_gamma(self.slider_gamma.value())

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

    def _on_change_mean(self, event):
        """
        Change mean value and update cursor position

        :param event: event that update the value

        :return: None
        """
        self.label_mean_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_lorentz_emission(np.asarray(self.data),
                                            [event, self.slider_gamma.value() + 0.0001, self.slider_add.value()])
        else:
            y = mF.model_lorentz(np.asarray(self.data),
                                [event, self.slider_gamma.value() + 0.0001, self.slider_add.value()])
        self.update_curves(y)

    def _on_change_add(self, event):
        """
            Change add value and update cursor position

            :param event: event that update the value

            :return: None
        """
        self.label_add_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_lorentz_emission(np.asarray(self.data),
                                            [self.slider_mean.value(), self.slider_gamma.value() + 0.0001, event])
        else:
            y = mF.model_lorentz(np.asarray(self.data),
                                [self.slider_mean.value(), self.slider_gamma.value() + 0.0001, event])
        self.update_curves(y)

    def _on_change_gamma(self, event):
        """
            Change gamma value and update cursor position

            :param event: event that update the value

            :return: None
        """
        self.label_gamma_actual_val.setNum(event)
        if self.emis.isChecked():
            y = mF.model_lorentz_emission(np.asarray(self.data),
                                            [self.slider_mean.value(), event + 0.0001, self.slider_add.value()])
        else:
            y = mF.model_lorentz(np.asarray(self.data),
                                [self.slider_mean.value(), event + 0.0001, self.slider_add.value()])
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

from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PySide2.QtGui import QPen
from PySide2.QtCore import Qt

import spectrofit.math.mathFunction as mF
from spectrofit.ui.DoubleSlider import Slider
import numpy as np

class SliderExponential(QWidget):
    def __init__(self, curve):
        super().__init__()
        self.curve = curve
        print("TBD")

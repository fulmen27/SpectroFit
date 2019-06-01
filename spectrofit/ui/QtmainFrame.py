import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Circle

from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QMenuBar, QMainWindow, QAction, QVBoxLayout, \
    QPushButton, QCheckBox, QLabel, QLineEdit, QMessageBox
from PySide2.QtCore import QRect, QPointF
from PySide2.QtGui import QPainter

from spectrofit.ui.PainterCanvas import PainterCanvas

from spectrofit.core.QTImportFile import ImportFile
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre

from spectrofit.math.Fits import Fits
import spectrofit.math.mathFunction as mF

from spectrofit.tools.elements_table import ElementTable


class MainFrame(QMainWindow, QWidget):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # layout
        self.layout = None
        self.bar = None

        # Var
        self.compute_button = None
        self.clean_button = None
        self.fit_button = None
        self.canvas = None
        self.toolbar = None
        self.full = None
        self.num_ordre = None

        # Imports
        self.my_import = None
        self.fig = None
        self.ax = None
        self.lim = []
        self.data = {"x": [], "y": []}
        self.fits = Fits(self.data)
        self.element_table = None

        # Set Users interfaces functions
        self._set_ui()

        self.master.show()

    def _set_ui(self):
        self.layout = QGridLayout()
        menu_layout = QHBoxLayout()
        menu_layout.setGeometry(QRect(0, 0, 800, 50))
        self.bar = QMenuBar(self.master)

        file_menu = self.bar.addMenu("file")
        open_S = QAction("Ouvrir fichier S", self.master)
        open_S.triggered.connect(self._open_s)
        file_menu.addAction(open_S)
        open_CSV = QAction("Ouvrir fichier CSV", self.master)
        open_CSV.triggered.connect(self._open_csv)
        file_menu.addAction(open_CSV)

        tools_menu = self.bar.addMenu("Tools")
        find_ray = QAction("Trouver une raie", self.master)
        find_ray.triggered.connect(self._find_ray)
        tools_menu.addAction(find_ray)
        fit = QAction("Fits", self.master)
        fit.triggered.connect(self._fit_algo)
        tools_menu.addAction(fit)
        menu_layout.addWidget(self.bar)
        self.layout.addLayout(menu_layout, 0, 0, 1, -1)

        btn_layout = QVBoxLayout()
        # Compute
        self.compute_button = QPushButton("Compute")
        self.compute_button.setEnabled(False)
        self.compute_button.clicked.connect(self._on_compute)
        btn_layout.addWidget(self.compute_button)
        self.compute_button.show()

        # Full Spectre
        self.full = QCheckBox("Spectre entier")
        self.full.setChecked(False)
        btn_layout.addWidget(self.full)

        # Get Order
        label = QLabel("Choisit ton ordre")
        btn_layout.addWidget(label)
        self.num_ordre = QLineEdit()
        btn_layout.addWidget(self.num_ordre)

        self.layout.addLayout(btn_layout, 1, 1)
        self.master.setLayout(self.layout)

    def _open_csv(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportFile("csv", self.master)
        self.compute_button.setEnabled(True)

    def _open_s(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportFile("s", self.master)
        self.compute_button.setEnabled(True)

    def _on_compute(self):
        try:
            order = int(self.num_ordre.text())
            self.lim = compute_delim(self.my_import, order, self.full.isChecked())
            self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1])
            self._set_canvas()
        except:
            print("erreur")
            warning = QMessageBox()
            warning.setText("Please enter an integer")
    """
    def _set_canvas(self):
        layout_canvas = QVBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.mpl_connect('button_press_event', self._on_left_click)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout_canvas.addWidget(self.canvas)
        layout_canvas.addWidget(self.toolbar)
        self.layout.addLayout(layout_canvas, 1, 0, -1, 1)
        self.master.setLayout(self.layout)"""

    def _set_canvas(self):
        layout_canvas = QVBoxLayout()
        self.canvas = PainterCanvas(self.fig, self.ax, self.master)
        self.canvas.mpl_connect("button_press_event", self._on_left_click)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout_canvas.addWidget(self.canvas)
        layout_canvas.addWidget(self.toolbar)
        self.layout.addLayout(layout_canvas, 1, 0, -1, 1)
        self.master.setLayout(self.layout)

    def _on_left_click(self, event):
        """SET POINTS"""
        print(event.xdata)
        self.data["x"].append(event.xdata)
        self.data["y"].append(event.ydata)
        self.fits.x = np.append(self.fits.x, event.xdata)
        self.fits.y = np.append(self.fits.y, event.ydata)
        self.canvas.create_oval(event.xdata, event.ydata, brush_color="green")

    def _find_ray(self):
        window = QWidget()
        self.element_table = ElementTable(window)

    def _fit_algo(self):
        self.window_fit = QWidget()
        layout_fit = QVBoxLayout()
        text = QLabel("Choisi ton fit")

        simple_gaussian = QPushButton("simple gaussian")
        simple_gaussian.clicked.connect(self._simple_gaussian)
        double_gaussian = QPushButton("double gaussian")
        double_gaussian.clicked.connect(self._double_gaussian)
        simple_expo = QPushButton("simple expo")
        simple_expo.clicked.connect(self._simple_expo)
        double_expo = QPushButton("double expo")
        double_expo.clicked.connect(self._double_expo)
        lorentz = QPushButton("lorentz")
        lorentz.clicked.connect(self._lorentz)
        double_lorentz = QPushButton("double lorentz")
        double_lorentz.clicked.connect(self._double_lorentz)
        linear = QPushButton("linear")
        linear.clicked.connect(self._linear)

        layout_fit.addWidget(text)
        layout_fit.addWidget(simple_gaussian)
        layout_fit.addWidget(double_gaussian)
        layout_fit.addWidget(simple_expo)
        layout_fit.addWidget(double_expo)
        layout_fit.addWidget(lorentz)
        layout_fit.addWidget(double_lorentz)
        layout_fit.addWidget(linear)

        simple_gaussian.show()
        double_gaussian.show()
        simple_expo.show()
        double_expo.show()
        lorentz.show()
        double_lorentz.show()
        linear.show()

        self.window_fit.setLayout(layout_fit)
        self.window_fit.activateWindow()
        self.window_fit.show()

    def _simple_gaussian(self):
        sol = self.fits.simple_gaussian()
        y = mF.model_simple_gaussian(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_gaussian(self):
        sol = self.fits.double_gaussian()
        y = mF.model_double_gaussian(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _simple_expo(self):
        sol = self.fits.simple_exp()
        y = mF.model_simple_expo(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_expo(self):
        sol = self.fits.double_exp()
        y = mF.model_double_expo(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _linear(self):
        sol = self.fits.linear()
        y = mF.model_linear(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _lorentz(self):
        sol = self.fits.lorentz()
        y = mF.model_lorentz(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_lorentz(self):
        sol = self.fits.double_lorentz()
        y = mF.model_double_lorentz(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _clean_list(self):
        self.data["x"] = []
        self.data["y"] = []
        self.fits.x = []
        self.fits.y = []
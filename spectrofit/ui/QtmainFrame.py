import numpy as np

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QMenuBar, QMainWindow, QAction, QVBoxLayout, \
    QPushButton, QCheckBox, QLabel, QLineEdit, QMessageBox
from PySide2.QtCore import QRect, Qt

from spectrofit.ui.PainterCanvas import PainterCanvas

from spectrofit.core.QTImportFile import ImportFile
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre

from spectrofit.math.Fits import Fits
import spectrofit.math.Fits as F
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
        self.abs = None

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
        self.find_ray = QAction("Trouver une raie", self.master)
        self.find_ray.setEnabled(False)
        self.find_ray.triggered.connect(self._find_ray)
        tools_menu.addAction(self.find_ray)
        self.fit_button = QAction("Fits", self.master)
        self.fit_button.setEnabled(False)
        self.fit_button.triggered.connect(self._fit_algo)
        tools_menu.addAction(self.fit_button)
        self.distance_btn = QAction("distance", self.master)
        self.distance_btn.setEnabled(False)
        self.distance_btn.triggered.connect(self._distance)
        tools_menu.addAction(self.distance_btn)
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
        label.setFixedHeight(10)
        btn_layout.addWidget(label)
        self.num_ordre = QLineEdit()
        btn_layout.addWidget(self.num_ordre)
        btn_layout.setAlignment(Qt.AlignTop)

        self.clean_button = QPushButton("Clean")
        self.clean_button.setEnabled(False)
        self.clean_button.clicked.connect(self._on_clean)
        btn_layout.addWidget(self.clean_button)
        self.clean_button.show()

        self.layout.addLayout(btn_layout, 1, 1, Qt.AlignTop)
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
        if self.full.isChecked():
            self.lim = compute_delim(self.my_import, btn_state=self.full.isChecked())
            self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1])
            self._set_canvas()
            self.find_ray.setEnabled(True)
            self.clean_button.setEnabled(True)
        else:
            try:
                order = int(self.num_ordre.text())
                self.lim = compute_delim(self.my_import, num_ordre=order)
                self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1])
                self._set_canvas()
                self.find_ray.setEnabled(True)
                self.clean_button.setEnabled(True)
            except ValueError:
                details = "Afin que l'algorithme puisse afficher votre spectre il lui faut un ordre pour " \
                          "compartimenter. Vous pouvez aussi clicker sur le bouton à cocher afin de sélectionner" \
                          " le spectre en entier"
                self._warnings("Rentrez un entier dans la sélection d'ordre", details)

    def _on_clean(self):
        self.canvas.clean_canvas()

    def _info(self, message, details=None):
        self.warning = QMessageBox()
        self.warning.setIcon(QMessageBox.Information)
        self.warning.setText(message)
        self.warning.setDetailedText(details)
        self.warning.setStandardButtons(QMessageBox.Ok)
        self.warning.activateWindow()
        self.warning.show()

    def _warnings(self, message, details=None):
        self.warning = QMessageBox()
        self.warning.setIcon(QMessageBox.Warning)
        self.warning.setText(message)
        self.warning.setDetailedText(details)
        self.warning.setStandardButtons(QMessageBox.Ok)
        self.warning.activateWindow()
        self.warning.show()

    def _error(self, message, details=None):
        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Critical)
        self.error.setText(message)
        self.error.setDetailedText(details)
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.activateWindow()
        self.error.show()

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
        self.master.showMaximized()

    def _on_left_click(self, event):
        """SET POINTS"""
        self.data["x"].append(event.xdata)
        self.data["y"].append(event.ydata)
        self.fits.x = np.append(self.fits.x, event.xdata)
        self.fits.y = np.append(self.fits.y, event.ydata)
        self.canvas.create_oval(event.xdata, event.ydata, brush_color="green")
        if len(self.data["x"]) >= 2:
            self.distance_btn.setEnabled(True)
            if len(self.data["x"]) > 5:
                self.fit_button.setEnabled(True)

    def _find_ray(self):
        window = QWidget()
        self.element_table = ElementTable(self, window)

    def _distance(self):
        x1 = self.data["x"][-2]
        x2 = self.data["x"][-1]
        y1 = self.data["y"][-2]
        y2 = self.data["y"][-1]
        message = "La distance horizontale entre les deux points est : {} \n" \
                  "La distance verticale entre les deux points est : {} \n" \
                  "La distance euclidienne est : {}".format(abs(x1 - x2), abs(y1 - y2),
                                                            np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        self._info(message)
        self.canvas.clean_canvas([[x1, y1], [x2, y2]])
        self.data["x"].pop(-1)
        self.data["x"].pop(-1)
        self.data["y"].pop(-1)
        self.data["y"].pop(-1)
        if len(self.data["x"]) < 2:
            self.distance_btn.setEnabled(False)

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
        self.abs = QCheckBox("Spectre en absorption")
        self.abs.setChecked(False)
        layout_fit.addWidget(self.abs)

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
        if self.abs.isChecked():
            sol = self.fits.simple_gaussian(F.model_simple_gaussian)
            y = mF.model_simple_gaussian(self.data["x"], sol)
        else:
            sol = self.fits.simple_gaussian(F.model_simple_gaussian_emission)
            y = mF.model_simple_gaussian_emission(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _double_gaussian(self):
        if self.abs.isChecked():
            sol = self.fits.double_gaussian(F.model_double_gaussian)
            y = mF.model_double_gaussian(self.data["x"], sol)
        else:
            sol = self.fits.double_gaussian(F.model_double_gaussian_emission)
            y = mF.model_double_gaussian_emission(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _simple_expo(self):
        sol = self.fits.simple_exp()
        y = mF.model_simple_expo(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _double_expo(self):
        sol = self.fits.double_exp()
        y = mF.model_double_expo(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _linear(self):
        sol = self.fits.linear()
        y = mF.model_linear(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _lorentz(self):
        if self.abs.isChecked():
            sol = self.fits.lorentz(F.model_lorentz)
            y = mF.model_lorentz(self.data["x"], sol)
        else:
            sol = self.fits.lorentz(F.model_lorentz_emission)
            y = mF.model_lorentz_emission(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _double_lorentz(self):
        if self.abs.isChecked():
            sol = self.fits.double_lorentz(F.model_double_lorentz)
            y = mF.model_double_lorentz(self.data["x"], sol)
        else:
            sol = self.fits.double_lorentz(F.model_double_lorentz_emission)
            y = mF.model_double_lorentz_emission(self.data["x"], sol)
        self.ax.plot(self.data["x"], y, color="green")
        self.fig.canvas.draw()
        self._clean_list()

    def _clean_list(self):
        self.data["x"] = []
        self.data["y"] = []
        self.fits.x = []
        self.fits.y = []

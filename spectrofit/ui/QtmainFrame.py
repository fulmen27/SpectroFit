import numpy as np

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt

from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QMenuBar, QMainWindow, QAction, QVBoxLayout, \
    QPushButton, QCheckBox, QLabel, QLineEdit, QMessageBox, QTabWidget
from PySide2.QtCore import QRect, Qt

from spectrofit.ui.PainterCanvas import PainterCanvas

from spectrofit.core.QTImportFile import ImportFile
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre, plot_from_xy_list

from spectrofit.math.Fits import Fits
from spectrofit.math.UserFit import UserFit, MixFit
import spectrofit.math.Fits as F
import spectrofit.math.mathFunction as mF

from spectrofit.tools.elements_table import ElementTable
from spectrofit.tools.Signal_processing_toolbox import SigProcToolbox


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
        self.full = None
        self.num_ordre = None
        self.abs = None
        self.tabs = None

        # Initialize QTabWidget (with first tab) and dict of tab
        self.tabs = QTabWidget()
        self.tabs.layout = QVBoxLayout()

        # Dict for all tabs
        self.dict_tabs = dict()
        self.links_list = []

        self.element_table = None
        self.signal_proc = None

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
        self.signal_proc_btn = QAction("Signal Processing ToolBox", self.master)
        self.signal_proc_btn.setEnabled(False)
        self.signal_proc_btn.triggered.connect(self._signal_processing_toolbox)
        tools_menu.addAction(self.signal_proc_btn)
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
        self.full = QCheckBox("Full Spectrum")
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
        my_import = ImportFile("csv", self.master)
        self.links_list.append([self.tabs.count(), None, my_import])
        self.compute_button.setEnabled(True)

    def _open_s(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        my_import = ImportFile("s", self.master)
        self.links_list.append([self.tabs.count(), None, my_import])
        self.compute_button.setEnabled(True)

    def _on_compute(self):
        if len(self.links_list) == self.tabs.count():
            my_import = self.links_list[self.tabs.currentIndex()][-1]
            reprint = True
        else:
            my_import = self.links_list[-1][-1]
            reprint = False

        if self.full.isChecked():
            lim = compute_delim(my_import, btn_state=self.full.isChecked())
            fig, ax = plot_ordre(my_import, lim[0], lim[1])
            self._set_canvas(my_import, lim, fig, ax, reprint)
            self.find_ray.setEnabled(True)
            self.clean_button.setEnabled(True)
            self.signal_proc_btn.setEnabled(True)
        else:
            try:
                order = int(self.num_ordre.text())
                lim = compute_delim(my_import, num_ordre=order)
                fig, ax = plot_ordre(my_import, lim[0], lim[1])
                self._set_canvas(my_import, lim, fig, ax, reprint)
                self.find_ray.setEnabled(True)
                self.clean_button.setEnabled(True)
                self.signal_proc_btn.setEnabled(True)
            except ValueError:
                details = "Afin que l'algorithme puisse afficher votre spectre il lui faut un ordre pour " \
                          "compartimenter. Vous pouvez aussi clicker sur le bouton à cocher afin de sélectionner" \
                          " le spectre en entier"
                self._warnings("Rentrez un entier dans la sélection d'ordre", details)

    def _on_clean(self):
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"].clean_canvas()

    def info(self, message, details=None):
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

    def error(self, message, details=None):
        self.error_var = QMessageBox()
        self.error_var.setIcon(QMessageBox.Critical)
        self.error_var.setText(message)
        self.error_var.setDetailedText(details)
        self.error_var.setStandardButtons(QMessageBox.Ok)
        self.error_var.activateWindow()
        self.error_var.show()

    def _set_canvas(self, my_import, lim, fig, ax, reprint=False):
        if not reprint:
            self.dict_tabs["Tab_{}".format(self.tabs.count())] = {}
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["Tab"] = QWidget()
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["Index"] = self.tabs.count()
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["import"] = my_import
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["lim"] = lim
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["fig"] = fig
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["ax"] = ax
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"] = dict()
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"]["x"] = list()
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"]["y"] = list()
            self.dict_tabs["Tab_{}".format(self.tabs.count())]["Fit"] = Fits(self,
                                                                             self.dict_tabs[
                                                                                 "Tab_{}".format(self.tabs.count())][
                                                                                 "data"])

            # Add tab
            self.tabs.addTab(self.dict_tabs["Tab_{}".format(self.tabs.count())]["Tab"],
                             my_import.my_csv["filename"].rstrip().split("/")[-1])

            # Set current index of tabs to use func currentIndex()
            self.tabs.setCurrentIndex(self.dict_tabs["Tab_{}".format(self.tabs.count() - 1)]["Index"])

            # Set tab Name into dict
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab_Name"] = \
                my_import.my_csv["filename"].rstrip().split("/")[-1]

            self.links_list[-1][0] = self.tabs.currentIndex()
            self.links_list[-1][1] = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab_Name"]

            # Set layout
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout = QVBoxLayout(self.tabs)

            # Set canvas
            canvas = PainterCanvas(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"],
                                   self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"],
                                   self.master)
            canvas.mpl_connect("button_press_event", self._on_canvas_click)
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"] = canvas

            # Set toolbar
            toolbar = NavigationToolbar(canvas, self)
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"] = toolbar

            # Set layout
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"])
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"])
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].setLayout(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout)

            self.tabs.layout.addWidget(self.tabs)
            self.layout.addLayout(self.tabs.layout, 1, 0, -1, 1)
            self.master.setLayout(self.layout)
            self.master.showMaximized()

        elif reprint:
            pos = self.tabs.currentIndex()
            plt.close(self.dict_tabs["Tab_{}".format(pos)]["fig"])
            del(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"])
            self.dict_tabs["Tab_{}".format(pos)] = {}
            self.dict_tabs["Tab_{}".format(pos)]["Tab"] = QWidget()
            self.dict_tabs["Tab_{}".format(pos)]["Index"] = pos
            self.dict_tabs["Tab_{}".format(pos)]["import"] = my_import
            self.dict_tabs["Tab_{}".format(pos)]["lim"] = lim
            self.dict_tabs["Tab_{}".format(pos)]["fig"] = fig
            self.dict_tabs["Tab_{}".format(pos)]["ax"] = ax
            self.dict_tabs["Tab_{}".format(pos)]["data"] = dict()
            self.dict_tabs["Tab_{}".format(pos)]["data"]["x"] = list()
            self.dict_tabs["Tab_{}".format(pos)]["data"]["y"] = list()
            self.dict_tabs["Tab_{}".format(pos)]["Fit"] = Fits(self, self.dict_tabs["Tab_{}".format(pos)]["data"])

            # Add tab
            self.tabs.insertTab(pos, self.dict_tabs["Tab_{}".format(pos)]["Tab"],
                                my_import.my_csv["filename"].rstrip().split("/")[-1])
            self.tabs.removeTab(pos + 1)
            # Set current index of tabs to use func currentIndex()
            self.tabs.setCurrentIndex(self.dict_tabs["Tab_{}".format(pos)]["Index"])

            # Set layout
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout = QVBoxLayout(self.tabs)

            # Set canvas
            canvas = PainterCanvas(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"],
                                   self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"],
                                   self.master)
            canvas.mpl_connect("button_press_event", self._on_canvas_click)
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"] = canvas

            # Set toolbar
            toolbar = NavigationToolbar(canvas, self)
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"] = toolbar

            # Set layout
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"])
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"])
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].setLayout(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout)

            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()

    def add_tab_from_wavelet(self, args):
        fig, ax = plot_from_xy_list(args)
        self.dict_tabs["Tab_{}".format(self.tabs.count())] = {}
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["Tab"] = QWidget()
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["Index"] = self.tabs.count()
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["import"] = args["import"]
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["lim"] = args["lim"]
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["fig"] = fig
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["ax"] = ax
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"] = dict()
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"]["x"] = list()
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["data"]["y"] = list()
        self.dict_tabs["Tab_{}".format(self.tabs.count())]["Fit"] = Fits(self,
                                                                         self.dict_tabs[
                                                                             "Tab_{}".format(self.tabs.count())][
                                                                             "data"])

        # Add tab
        self.tabs.addTab(self.dict_tabs["Tab_{}".format(self.tabs.count())]["Tab"],
                         args["import"].my_csv["filename"].rstrip().split("/")[-1] + "_wavelet_denoising")

        # Set current index of tabs to use func currentIndex()
        self.tabs.setCurrentIndex(self.dict_tabs["Tab_{}".format(self.tabs.count() - 1)]["Index"])

        # Set tab Name into dict
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab_Name"] = \
            args["import"].my_csv["filename"].rstrip().split("/")[-1]

        self.links_list[-1][0] = self.tabs.currentIndex()
        self.links_list[-1][1] = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab_Name"]

        # Set layout
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout = QVBoxLayout(self.tabs)

        # Set canvas
        canvas = PainterCanvas(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"],
                               self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"],
                               self.master)
        canvas.mpl_connect("button_press_event", self._on_canvas_click)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"] = canvas

        # Set toolbar
        toolbar = NavigationToolbar(canvas, self)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"] = toolbar

        # Set layout
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"])
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout.addWidget(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["toolbar"])
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].setLayout(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Tab"].layout)

    def _on_canvas_click(self, event):
        if event.button == MouseButton.LEFT:
            self._on_left_click(event)
        elif event.button == MouseButton.RIGHT:
            print("TBD")

    def _on_left_click(self, event):
        """SET POINTS"""
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"].append(event.xdata)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"].append(event.ydata)

        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].x = np.append(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].x,
            event.xdata)

        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].y = np.append(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].y,
            event.ydata)

        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"].create_oval(event.xdata, event.ydata,
                                                                                        brush_color="green")

        if len(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"]) >= 2:
            self.distance_btn.setEnabled(True)
            if len(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"]) > 5:
                self.fit_button.setEnabled(True)

    def _find_ray(self):
        window = QWidget()
        self.element_table = ElementTable(self, window)

    def _distance(self):
        x1 = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"][-2]
        x2 = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"][-1]
        y1 = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"][-2]
        y2 = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"][-1]
        message = "La distance horizontale entre les deux points est : {} \n" \
                  "La distance verticale entre les deux points est : {} \n" \
                  "La distance euclidienne est : {}".format(abs(x1 - x2), abs(y1 - y2),
                                                            np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        self.info(message)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["canvas"].clean_canvas([[x1, y1], [x2, y2]])
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"].pop(-1)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"].pop(-1)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"].pop(-1)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"].pop(-1)
        if len(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"]) < 2:
            self.distance_btn.setEnabled(False)

    def _signal_processing_toolbox(self):
        self.signal_proc = SigProcToolbox(self)

    def _fit_algo(self):
        self.window_fit = QWidget()
        layout_fit = QVBoxLayout()
        text = QLabel("Choose a function to fit to the data")
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
        mix = QPushButton("mix")
        mix.clicked.connect(self._mix)
        new = QPushButton("new model")
        new.clicked.connect(self._new)
        self.abs = QCheckBox("Absorption Spectrum ?")
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
        layout_fit.addWidget(mix)
        layout_fit.addWidget(new)

        simple_gaussian.show()
        double_gaussian.show()
        simple_expo.show()
        double_expo.show()
        lorentz.show()
        double_lorentz.show()
        linear.show()
        mix.show()
        new.show()

        self.window_fit.setLayout(layout_fit)
        self.window_fit.activateWindow()
        self.window_fit.show()

    def _simple_gaussian(self):
        if self.abs.isChecked():
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].simple_gaussian(
                F.model_simple_gaussian)
            y = mF.model_simple_gaussian(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        else:
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].simple_gaussian(
                F.model_simple_gaussian_emission)
            y = mF.model_simple_gaussian_emission(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _double_gaussian(self):
        if self.abs.isChecked():
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].double_gaussian(
                F.model_double_gaussian)
            y = mF.model_double_gaussian(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        else:
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].double_gaussian(
                F.model_double_gaussian_emission)
            y = mF.model_double_gaussian_emission(
                self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _simple_expo(self):
        sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].simple_exp(F.model_simple_expo)
        y = mF.model_simple_expo(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _double_expo(self):
        sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].double_exp(F.model_double_expo)
        y = mF.model_double_expo(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _linear(self):
        sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].linear(F.model_linear)
        y = mF.model_linear(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _lorentz(self):
        if self.abs.isChecked():
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].lorentz(F.model_lorentz)
            y = mF.model_lorentz(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        else:
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].lorentz(F.model_lorentz_emission)
            y = mF.model_lorentz_emission(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)

        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _double_lorentz(self):
        if self.abs.isChecked():
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].double_lorentz(
                F.model_double_lorentz)
            y = mF.model_double_lorentz(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], sol)
        else:
            sol = self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].double_lorentz(
                F.model_double_lorentz_emission)
            y = mF.model_double_lorentz_emission(self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"],
                                                 sol)
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["ax"].plot(
            self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"], y, color="green")
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["fig"].canvas.draw()
        self._clean_list()

    def _mix(self):
        self.mix_fit = MixFit(self, self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"])

    def _new(self):
        self.ufit = UserFit(self, self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"])

    def _clean_list(self):
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["x"] = []
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["data"]["y"] = []
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].x = []
        self.dict_tabs["Tab_{}".format(self.tabs.currentIndex())]["Fit"].y = []

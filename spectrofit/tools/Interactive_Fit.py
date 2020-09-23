import pyqtgraph as pg
from PySide2.QtWidgets import QWidget, QGridLayout, QMenuBar, QAction
from PySide2.QtGui import QPen
from PySide2.QtCore import Slot, Qt
import json

import spectrofit.math.mathFunction as mF

from spectrofit.ui.SliderGaussian import SliderGaussian
from spectrofit.ui.SliderLorentz import SliderLorentz

import numpy as np


class InteractiveFit(QWidget):

    """Interactive Fit with slider to adjust curve to the spectrum"""

    def __init__(self, data):
        super().__init__()
        self.data = data

        # Init all dictionnary
        self.curves = dict()
        self.curves["nb_lo"] = 0
        self.curves["nb_gaus"] = 0
        self.curves["nb_l"] = 0
        self.curves["nb_exp"] = 0
        self.curves["y_tot"] = np.asarray([0 for _ in range(len(data["x"]))])

        self.pen_tot = QPen(Qt.red, 0.01)

        self.set_ui()
        self.show()

    def set_ui(self):

        # Set window's layout and UI

        lay = QGridLayout()
        self.graphWidget = pg.PlotWidget()
        curve = self.graphWidget.plot(self.data["x"], self.data["y"])
        self.curves["curve_tot"] = self.graphWidget.plot(self.data["x"], self.curves["y_tot"], pen=self.pen_tot)

        self.curves["widget"] = self.graphWidget

        lay.addWidget(self.graphWidget, 1, 0, 1, 1)
        self.setLayout(lay)

        self.bar = QMenuBar()
        tools = self.bar.addMenu("Tools")
        report = self.bar.addMenu("Report")

        add_lo = QAction("Add lorentz curve", self.bar)
        add_lo.triggered.connect(self._on_add_lo)

        add_gaus = QAction("Add gaussian curve", self.bar)
        add_gaus.triggered.connect(self._on_add_gaus)

        add_l = QAction("Add linear curve", self.bar)
        add_l.triggered.connect(self._on_add_l)

        add_exp = QAction("Add expo curve", self.bar)
        add_exp.triggered.connect(self._on_add_exp)

        tools.addAction(add_lo)
        tools.addAction(add_gaus)

        get_fit_report = QAction("Fit Report", self.bar)
        get_fit_report.triggered.connect(self._fit_report)
        report.addAction(get_fit_report)
        # HIDE FOR THE MOMENT BECAUSE USELESS
        # tools.addAction(add_l)
        # tools.addAction(add_exp)

        lay.addWidget(self.bar, 0, 0, 1, 1)

    @Slot()
    def _on_add_lo(self):
        """

        add a lorentz curve on the graph to fit the spectrum

        :return: None
        """

        # set metadata of new curve
        self.curves["nb_lo"] += 1
        self.curves["lo{}".format(self.curves["nb_lo"])] = dict()

        self.curves["lo{}".format(self.curves["nb_lo"])]["count"] = self.curves["nb_lo"]
        self.curves["lo{}".format(self.curves["nb_lo"])]["name"] = "lo{}".format(self.curves["nb_lo"])
        self.curves["lo{}".format(self.curves["nb_lo"])]["lim"] = [self.data["x"][0], self.data["x"][-1]]

        # set parameter
        mu = (self.data["x"][0] + self.data["x"][-1]) / 2
        gamma = 1
        y = mF.model_lorentz_emission(np.asarray(self.data["x"]), [mu, gamma, 0])

        # compute curve
        self.curves["lo{}".format(self.curves["nb_lo"])]["y"] = y
        self.curves["lo{}".format(self.curves["nb_lo"])]["curve"] = self.graphWidget.plot(self.data["x"], y)

        self.curves["lo{}".format(self.curves["nb_lo"])]["curseur"] = SliderLorentz(self,
                                                                                    self.curves["lo{}".format(
                                                                                        self.curves["nb_lo"])],
                                                                                    self.data["x"])

    @Slot()
    def _on_add_gaus(self):
        """

            add a gaussian curve on the graph to fit the spectrum

            :return: None
        """

        # set metadata of new curve
        self.curves["nb_gaus"] += 1
        self.curves["gaus{}".format(self.curves["nb_gaus"])] = dict()

        self.curves["gaus{}".format(self.curves["nb_gaus"])]["count"] = self.curves["nb_gaus"]
        self.curves["gaus{}".format(self.curves["nb_gaus"])]["name"] = "gaus{}".format(self.curves["nb_gaus"])
        self.curves["gaus{}".format(self.curves["nb_gaus"])]["lim"] = [self.data["x"][0], self.data["x"][-1]]


        # set parameter
        mu = (self.data["x"][0] + self.data["x"][-1]) / 2
        sigma = 1
        y = mF.model_simple_gaussian_emission(np.asarray(self.data["x"]), [sigma, mu, 0])

        # compute curve
        self.curves["gaus{}".format(self.curves["nb_gaus"])]["y"] = y
        self.curves["gaus{}".format(self.curves["nb_gaus"])]["curve"] = self.graphWidget.plot(self.data["x"], y)

        self.curves["gaus{}".format(self.curves["nb_gaus"])]["curseur"] = SliderGaussian(self, self.curves[
            "gaus{}".format(self.curves["nb_gaus"])], self.data["x"])

    @Slot()
    def _on_add_l(self):
        """deprecated"""
        print("Deprecated function")

    @Slot()
    def _on_add_exp(self):
        """deprecated"""
        print("Deprecated function")

    def update_all(self):
        """

        update sum of all curve when adding a new curve or modifying existing one

        :return:
        """
        self.curves["y_tot"] = np.asarray([0.0 for _ in range(len(self.data["x"]))])
        for key, value in self.curves.items():
            if type(value) == type(dict()):
                self.curves["y_tot"] += np.asarray(value["y"])
        self.curves["curve_tot"].setData(self.data["x"], self.curves["y_tot"], pen=self.pen_tot)

    def _fit_report(self):

        """

        build and save the report of the fit in json file

        :return:
        """
        report = dict()
        report["lim"] = [self.data["x"][0], self.data["x"][-1]]
        for key, value in self.curves.items():
            if type(value) == type(dict()):
                if "lo" in key:
                    report["Lorentzian_number : {}".format(value["count"])] = dict()
                    report["Lorentzian_number : {}".format(value["count"])]["parameter_mu"] = value[
                        "curseur"].slider_mean.value()
                    report["Lorentzian_number : {}".format(value["count"])]["parameter_gamma"] = value[
                        "curseur"].slider_gamma.value()
                    report["Lorentzian_number : {}".format(value["count"])]["parameter_add"] = value[
                        "curseur"].slider_add.value()
                if "gaus" in key:
                    report["Gaussian number : {}".format(value["count"])] = dict()
                    report["Gaussian number : {}".format(value["count"])]["parameter_mu_"] = value[
                        "curseur"].slider_mu.value()
                    report["Gaussian number : {}".format(value["count"])]["parameter_sigma"] = value[
                        "curseur"].slider_sigma.value()
                    report["Gaussian number : {}".format(value["count"])]["parameter_add"] = value[
                        "curseur"].slider_add.value()

        with open('fit_report.json', 'w') as fp:
            json.dump(report, fp)

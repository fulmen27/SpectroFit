from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QPushButton, QCheckBox
from PySide2.QtCore import Qt, SIGNAL, QObject

import spectrofit.math.Fits as F
import spectrofit.math.mathFunction as mF

import numpy as np
import random as rd
from lmfit import Model


class UserFit(QWidget):
    def __init__(self, master, data):
        self.master = master
        self.window = QWidget()
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])
        self.params = None

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
        super().__init__()
        self.master = master
        self.window = QWidget()
        self.x = np.asarray(data.x)
        self.y = np.asarray(data.y)

        self.solution = dict()
        self.checkbox_states = dict()
        self.checkbox_states_fit_method = dict()

        self.model = None
        self.emis = None

        self.set_ui()
        self.window.show()

    def set_ui(self):
        lay = QGridLayout(self.window)
        label = QLabel("Model to choose : ")
        lay.addWidget(label, 0, 0)
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

        self.emis = QCheckBox("Emission Spectrum")
        lay.addWidget(self.emis, i + 2, 0)

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
        lay.addWidget(process_fit, i + 2, 3)

    def _on_process_fit(self):
        s = 0
        method = ""
        for key, value in self.checkbox_states_fit_method.items():
            if value.isChecked():
                method = key
                s += 1

        print("you want to use method : {}".format(method))
        if s > 1:
            self.master.error("To many method are checked. Check only one box")
        else:
            models = dict()
            min = np.amin(self.x)
            max = np.amax(self.x)
            n_point_mandatory = 0
            for key, value in self.checkbox_states.items():
                moy1 = rd.uniform(min, max)
                moy2 = rd.uniform(min, max)
                s1 = rd.uniform(0, 1)
                s2 = rd.uniform(0, 1)
                if value.isChecked():
                    if key == "l":
                        models[key] = Model(F.model_linear)
                        models[key].set_param_hint("a_l", value=1)
                        models[key].set_param_hint("b_l", value=1)
                        n_point_mandatory += 2

                    elif key == "e":
                        models[key] = Model(F.model_simple_expo)
                        models[key].set_param_hint("a_e", value=1)
                        models[key].set_param_hint("b_e", value=1)
                        models[key].set_param_hint("add_e", value=1)
                        n_point_mandatory += 3

                    elif key == "de":
                        models[key] = Model(F.model_double_expo)
                        models[key].set_param_hint("a_de", value=1)
                        models[key].set_param_hint("b_de", value=1)
                        models[key].set_param_hint("c_de", value=1)
                        models[key].set_param_hint("d_de", value=1)
                        models[key].set_param_hint("add_de", value=1)
                        n_point_mandatory += 5

                    elif key == "lor":
                        if self.emis.isChecked():
                            models[key] = Model(F.model_lorentz_emission)
                        else:
                            models[key] = Model(F.model_lorentz)
                        models[key].set_param_hint("mu_l", value=moy1, min=min, max=max)
                        models[key].set_param_hint("gamma_l", value=s1, max=15, min=0)
                        models[key].set_param_hint("add_l", value=0)
                        n_point_mandatory += 3

                    elif key == "dlor":
                        if self.emis.isChecked():
                            models[key] = Model(F.model_double_lorentz_emission)
                        else:
                            models[key] = Model(F.model_double_lorentz)
                        models[key].set_param_hint("mu1_dl", value=moy1, min=min, max=max)
                        models[key].set_param_hint("gamma1_dl", value=s1, max=15, min=0)
                        models[key].set_param_hint("mu2_dl", value=moy2, min=min, max=max)
                        models[key].set_param_hint("gamma2_dl", value=s2, max=15, min=0)
                        models[key].set_param_hint("add_dl", value=0)
                        n_point_mandatory += 5

                    elif key == "gaus":
                        if self.emis.isChecked():
                            models[key] = Model(F.model_simple_gaussian_emission)
                        else:
                            models[key] = Model(F.model_simple_gaussian)
                        models[key].set_param_hint("sigma1_g", value=s1, max=15, min=0)
                        models[key].set_param_hint("mu1_g", value=moy1, min=min, max=max)
                        models[key].set_param_hint("add_g", value=0)
                        n_point_mandatory += 3

                    elif key == "dgaus":
                        if self.emis.isChecked():
                            models[key] = Model(F.model_double_gaussian_emission)
                        else:
                            models[key] = Model(F.model_double_gaussian)
                        models[key].set_param_hint("sigma1_dg", value=s1, max=15, min=0)
                        models[key].set_param_hint("mu1_dg", value=moy1, min=min, max=max)
                        models[key].set_param_hint("sigma2_dg", value=s2, max=15, min=0)
                        models[key].set_param_hint("mu2_dg", value=moy2, min=min, max=max)
                        models[key].set_param_hint("add_dg", value=0)
                        n_point_mandatory += 5

            if n_point_mandatory > len(self.x) or n_point_mandatory > len(self.y):
                self.master.error("Not enough point to fit all parameters")
            else:
                j = 0
                for key, value in models.items():
                    if j == 0:
                        self.model = value
                    else:
                        self.model += value
                    j += 1

                self.params = self.model.make_params()
                self.solution = self.model.fit(self.y, self.params, x=self.x, method=method)
                print(self.solution.fit_report())
                self.master.info(self.solution.fit_report())

                y = 0
                for key, value in self.checkbox_states.items():
                    if value.isChecked():
                        if key == "l":
                            coefficient = [self.solution.best_values['a_l'],
                                           self.solution.best_values['b_l']]
                            y += mF.model_linear(self.x, coefficient)
                        elif key == "e":
                            coefficient = [self.solution.best_values['a_e'],
                                           self.solution.best_values['b_e'],
                                           self.solution.best_values['add_e']]
                            y += mF.model_simple_expo(self.x, coefficient)
                        elif key == "de":
                            coefficient = [self.solution.best_values['a_de'],
                                           self.solution.best_values['b_de'],
                                           self.solution.best_values['c_de'],
                                           self.solution.best_values['d_de'],
                                           self.solution.best_values['add_de']]
                            y += mF.model_double_expo(self.x, coefficient)
                        elif key == "lor":
                            coefficient = [self.solution.best_values['mu_l'],
                                           self.solution.best_values['gamma_l'],
                                           self.solution.best_values['add_l']]
                            if self.emis.isChecked():
                                y += mF.model_lorentz_emission(self.x, coefficient)
                            else:
                                y += mF.model_lorentz(self.x, coefficient)
                        elif key == "dlor":
                            coefficient = [self.solution.best_values['mu1_dl'],
                                           self.solution.best_values['gamma1_dl'],
                                           self.solution.best_values['mu2_dl'],
                                           self.solution.best_values['gamma2_dl'],
                                           self.solution.best_values['add_dl']]
                            if self.emis.isChecked():
                                y += mF.model_double_lorentz_emission(self.x, coefficient)
                            else:
                                y += mF.model_double_lorentz(self.x, coefficient)
                        elif key == "gaus":
                            coefficient = [self.solution.best_values['sigma1_g'],
                                           self.solution.best_values['mu1_g'],
                                           self.solution.best_values['add_g']]
                            if self.emis.isChecked():
                                y += mF.model_simple_gaussian_emission(self.x, coefficient)
                            else:
                                y += mF.model_simple_gaussian(self.x, coefficient)
                        elif key == "dgaus":
                            coefficient = [self.solution.best_values['sigma1_dg'],
                                           self.solution.best_values['mu1_dg'],
                                           self.solution.best_values['sigma2_dg'],
                                           self.solution.best_values['mu2_dg'],
                                           self.solution.best_values['add_dg']]
                            if self.emis.isChecked():
                                y += mF.model_double_gaussian_emission(self.x, coefficient)
                            else:
                                y += mF.model_double_gaussian(self.x, coefficient)
                self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].plot(
                    self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["Fit"].x, y,
                    color="green")
                self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["fig"].canvas.draw()
                self.master.clean_list()
                
                self.master.save_file(self.solution.fit_report())

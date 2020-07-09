import numpy as np
from lmfit import Model


e = 10 ** (-8)

class Fits:
    def __init__(self, master, data):
        self.master = master
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])

        self.abs = 0

        self.solution = dict()

    # FITS
    def simple_gaussian(self, mod):
        min = np.asarray(self.x).min()
        max = np.asarray(self.x).max()
        moy = (min + max) / 2
        gmodel = Model(mod)
        gmodel.set_param_hint('sigma1_g', min=0, max=100)
        gmodel.set_param_hint('mu1_g', min=min, max=max)
        gmodel.set_param_hint('add_g', min=0)
        self.solution["simple_gaussian"] = gmodel.fit(self.y, x=self.x, sigma1_g=1, mu1_g=moy, add_g=1,
                                                      method='powell')
        self.master.info(self.solution["simple_gaussian"].fit_report())
        print(self.solution["simple_gaussian"].fit_report())
        self.solution["simple_gaussian_fit"] = [self.solution["simple_gaussian"].best_values['sigma1_g'],
                                                self.solution["simple_gaussian"].best_values['mu1_g'],
                                                self.solution["simple_gaussian"].best_values['add_g']]
        return self.solution["simple_gaussian_fit"], self.solution["simple_gaussian"].fit_report()

    def double_gaussian(self, mod):
        min = np.asarray(self.x).min()
        max = np.asarray(self.x).max()
        moy1 = (min + max) / 2 + 5
        moy2 = (min + max) / 2 - 5
        gmodel = Model(mod)
        gmodel.set_param_hint('sigma1_dg', min=0)
        gmodel.set_param_hint('sigma2_dg', min=0)
        gmodel.set_param_hint('mu1_dg', min=min, max=max)
        gmodel.set_param_hint('mu2_dg', min=min, max=max)
        self.solution["double_gaussian"] = gmodel.fit(self.y, x=self.x, sigma1_dg=1, sigma2_dg=1, mu1_dg=moy1,
                                                      mu2_dg=moy2, add_dg=1, method='powell')
        self.master.info(self.solution["double_gaussian"].fit_report())
        print(self.solution["double_gaussian"].fit_report())
        self.solution["double_gaussian_fit"] = [self.solution["double_gaussian"].best_values['sigma1_dg'],
                                                self.solution["double_gaussian"].best_values['mu1_dg'],
                                                self.solution["double_gaussian"].best_values['sigma2_dg'],
                                                self.solution["double_gaussian"].best_values['mu2_dg'],
                                                self.solution["double_gaussian"].best_values['add_dg']]
        return self.solution["double_gaussian_fit"], self.solution["double_gaussian"].fit_report()

    def simple_exp(self, mod):
        gmodel = Model(mod)
        self.solution["simple_exp"] = gmodel.fit(self.y, x=self.x, a_e=0, b_e=0, add_e=0, method='powell')
        print(self.solution["simple_exp"].fit_report())
        self.master.info(self.solution["simple_exp"].fit_report())
        self.solution["simple_exp_fit"] = [self.solution["simple_exp"].best_values['a_e'],
                                           self.solution["simple_exp"].best_values['b_e'],
                                           self.solution["simple_exp"].best_values['add_e'], ]
        return self.solution["simple_exp_fit"], self.solution["simple_exp"].fit_report()

    def double_exp(self, mod):
        gmodel = Model(mod)
        self.solution["double_exp"] = gmodel.fit(self.y, x=self.x, a_de=0, b_de=0, c_de=0, d_de=0, add_de=0,
                                                 method='powell')
        print(self.solution["double_exp"].fit_report())
        self.master.info(self.solution["double_exp"].fit_report())
        self.solution["double_exp_fit"] = [self.solution["double_exp"].best_values['a_de'],
                                           self.solution["double_exp"].best_values['b_de'],
                                           self.solution["double_exp"].best_values['c_de'],
                                           self.solution["double_exp"].best_values['d_de'],
                                           self.solution["double_exp"].best_values['add_de']]
        return self.solution["double_exp_fit"], self.solution["double_exp"].fit_report()

    def lorentz(self, mod):
        min = np.asarray(self.x).min()
        max = np.asarray(self.x).max()
        moy = (min + max) / 2
        gmodel = Model(mod)
        gmodel.set_param_hint('gamma_l', min=0)
        gmodel.set_param_hint('mu_l', min=min, max=max)
        self.solution["lorentz"] = gmodel.fit(self.y, x=self.x, mu_l=moy, gamma_l=1, add_l=1, method='powell')
        print(self.solution["lorentz"].fit_report())
        self.master.info(self.solution["lorentz"].fit_report())
        self.solution["lorentz_fit"] = [self.solution["lorentz"].best_values['mu_l'],
                                        self.solution["lorentz"].best_values['gamma_l'],
                                        self.solution["lorentz"].best_values['add_l']]
        return self.solution["lorentz_fit"], self.solution["lorentz"].fit_report()

    def double_lorentz(self, mod):
        min = np.asarray(self.x).min()
        max = np.asarray(self.x).max()
        moy1 = (min + max) / 2 + 5
        moy2 = (min + max) / 2 - 5
        gmodel = Model(mod)
        gmodel.set_param_hint('gamma1_dl', min=0)
        gmodel.set_param_hint('gamma2_dl', min=0)
        gmodel.set_param_hint('mu1_dl', min=min, max=max)
        gmodel.set_param_hint('mu2_dl', min=min, max=max)
        self.solution["double_lorentz"] = gmodel.fit(self.y, x=self.x, mu1_dl=moy1, gamma1_dl=2, mu2_dl=moy2,
                                                     gamma2_dl=2, add_dl=1, method='powell')
        print(self.solution["double_lorentz"].fit_report())
        self.master.info(self.solution["double_lorentz"].fit_report())
        self.solution["double_lorentz_fit"] = [self.solution["double_lorentz"].best_values['mu1_dl'],
                                               self.solution["double_lorentz"].best_values['gamma1_dl'],
                                               self.solution["double_lorentz"].best_values['mu2_dl'],
                                               self.solution["double_lorentz"].best_values['gamma2_dl'],
                                               self.solution["double_lorentz"].best_values['add_dl']]
        return self.solution["double_lorentz_fit"], self.solution["double_lorentz"].fit_report()

    def linear(self, mod):
        gmodel = Model(mod)
        self.solution["linear"] = gmodel.fit(self.y, x=self.x, a_l=0, b_l=0, method='powell')
        print(self.solution["linear"].fit_report())
        self.master.info(self.solution["linear"].fit_report())
        self.solution["linear_fit"] = [self.solution["linear"].best_values['a_l'],
                                       self.solution["linear"].best_values['b_l']]
        return self.solution["linear_fit"], self.solution["linear"].fit_report()


# MODELS Emission

def model_simple_gaussian_emission(x, sigma1_g, mu1_g, add_g):
    return 1 / (sigma1_g * np.sqrt(2 * np.pi) + e) * np.exp(
        - 1 / 2 * ((x - mu1_g) / (sigma1_g + e)) ** 2) + add_g


def model_double_gaussian_emission(x, sigma1_dg, mu1_dg, sigma2_dg, mu2_dg, add_dg):
    return 1 / (sigma1_dg * np.sqrt(2 * np.pi) + e) * np.exp(- 1 / 2 * ((x - mu1_dg) / (sigma1_dg + e)) ** 2) \
           + 1 / (sigma2_dg * np.sqrt(2 * np.pi) + e) * np.exp(- 1 / 2 * ((x - mu2_dg) / (sigma2_dg + e)) ** 2) + add_dg


def model_lorentz_emission(x, mu_l, gamma_l, add_l):
    return (2 / (np.pi * gamma_l + e)) / (1 + ((x - mu_l) / (0.5 * gamma_l + e)) ** 2) + add_l


def model_double_lorentz_emission(x, mu1_dl, gamma1_dl, mu2_dl, gamma2_dl, add_dl):
    return (2 / (np.pi * gamma1_dl + e)) / (1 + ((x - mu1_dl) / (0.5 * gamma1_dl + e)) ** 2) + \
           (2 / (np.pi * gamma2_dl + e)) / (1 + ((x - mu2_dl) / (0.5 * gamma2_dl + e)) ** 2) + add_dl


# MODELS Absorption

def model_simple_gaussian(x, sigma1_g, mu1_g, add_g):
    return - 1 / (sigma1_g * np.sqrt(2 * np.pi) + e) * np.exp(- 1 / 2 * ((x - mu1_g) / (sigma1_g + e)) ** 2) + add_g


def model_double_gaussian(x, sigma1_dg, mu1_dg, sigma2_dg, mu2_dg, add_dg):
    return - 1 / (sigma1_dg * np.sqrt(2 * np.pi) + e) * np.exp(- 1 / 2 * ((x - mu1_dg) / (sigma1_dg + e)) ** 2) \
           - 1 / (sigma2_dg * np.sqrt(2 * np.pi) + e) * np.exp(- 1 / 2 * ((x - mu2_dg) / (sigma2_dg + e)) ** 2) + add_dg


def model_lorentz(x, mu_l, gamma_l, add_l):
    return - (2 / (np.pi * gamma_l + e)) / (1 + ((x - mu_l) / (0.5 * gamma_l + e)) ** 2) + add_l


def model_double_lorentz(x, mu1_dl, gamma1_dl, mu2_dl, gamma2_dl, add_dl):
    return - (2 / (np.pi * gamma1_dl + e)) / (1 + ((x - mu1_dl) / (0.5 * gamma1_dl + e)) ** 2) \
           - (2 / (np.pi * gamma2_dl + e)) / (1 + ((x - mu2_dl) / (0.5 * gamma2_dl + e)) ** 2) + add_dl


# Models that apply to both:
def model_simple_expo(x, a_e, b_e, add_e):
    return a_e * np.exp(b_e * x) + add_e


def model_double_expo(x, a_de, b_de, c_de, d_de, add_de):
    return a_de * np.exp(b_de * x) + c_de * np.exp(
        d_de * x) + add_de


def model_linear(x, a_l, b_l):
    return a_l * x + b_l

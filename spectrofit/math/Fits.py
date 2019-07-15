import numpy as np
from lmfit import Model


class Fits:
    def __init__(self, data):
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])

        self.abs = 0

        self.solution = dict()

    # FITS
    def simple_gaussian(self, mod):
        gmodel = Model(mod)
        gmodel.set_param_hint('sigma1', min=0)
        gmodel.set_param_hint('mu1', min=656)
        gmodel.set_param_hint('add', min=0)
        self.solution["simple_gaussian"] = gmodel.fit(self.y, x=self.x, sigma1=1, mu1=1, add=1,
                                                      method='powell')
        print(self.solution["simple_gaussian"].fit_report())
        self.solution["simple_gaussian_fit"] = [self.solution["simple_gaussian"].best_values['sigma1'],
                                                self.solution["simple_gaussian"].best_values['mu1'],
                                                self.solution["simple_gaussian"].best_values['add']]
        return self.solution["simple_gaussian_fit"]

    def double_gaussian(self, mod):
        gmodel = Model(mod)
        gmodel.set_param_hint('sigma1', min=0)
        gmodel.set_param_hint('sigma2', min=0)
        gmodel.set_param_hint('mu1', min=656)
        gmodel.set_param_hint('mu2', min=656)
        gmodel.set_param_hint('add', min=0)
        self.solution["double_gaussian"] = gmodel.fit(self.y, x=self.x, sigma1=1, sigma2=1, mu1=1, mu2=1, add=1,
                                                      method='powell')
        print(self.solution["double_gaussian"].fit_report())
        self.solution["double_gaussian_fit"] = [self.solution["double_gaussian"].best_values['sigma1'],
                                                self.solution["double_gaussian"].best_values['mu1'],
                                                self.solution["double_gaussian"].best_values['sigma2'],
                                                self.solution["double_gaussian"].best_values['mu2'],
                                                self.solution["double_gaussian"].best_values['add']]
        return self.solution["double_gaussian_fit"]

    def simple_exp(self, mod):
        gmodel = Model(mod)
        self.solution["simple_exp"] = gmodel.fit(self.y, x=self.x, a=0, b=0, method='powell')
        print(self.solution["simple_exp"].fit_report())
        self.solution["simple_exp_fit"] = [self.solution["simple_exp"].best_values['a'],
                                           self.solution["simple_exp"].best_values['b']]
        return self.solution["simple_exp_fit"]

    def double_exp(self, mod):
        gmodel = Model(mod)
        self.solution["double_exp"] = gmodel.fit(self.y, x=self.x, a=0, b=0, c=0, d=0, method='powell')
        print(self.solution["double_exp"].fit_report())
        self.solution["double_exp_fit"] = [self.solution["double_exp"].best_values['a'],
                                           self.solution["double_exp"].best_values['b'],
                                           self.solution["double_exp"].best_values['c'],
                                           self.solution["double_exp"].best_values['d']]
        return self.solution["double_exp_fit"]

    def lorentz(self, mod):
        gmodel = Model(mod)
        gmodel.set_param_hint('gamma', min=0)
        gmodel.set_param_hint('mu', min=300, max=1100)
        self.solution["lorentz"] = gmodel.fit(self.y, x=self.x, mu=600, gamma=1, add=1, method='powell')
        print(self.solution["lorentz"].fit_report())
        self.solution["lorentz_fit"] = [self.solution["lorentz"].best_values['mu'],
                                        self.solution["lorentz"].best_values['gamma'],
                                        self.solution["lorentz"].best_values['add']]
        return self.solution["lorentz_fit"]

    def double_lorentz(self, mod):
        gmodel = Model(mod)
        gmodel.set_param_hint('gamma', min=0)
        gmodel.set_param_hint('gamma2', min=0)
        gmodel.set_param_hint('mu', min=300, max=1100)
        gmodel.set_param_hint('mu2', min=300, max=1100)
        self.solution["double_lorentz"] = gmodel.fit(self.y, x=self.x, mu=600, gamma=1, mu2=600, gamma2=1, add=1,
                                                     method='powell')
        print(self.solution["double_lorentz"].fit_report())
        self.solution["double_lorentz_fit"] = [self.solution["double_lorentz"].best_values['mu'],
                                               self.solution["double_lorentz"].best_values['gamma'],
                                               self.solution["double_lorentz"].best_values['mu2'],
                                               self.solution["double_lorentz"].best_values['gamma2'],
                                               self.solution["double_lorentz"].best_values['add']]
        return self.solution["double_lorentz_fit"]

    def linear(self, mod):
        gmodel = Model(mod)
        self.solution["linear"] = gmodel.fit(self.y, x=self.x, a=0, b=0, method='powell')
        print(self.solution["linear"].fit_report())
        self.solution["linear_fit"] = [self.solution["linear"].best_values['a'],
                                       self.solution["linear"].best_values['b']]
        return self.solution["linear_fit"]


# MODELS Emission

def model_simple_gaussian_emission(x, sigma1, mu1, add):
    return 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(
        + 1 / 2 * ((x - mu1) / sigma1) ** 2) + add


def model_double_gaussian_emission(x, sigma1, mu1, sigma2, mu2, add):
    return 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu1) / sigma1) ** 2) + 1 / (
                   sigma2 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu2) / sigma2) ** 2) + add


def model_lorentz_emission(x, mu, gamma, add):
    return (2 / (np.pi * gamma)) / (1 + ((x - mu) / (0.5 * gamma)) ** 2) + add


def model_double_lorentz_emission(x, mu, gamma, mu2, gamma2, add):
    return (2 / (np.pi * gamma)) / (1 + ((x - mu) / (0.5 * gamma)) ** 2) + (2 / (np.pi * gamma2)) / (
            1 + ((x - mu2) / (0.5 * gamma2)) ** 2) + add


# MODELS Absorption

def model_simple_gaussian(x, sigma1, mu1, add):
    return - 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu1) / sigma1) ** 2) + add


def model_double_gaussian(x, sigma1, mu1, sigma2, mu2, add):
    return - 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu1) / sigma1) ** 2) - 1 / (
                   sigma2 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu2) / sigma2) ** 2) + add


def model_lorentz(x, mu, gamma, add):
    return - (2 / (np.pi * gamma)) / (1 + ((x - mu) / (0.5 * gamma)) ** 2) + add


def model_double_lorentz(x, mu, gamma, mu2, gamma2, add):
    return - (2 / (np.pi * gamma)) / (1 + ((x - mu) / (0.5 * gamma)) ** 2) - (2 / (np.pi * gamma2)) / (
            1 + ((x - mu2) / (0.5 * gamma2)) ** 2) + add


# Models that apply to both:
def model_simple_expo(x, a, b):
    return a * np.exp(b * x)


def model_double_expo(x, a, b, c, d):
    return a * np.exp(b * x) + c * np.exp(
        d * x)


def model_linear(x, a, b):
    return a * x + b

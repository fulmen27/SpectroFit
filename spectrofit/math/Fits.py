import numpy as np
from scipy import optimize as opt
from lmfit import Model

import spectrofit.math.mathFunction as maf


class Fits:
    def __init__(self, data):
        self.x = np.array(data["x"])
        self.y = np.array(data["y"])

        self.solution = dict()

    # MODELS
    def model_simple_gaussian(self, coefficients):
        return 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
            - 0.5 * ((self.x - coefficients[1]) / coefficients[0]) ** 2) + coefficients[2]

    def model_double_gaussian(self, coefficients):
        return - 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
            - 1 / 2 * ((self.x - coefficients[1]) / coefficients[0]) ** 2) - 1 / (
                       coefficients[2] * np.sqrt(2 * np.pi)) * np.exp(
            - 1 / 2 * ((self.x - coefficients[3]) / coefficients[2]) ** 2) + coefficients[4]

    def model_simple_expo(self, coefficients):
        return coefficients[0] * np.exp(coefficients[1] * self.x)

    def model_double_expo(self, coefficients):
        return coefficients[0] * np.exp(coefficients[1] * self.x) + coefficients[2] * np.exp(
            coefficients[3] * self.x)

    def model_lorentz(self, coefficients):
        return (2 / (np.pi * coefficients[1])) / (1 + ((self.x - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + \
               coefficients[2]

    def model_linear(self, coefficients):
        return coefficients[0] * self.x + coefficients[1]

    # FITS
    def simple_gaussian(self):
        def residuals(coefficients):
            return self.y - self.model_simple_gaussian(coefficients)

        self.solution["simple_gaussian"] = opt.leastsq(residuals, np.ones(3))[0]
        return self.solution["simple_gaussian"]

    def double_gaussian(self):
        def residuals(coefficients):
            return self.y - self.model_double_gaussian(coefficients)

        gmodel = Model(maf.model_double_gaussian)
        gmodel.set_param_hint('sigma1', min=0)
        gmodel.set_param_hint('sigma1', min=0)
        gmodel.set_param_hint('add', min=0, max=2)
        self.solution["double_gaussian"] = gmodel.fit(self.y, x=self.x, sigma1=1, sigma2=1, mu1=1, mu2=1, add=1)
        print(self.solution["double_gaussian"].fit_report())
        return self.solution["double_gaussian"]

    def simple_exp(self):
        def residuals(coefficients):
            return self.y - self.model_simple_expo(coefficients)

        self.solution["simple_exp"] = opt.leastsq(residuals, np.ones(2))[0]
        return self.solution["simple_exp"]

    def double_exp(self):
        def residuals(coefficients):
            return self.y - self.model_double_expo(coefficients)

        self.solution["double_exp"] = opt.leastsq(residuals, np.ones(4))[0]
        return self.solution["double_exp"]

    def lorentz(self):
        gmodel = Model(maf.model_lorentz2)
        gmodel.set_param_hint('gamma', min=0)
        gmodel.set_param_hint('mu', min=300, max=1100)
        self.solution["lorentz"] = gmodel.fit(self.y, x=self.x, mu=600, gamma=1, add=1, method='powell')
        print(self.solution["lorentz"].fit_report())
        self.solution["lorentz_fit"] = [self.solution["lorentz"].best_values['mu'],
                                        self.solution["lorentz"].best_values['gamma'],
                                        self.solution["lorentz"].best_values['add']]
        return self.solution["lorentz_fit"]

    def linear(self):
        def residuals(coefficients):
            return self.y - self.model_linear(coefficients)

        self.solution["linear"] = opt.leastsq(residuals, np.ones(2))[0]
        return self.solution["linear"]

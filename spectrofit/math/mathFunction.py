import numpy as np


def model_simple_gaussian(x, coefficients):
    return 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
        - 0.5 * ((x - coefficients[1]) / coefficients[0]) ** 2) + coefficients[2]


def model_double_gaussian(x, sigma1, mu1, sigma2, mu2, add):
    return - 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu1) / sigma1) ** 2) - 1 / (
                   sigma2 * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - mu2) / sigma2) ** 2) + add


def model_simple_expo(x, coefficients):
    return coefficients[0] * np.exp(coefficients[1] * x)


def model_double_expo(x, coefficients):
    return coefficients[0] * np.exp(coefficients[1] * x) + coefficients[2] * np.exp(
        coefficients[3] * x)


def model_lorentz(x, coefficients):
    return - (2 / (np.pi * coefficients[1])) / (1 + ((x - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + \
               coefficients[2]


def model_lorentz2(x, mu, gamma, add):
    return - (2 / (np.pi * gamma)) / (1 + ((x - mu) / (0.5 * gamma)) ** 2) + add


def model_linear(x, coefficients):
    return coefficients[0] * x + coefficients[1]

import numpy as np


def model_simple_gaussian(x, coefficients):
    return 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
        - 0.5 * ((np.array(x) - coefficients[1]) / coefficients[0]) ** 2) + coefficients[2]


def model_double_gaussian(x, coefficients):
    return - 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((np.array(x) - coefficients[1]) / coefficients[0]) ** 2) \
           - 1 / (coefficients[2] * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((np.array(x) - coefficients[3]) / coefficients[2]) ** 2) + coefficients[4]


def model_simple_expo(x, coefficients):
    return coefficients[0] * np.exp(coefficients[1] * np.array(x))


def model_double_expo(x, coefficients):
    return coefficients[0] * np.exp(coefficients[1] * np.array(x)) + coefficients[2] * np.exp(
        coefficients[3] * np.array(x))


def model_lorentz(x, coefficients):
    return - (2 / (np.pi * coefficients[1])) / (1 + ((np.array(x) - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + \
           coefficients[2]


def model_double_lorentz(x, coefficients):
    return - (2 / (np.pi * coefficients[1])) / (
            1 + ((np.array(x) - coefficients[0]) / (0.5 * coefficients[1])) ** 2) - (
                   2 / (np.pi * coefficients[3])) / (
                   1 + ((np.array(x) - coefficients[2]) / (0.5 * coefficients[3])) ** 2) + coefficients[4]


def model_linear(x, coefficients):
    return coefficients[0] * np.array(x) + coefficients[1]


def model_simple_gaussian_emission(x, coefficients):
    return 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - coefficients[1]) / coefficients[0]) ** 2) + coefficients[2]


def model_double_gaussian_emission(x, coefficients):
    return 1 / (coefficients[0] * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - coefficients[1]) / coefficients[0]) ** 2) + 1 / (
                   coefficients[2] * np.sqrt(2 * np.pi)) * np.exp(
        - 1 / 2 * ((x - coefficients[3]) / coefficients[2]) ** 2) + coefficients[4]


def model_lorentz_emission(x, coefficients):
    return (2 / (np.pi * coefficients[1])) / (1 + ((x - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + \
           coefficients[2]


def model_double_lorentz_emission(x, coefficients):
    return (2 / (np.pi * coefficients[1])) / (1 + ((x - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + (
            2 / (np.pi * coefficients[3])) / (1 + ((x - coefficients[2]) / (0.5 * coefficients[3])) ** 2) + \
           coefficients[4]

import matplotlib.pyplot as plt
import numpy as np


def model_lorentz(x, coefficients):
    return - (2 / (np.pi * coefficients[1])) / (1 + ((x - coefficients[0]) / (0.5 * coefficients[1])) ** 2) + \
           coefficients[2]


sol = [6.38951698e+07, -4.72605475e+05,  9.25324675e-01]

x = np.array([0.01 * i for i in range(10000)])
y = model_lorentz(x, sol)

plt.plot(x, y)
plt.show()

import numpy as np
from lmfit import Model


def func(model, a=5, b=6):
    print(eval(model))

mod = input()
model = Model(func)

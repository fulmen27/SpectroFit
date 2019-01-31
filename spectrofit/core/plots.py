import matplotlib.pyplot as plt
import pylab as pl


def plot_ordre(my_import, x_lower, x_upper):
    fig = plt.gcf()
    ax = plt.gca()

    ax.set_xlim(float(my_import.data["lambda"][x_lower]), float(my_import.data["lambda"][x_upper]))
    ax.set_ylim(0, 2)

    plt.plot(my_import.data["lambda"][x_lower: x_upper], my_import.data["yspectre"][x_lower: x_upper], color='red')

    y = [0.1 for _ in
         range(len(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]]))]
    pl.scatter(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]], y,
               color='green', s=0.1)

    return fig





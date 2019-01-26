import matplotlib.pylab as plt


def plot_ordre(my_import, x_lower, x_upper):

    fig = plt.gcf()
    ax = plt.gca()

    ax.set_xlim(float(my_import.data["lambda"][x_lower]), float(my_import.data["lambda"][x_upper]))
    ax.set_ylim(0, 2)

    plt.plot(my_import.data["lambda"][x_lower: x_upper], my_import.data["yspectre"][x_lower: x_upper], color='red')

    plt.show()

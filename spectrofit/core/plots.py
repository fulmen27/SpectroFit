import matplotlib.pyplot as plt


def plot_ordre(my_import, x_lower, x_upper):
    print(my_import.data["lambda"][x_lower: x_upper])
    print(my_import.data["yspectre"][x_lower: x_upper])

    fig = plt.gcf()
    ax = plt.gca()

    ax.set_xlim(my_import.data["lambda"][x_lower], my_import.data["lambda"][x_upper])
    ax.set_ylim(0, 1.2)

    plt.plot(my_import.data["lambda"][x_lower: x_upper], my_import.data["yspectre"][x_lower: x_upper])

    plt.show()

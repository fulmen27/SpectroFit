import matplotlib.pyplot as plt
import pylab as pl

from spectrofit.core.compute_delim import compute_delim


def plot_ordre(my_import, order=0, btn_state=False):
    fig = plt.figure(figsize=(25, 10))
    ax = plt.gca()
    lim = compute_delim(my_import, num_ordre=order, btn_state=btn_state)

    if my_import.type == "fits":

        idx1 = my_import.fits_data["Wav"].columns.get_loc("Wavelength1")
        idx2 = my_import.fits_data["Wav"].columns.get_loc("Intensity")

        x = my_import.fits_data["Wav"].iloc[lim[0]: lim[1], idx1].to_numpy()
        y = my_import.fits_data["Wav"].iloc[lim[0]: lim[1], idx2].to_numpy()
        print(x)
        print(y)

        ax.set_xlim(int(min(x)), int(max(x)) + 1)
        ax.set_ylim(min(y), max(y))
        ax.plot(x, y, color='red')

        y = [0.1 for _ in
             range(len(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]]))]
        pl.scatter(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]], y,
                   color='green', s=0.1)

    elif my_import.type == "s" or my_import.type == "csv":

        ax.set_xlim(float(my_import.data["lambda"][lim[0]]), float(my_import.data["lambda"][lim[1]]))

        plt.plot(my_import.data["lambda"][lim[0]: lim[1]], my_import.data["yspectre"][lim[0]: lim[1]], color='red')

        y = [0.1 for _ in
             range(len(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]]))]
        pl.scatter(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]], y,
                   color='green', s=0.1)

    else:
        raise ValueError("Cannot plot data from this type of file")

    return fig, ax, lim


def plot_from_xy_list(args):
    fig = plt.figure(figsize=(25, 10))
    ax = plt.gca()
    ax.set_xlim(int(min(args["x"])), int(max(args["x"])) + 1)
    ax.set_ylim(min(args["y"]), max(args["y"]))
    plt.plot(args["x"], args["y"], color='red')

    return fig, ax

import matplotlib.pyplot as plt
import pylab as pl

from spectrofit.core.compute_delim import compute_delim


def plot_ordre(my_import, order=0, btn_state=False):
    fig = plt.figure(figsize=(25, 10))  # create figure
    ax = plt.gca()  # create axis
    lim = compute_delim(my_import, num_ordre=order, btn_state=btn_state)  # compute limit according to order

    if my_import.type == "fits":  # Neo Narval file

        idx1 = my_import.fits_data["Wav"].columns.get_loc("Wavelength1")
        idx2 = my_import.fits_data["Wav"].columns.get_loc("Intensity")
        idx3 = my_import.fits_data["Wav"].columns.get_loc("Error")

        # get data :

        x = my_import.fits_data["Wav"].iloc[lim[0]: lim[1], idx1].to_numpy()
        y = my_import.fits_data["Wav"].iloc[lim[0]: lim[1], idx2].to_numpy()
        error = my_import.fits_data["Wav"].iloc[lim[0]: lim[1], idx3].to_numpy()

        # set axis lim
        ax.set_xlim(int(min(x)), int(max(x)) + 1)
        ax.set_ylim(min(y - error), max(y + error))
        ax.plot(x, y, color='red')  # plot curve
        ax.fill_between(x, y - error, y + error, edgecolor='#CC4F1B', facecolor='#FF9848', alpha=0.3)  # error bar

        y = [0.1 for _ in
             range(len(my_import.lineident["lambda"][
                       my_import.lineident["x_lower"]: my_import.lineident["x_upper"]]))]  # get lnown elements to plot
        pl.scatter(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]], y,
                   color='green', s=0.1)  # plot known elements

    elif my_import.type == "s" or my_import.type == "csv":  # Narval file

        ax.set_xlim(float(my_import.data["lambda"][lim[0]]), float(my_import.data["lambda"][lim[1]]))  # set lim

        plt.plot(my_import.data["lambda"][lim[0]: lim[1]], my_import.data["yspectre"][lim[0]: lim[1]],
                 color='red')  # plot curve in figure

        y = [0.1 for _ in
             range(len(my_import.lineident["lambda"][
                       my_import.lineident["x_lower"]: my_import.lineident["x_upper"]]))]  # get lnown elements to plot

        pl.scatter(my_import.lineident["lambda"][my_import.lineident["x_lower"]: my_import.lineident["x_upper"]], y,
                   color='green', s=0.1)  # plot known elements

    else:  # Unknown format
        raise ValueError("Cannot plot data from this type of file")

    return fig, ax, lim


def plot_from_xy_list(args):
    fig = plt.figure(figsize=(25, 10))
    ax = plt.gca()
    ax.set_xlim(int(min(args["x"])), int(max(args["x"])) + 1)
    ax.set_ylim(min(args["y"]), max(args["y"]))
    plt.plot(args["x"], args["y"], color='red')

    return fig, ax

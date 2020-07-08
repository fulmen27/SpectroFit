def compute_delim(my_import, num_ordre=None, btn_state=False):
    if my_import.type == "s" or my_import.type == "s":
        x_lower = 0
        x_upper = 0
        lower_lim = None
        upper_lim = None
        if btn_state:
            x_lower = 1
            x_upper = -1
            my_import.lineident["x_lower"] = 1
            my_import.lineident["x_upper"] = -1
        else:
            order = 'ordre_{}'.format(int(num_ordre))
            lower_lim = float(my_import.delim["delim_data"][order]['lim_basse'])
            upper_lim = float(my_import.delim["delim_data"][order]['lim_haute'])

            for i in range(len(my_import.data["lambda"])):
                if lower_lim <= float(my_import.data["lambda"][i]) and x_lower == 0:
                    x_lower = i
                if float(my_import.data["lambda"][i]) >= upper_lim and x_upper == 0:
                    x_upper = i-1
                    break

            for j in range(int(x_lower), int(x_upper)):
                if float(my_import.data["lambda"][j]) > float(my_import.data["lambda"][j+1]):
                    x_lower = j+1
                    break

    elif my_import.type == "fits":
        x_lower = my_import.fits_data["order"].loc[num_ordre, "Orderlimit"]
        x_upper = my_import.fits_data["order"].loc[num_ordre + 1, "Orderlimit"]
        lower_lim = my_import.fits_data["Wav"].loc[x_lower, "Wavelength1"]
        upper_lim = my_import.fits_data["Wav"].loc[x_upper, "Wavelength1"]
    else:
        raise ValueError("Can't find limitation for this type of file")

    my_import.lineident["x_lower"] = None
    my_import.lineident["x_upper"] = None

    for k in range(len(my_import.lineident["lambda"])):
        if lower_lim < my_import.lineident["lambda"][k] and my_import.lineident["x_lower"] is None:
            my_import.lineident["x_lower"] = k
        if upper_lim < my_import.lineident["lambda"][k] and my_import.lineident["x_upper"] is None:
            my_import.lineident["x_upper"] = k - 1

    return x_lower, x_upper, lower_lim, upper_lim

def compute_delim(my_import, num_ordre=None, btn_state=False):
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

        my_import.lineident["x_lower"] = None
        my_import.lineident["x_upper"] = None

        for k in range(len(my_import.lineident["lambda"])):
            if lower_lim < my_import.lineident["lambda"][k] and my_import.lineident["x_lower"] is None :
                my_import.lineident["x_lower"] = k
            if upper_lim < my_import.lineident["lambda"][k] and my_import.lineident["x_upper"] is None :
                my_import.lineident["x_upper"] = k - 1

    return x_lower, x_upper, lower_lim, upper_lim

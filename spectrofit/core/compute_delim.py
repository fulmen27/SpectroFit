def compute_delim(my_import, num_ordre, btn_state):
    x_lower = None
    x_upper = None
    if btn_state:
        x_lower = 1
        x_upper = -1
    else:
        order = 'ordre_{}'.format(int(num_ordre))
        lower_lim = float(my_import.delim["delim_data"][order]['lim_basse'])
        upper_lim = float(my_import.delim["delim_data"][order]['lim_haute'])

        for i in range(len(my_import.data["lambda"])):
            if lower_lim <= float(my_import.data["lambda"][i]) and x_lower is None:
                x_lower = i
            if float(my_import.data["lambda"][i]) >= upper_lim and x_upper is None:
                x_upper = i-1
                break

        for j in range(int(x_lower), int(x_upper)):
            if float(my_import.data["lambda"][j]) > float(my_import.data["lambda"][j+1]):
                x_lower = j+1
                break

    return x_lower, x_upper


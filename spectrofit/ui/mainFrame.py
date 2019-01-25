import tkinter as tk
import tkinter.ttk as ttk

from spectrofit.core.CSVfile import ImportCSV


class MainFrame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.compute_button = None
        self.canvas = None
        self.full = tk.BooleanVar(self, True)
        self.my_import = None

        self._set_ui()

    def _set_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Menu
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Ouvrir un fichier CSV", command=self._open_csv)
        menu_file.add_command(label="Nettoyer le canvas", command=self._clean_canvas)
        menu_file.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        self.master.config(menu=menu_bar)

        # Buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(column=1, row=0, sticky="nsew")

        self.compute_button = ttk.Button(buttons_frame, text="Csv", command=self._on_compute, state=tk.DISABLED)
        self.compute_button.pack(fill=tk.BOTH)

        ttk.Checkbutton(buttons_frame, text="Full_spectre", variable=self.full).pack(fill=tk.BOTH)

        self.grid(column=0, row=0, sticky="nsew")

    def _on_compute(self):
        #On fais le découpage des spectres + affichage de l'ordre voulu par l'utilisateur
        print('_on_compute')
        self.my_import.__str__()

    def _open_csv(self):
        #on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportCSV()
        self.compute_button.config(state=tk.NORMAL)

    def _clean_canvas(self):
        #on clean l'affichage
        print("_clean_canvas")

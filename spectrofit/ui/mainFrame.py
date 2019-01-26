import tkinter as tk
import tkinter.ttk as ttk

from spectrofit.core.CSVfile import ImportCSV
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre


class MainFrame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master

        self.compute_button = None
        self.ent = None
        self.canvas = None
        self.full = tk.BooleanVar(self, False)
        self.my_import = None
        self.num_ordre = tk.DoubleVar(master, 0.0)
        self.num_ordre.set(0)

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

        self.compute_button = ttk.Button(buttons_frame, text="Compute", command=self._on_compute, state=tk.DISABLED)
        self.compute_button.grid(column=1, row=0)

        ttk.Checkbutton(buttons_frame, text="Full_spectre", variable=self.full).grid(column=1, row=1)

        text = tk.StringVar()
        text.set("Choisi ton ordre : ")
        text_label = tk.Label(self.master, textvariable=text)
        text_label.grid(column=1, row=2)

        self.ent = tk.Entry(self.master, textvariable=self.num_ordre)
        self.ent.grid(column=1, row=3)
        self.ent.configure(textvariable=self.num_ordre)

        self.grid(column=1, row=0, sticky="nsew")

    def _on_compute(self):
        # On fais le découpage des spectres + affichage de l'ordre voulu par l'utilisateur
        print('_on_compute')
        x, y = compute_delim(self.my_import, self.num_ordre.get(), self.full.get())
        plot_ordre(self.my_import, x, y)

    def _open_csv(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportCSV()
        self.compute_button.config(state=tk.NORMAL)

    def _clean_canvas(self):
        # on clean l'affichage
        print("_clean_canvas")

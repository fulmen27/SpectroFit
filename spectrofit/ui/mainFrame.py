import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler

from spectrofit.core.CSVfile import ImportCSV
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre


class MainFrame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.bind("<Button-1>", self._on_left_click)

        self.compute_button = None
        self.ent = None
        self.canvas = None
        self.full = tk.BooleanVar(self, False)
        self.my_import = None
        self.num_ordre = tk.DoubleVar(master, 0.0)
        self.num_ordre.set(0)
        self.canvas = None
        self.fig = None
        self.toolbar = None

        self.data = {"x": [], "y": []}

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
        self.compute_button.pack(fill=tk.BOTH)
        self.clean_button = ttk.Button(buttons_frame, text="clean", command=self._clean_canvas, state=tk.NORMAL)
        self.clean_button.pack(fill=tk.BOTH)

        ttk.Checkbutton(buttons_frame, text="Full spectre", variable=self.full).pack(fill=tk.BOTH)

        text = tk.StringVar()
        text.set("Choisi ton ordre : ")
        text_label = tk.Label(buttons_frame, textvariable=text)
        text_label.pack(fill=tk.BOTH)

        self.ent = tk.Entry(buttons_frame, textvariable=self.num_ordre)
        self.ent.pack(fill=tk.BOTH)
        self.ent.configure(textvariable=self.num_ordre)

        self.grid(column=1, row=0, sticky="nsew")

    def _on_compute(self):
        x, y = compute_delim(self.my_import, self.num_ordre.get(), self.full.get())
        self.fig = plot_ordre(self.my_import, x, y)
        self._set_canvas()

    def _open_csv(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportCSV()
        self.compute_button.config(state=tk.NORMAL)

    def _on_left_click(self, event):
        """SET POINTS"""
        self.data["x"].append(event.xdata)
        self.data["y"].append(event.ydata)
        self._add_point(event.x, event.y)

    def _set_canvas(self):
        canvas_frame = ttk.Frame(self)
        canvas_frame.grid(column=0, row=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.mpl_connect('button_press_event', self._on_left_click)
        # self.fig.canvas.callbacks.connect("<Button-1>", self._on_click)
        # self.fig.canvas.get_tk_widget().bind("<Button-1>", self._on_click)
        self.grid(column=0, row=0, sticky="nsew")

        toolbar_frame = ttk.Frame(master=self.master)
        toolbar_frame.grid(column=0, row=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

    def on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    def _clean_canvas(self):
        # on clean l'affichage
        print("_clean_canvas : coming soon")

    def _add_point(self, x, y):
        self.canvas.get_tk_widget().create_oval(x - 4, self.canvas.get_tk_widget().winfo_height() - (y - 4), x + 4,
                                                self.canvas.get_tk_widget().winfo_height() - (y + 4), fill='green')

    def _on_click(self, event):
        print('click')

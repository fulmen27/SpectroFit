import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import sys

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

from PySide2.QtWidgets import QApplication, QWidget

from spectrofit.core.CSVfile import ImportFile
from spectrofit.core.compute_delim import compute_delim
from spectrofit.core.plots import plot_ordre

from spectrofit.math.Fits import Fits
import spectrofit.math.mathFunction as mF

from spectrofit.tools.elements_table import ElementTable


class MainFrame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.bind("<Button-1>", self._on_left_click)

        self.compute_button = None
        self.clean_button = None
        self.fit_button = None
        self.ent = None
        self.canvas = None
        self.toolbar = None

        self.full = tk.BooleanVar(self, False)
        self.absorb = tk.BooleanVar(self, False)
        self.num_ordre = tk.DoubleVar(master, 0.0)

        self.my_import = None
        self.num_ordre.set(0)
        self.fig = None
        self.ax = None

        self.lim = []
        self.data = {"x": [], "y": []}
        self.fits = Fits(self.data)

        self.element_table = None
        self.app = None

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
        menu_file.add_command(label="Ouvrir un fichier S", command=self._open_s)
        menu_file.add_command(label="Nettoyer le canvas", command=self._clean_canvas)
        menu_file.add_command(label="Quitter", command=self.Quit)
        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        menu_tools = tk.Menu(menu_bar, tearoff=0)
        menu_tools.add_command(label="Find Ray", command=self._find_ray)
        menu_bar.add_cascade(label="Outils", menu=menu_tools)

        self.master.config(menu=menu_bar)

        # Buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(column=1, row=0, sticky="nsew")

        self.compute_button = ttk.Button(buttons_frame, text="Compute", command=self._on_compute, state=tk.DISABLED)
        self.compute_button.pack(fill=tk.BOTH)
        self.clean_button = ttk.Button(buttons_frame, text="clean", command=self._clean_canvas, state=tk.DISABLED)
        self.clean_button.pack(fill=tk.BOTH)
        self.fit_button = ttk.Button(buttons_frame, text="fit", command=self._fit_algo, state=tk.DISABLED)
        self.fit_button.pack(fill=tk.BOTH)

        ttk.Checkbutton(buttons_frame, text="Full spectre", variable=self.full).pack(fill=tk.BOTH)

        text = tk.StringVar()
        text.set("Choisi ton ordre : ")
        text_label = tk.Label(buttons_frame, textvariable=text)
        text_label.pack(fill=tk.BOTH)

        self.ent = tk.Entry(buttons_frame, textvariable=self.num_ordre)
        self.ent.pack(fill=tk.BOTH)
        self.ent.configure(textvariable=self.num_ordre)

        quit_button = ttk.Button(buttons_frame, text='QUIT', command=self.Quit)
        quit_button.pack(fill=tk.BOTH)

        self.grid(column=1, row=0, sticky="nsew")

    def _on_compute(self):
        self.lim = compute_delim(self.my_import, self.num_ordre.get(), self.full.get())
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1])
        self._set_canvas()

    def _open_csv(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportFile("csv")
        self.compute_button.config(state=tk.NORMAL)
        self.clean_button.config(state=tk.NORMAL)

    def _open_s(self):
        # on ouvre le fichier que l'on fait choisir par l'utilisateur
        self.my_import = ImportFile("s")
        self.compute_button.config(state=tk.NORMAL)
        self.clean_button.config(state=tk.NORMAL)

    def _on_left_click(self, event):
        """SET POINTS"""
        self.data["x"].append(event.xdata)
        self.data["y"].append(event.ydata)
        self.fits.x = np.append(self.fits.x, event.xdata)
        self.fits.y = np.append(self.fits.y, event.ydata)
        self._add_point(event.x, event.y)
        if len(self.data["x"]) > 5:
            self.fit_button.config(state=tk.NORMAL)

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

    def _clean_list(self):
        self.data["x"] = []
        self.data["y"] = []
        self.fits.x = []
        self.fits.y = []

    def _clean_canvas(self):
        # on clean l'affichage
        self.fit_button.config(state=tk.DISABLED)
        self._clean_list()
        self.canvas.get_tk_widget().delete("all")

    def _add_point(self, x, y):
        self.canvas.get_tk_widget().create_oval(x - 4, self.canvas.get_tk_widget().winfo_height() - (y - 4), x + 4,
                                                self.canvas.get_tk_widget().winfo_height() - (y + 4), fill='green')

    def _find_ray(self):
        self.app = QApplication(sys.argv)
        window = QWidget()
        self.element_table = ElementTable(window)
        self.app.exec_()

    # FITS PART
    def _fit_algo(self):
        window = tk.Toplevel(self.master)
        text = tk.StringVar()
        text.set("Choisi ton fit : ")
        text_label = tk.Label(window, textvariable=text)
        text_label.pack(fill=tk.BOTH)

        simple_gaussian = ttk.Button(window, text="Simple Gaussian", command=self._simple_gaussian, state=tk.NORMAL)
        simple_gaussian.pack(fill=tk.BOTH)
        double_gaussian = ttk.Button(window, text="Double Gaussian", command=self._double_gaussian, state=tk.NORMAL)
        double_gaussian.pack(fill=tk.BOTH)
        simple_expo = ttk.Button(window, text="Simple Expo", command=self._simple_expo, state=tk.NORMAL)
        simple_expo.pack(fill=tk.BOTH)
        double_expo = ttk.Button(window, text="Double Expo", command=self._double_expo, state=tk.NORMAL)
        double_expo.pack(fill=tk.BOTH)
        lorentz = ttk.Button(window, text="Lorentz", command=self._lorentz, state=tk.NORMAL)
        lorentz.pack(fill=tk.BOTH)
        double_lorentz = ttk.Button(window, text="Double Lorentz", command=self._double_lorentz, state=tk.NORMAL)
        double_lorentz.pack(fill=tk.BOTH)
        linear = ttk.Button(window, text="Linear", command=self._linear, state=tk.NORMAL)
        linear.pack(fill=tk.BOTH)
        ttk.Checkbutton(window, text="Spectre absorption ?", variable=self.absorb).pack(fill=tk.BOTH)

    def _simple_gaussian(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.simple_gaussian()
        y = mF.model_simple_gaussian(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_gaussian(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.double_gaussian()
        y = mF.model_double_gaussian(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _simple_expo(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.simple_exp()
        y = mF.model_simple_expo(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_expo(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.double_exp()
        y = mF.model_double_expo(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _linear(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.linear()
        y = mF.model_linear(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _lorentz(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.lorentz()
        y = mF.model_lorentz(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    def _double_lorentz(self):
        self.fits.abs = self.absorb.get()
        sol = self.fits.double_lorentz()
        y = mF.model_double_lorentz(self.data["x"], sol)
        self.fig, self.ax = plot_ordre(self.my_import, self.lim[0], self.lim[1], x_fit=self.data["x"], y_fit=y)
        self._set_canvas()
        self._clean_list()

    # DESTROY()
    def Quit(self):
        self.canvas.get_tk_widget().delete("all")
        self.canvas.get_tk_widget().destroy()
        self.master.destroy()
        self.tk.quit()

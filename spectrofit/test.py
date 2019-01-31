import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure

import numpy as np


def callback(event):
    print("clicked at", event.xdata, event.ydata)

root = tk.Tk()

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = np.arange(0.0,3.0,0.01)
s = np.sin(2*np.pi*t)

a.plot(t,s)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas.mpl_connect('button_press_event', callback)

toolbar = NavigationToolbar2Tk( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
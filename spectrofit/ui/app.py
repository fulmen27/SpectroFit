import tkinter as tk

from spectrofit.ui.mainFrame import MainFrame


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Spectro Fit")

        main_frame = MainFrame(self)
        main_frame.mainloop()


if __name__ == '__main__':
    app = App()

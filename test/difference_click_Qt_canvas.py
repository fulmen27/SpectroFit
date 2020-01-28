from PySide2 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton


import numpy as np


class PainterCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self._instructions = []
        self.axes = self.figure.add_subplot(111)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        width, height = self.get_width_height()
        for x, y, rx, ry, br_color in self._instructions:
            x_pixel, y_pixel_m = self.axes.transData.transform((x, y))
            # In matplotlib, 0,0 is the lower left corner,
            # whereas it's usually the upper right
            # for most image software, so we'll flip the y-coor
            y_pixel = height - y_pixel_m
            painter.setBrush(QtGui.QColor(br_color))
            painter.drawEllipse( QtCore.QPoint(x_pixel, y_pixel), rx, ry)

    def create_oval(self, x, y, radius_x=5, radius_y=5, brush_color="red"):
        self._instructions.append([x, y, radius_x, radius_y, brush_color])
        self.update()


class MyPaintWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.canvas = PainterCanvas()
        self.canvas.mpl_connect("button_press_event", self._on_left_click)
        x = np.arange(0, 10, 0.1)
        y = np.cos(x)
        self.canvas.axes.plot(x, y)

        layout_canvas = QtWidgets.QVBoxLayout(self)
        layout_canvas.addWidget(self.canvas)

    def _on_left_click(self, event):
        if event.button == MouseButton.LEFT:
            self.canvas.create_oval(event.xdata, event.ydata, brush_color="green")
        elif event.button == MouseButton.RIGHT:
            self.canvas.create_oval(event.xdata, event.ydata, brush_color="orange")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MyPaintWidget()
    w.show()
    sys.exit(app.exec_())

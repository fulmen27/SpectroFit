from PySide2.QtCore import QPoint
from PySide2.QtGui import QPainter, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PainterCanvas(FigureCanvas):
    def __init__(self, fig, ax, parent=None):
        self.fig = fig
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self._instructions = []
        self.axes = ax
        self.y_lim = self.axes.get_ylim()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        width, height = self.get_width_height()
        for x, y, rx, ry, br_color in self._instructions:
            x_pixel, y_pixel_m = self.axes.transData.transform((x, y))
            # In matplotlib, 0,0 is the lower left corner,
            # whereas it's usually the upper right
            # for most image software, so we'll flip the y-coor
            y_pixel = height - y_pixel_m
            painter.setBrush(QColor(br_color))
            painter.drawEllipse(QPoint(x_pixel, y_pixel), rx, ry)

    def create_oval(self, x, y, radius_x=5, radius_y=5, brush_color="green"):
        self._instructions.append([x, y, radius_x, radius_y, brush_color])
        self.update()

    def clean_canvas(self, l=None):
        if l is None:
            self._instructions = []
        else:
            for i in range(len(l)):
                j = 0
                while j < len(self._instructions):
                    if l[i][0] == self._instructions[j][0] and l[i][1] == self._instructions[j][1]:
                        self._instructions.pop(j)
                    j += 1
        self.update()

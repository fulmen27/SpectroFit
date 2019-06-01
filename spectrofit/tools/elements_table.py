from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

from silx.gui.widgets.PeriodicTable import PeriodicTable


class ElementTable(QWidget):

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.set_ui()
        self.window.show()

    def set_ui(self):
        layout = QVBoxLayout()
        b_pt = QPushButton('Periodic Table')
        b_pt.clicked.connect(self._start_periodic_table)
        layout.addWidget(b_pt)
        b_pt.show()
        btn_quit = QPushButton('Quit')
        btn_quit.clicked.connect(self.quit)
        layout.addWidget(btn_quit)
        btn_quit.show()
        self.window.setLayout(layout)

    @pyqtSlot(name="_start_periodic_table")
    def _start_periodic_table(self):
        self.pt = PeriodicTable()
        self.pt.sigElementClicked.connect(self._my_slot)
        self.pt.show()

    def _my_slot(self, item):
        self.pt.elementToggle(item)
        selected_elements = self.pt.getSelection()
        for e in selected_elements:
            print(e.symbol)

    @pyqtSlot(name="quit")
    def quit(self):
        self.window.close()

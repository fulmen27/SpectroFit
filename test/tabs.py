from PySide2.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, QGridLayout, \
    QCheckBox
from PySide2.QtCore import SIGNAL, QObject
import sys


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        layout.addWidget(self.tabs)

        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")

        print(self.tabs.currentIndex())

        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Tab 2")

        print(self.tabs.currentIndex())

        lay1 = QGridLayout(self.tab1)
        self.checkbox_states1 = {}
        for i, (key, text) in enumerate(
                (
                        ("Haar", "small"),
                        ("db", "small"),
                        ("sym", "small"),
                        ("coif", "very very very very long"),
                )
        ):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            lay1.addWidget(checkbox, i, 0)
            self.checkbox_states1[key] = checkbox

        self.process_wavelet1 = QPushButton("Process")
        lay1.addWidget(self.process_wavelet1, i, 1)
        QObject.connect(self.process_wavelet1, SIGNAL('clicked()'), self._on_process_wavelet)

        self.process_wavelet2 = QPushButton("suppr")
        lay1.addWidget(self.process_wavelet2, i + 1, 1)
        QObject.connect(self.process_wavelet2, SIGNAL('clicked()'), self.suppr)

        lay = QGridLayout(self.tab2)
        self.checkbox_states = {}
        for i, (key, text) in enumerate(
            (
                ("Haar", "small"),
                ("db", "small"),
                ("sym", "small"),
                ("coif", "very very very very long"),
            )
        ):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            lay.addWidget(checkbox, i, 0)
            self.checkbox_states[key] = checkbox

        self.process_wavelet = QPushButton("Process")
        lay.addWidget(self.process_wavelet, i, 1)
        QObject.connect(self.process_wavelet, SIGNAL('clicked()'), self._on_process_wavelet)

    def _on_process_wavelet(self):
        print(self.tabs.tabText(self.tabs.currentIndex()))
        print(self.tabs.currentIndex())
        print(self.tabs.count())

    def suppr(self):
        # self.tabs.removeTab(0)
        self.tabs.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

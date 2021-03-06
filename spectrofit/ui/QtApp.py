from PySide2.QtWidgets import QApplication, QWidget

from spectrofit.ui.QtmainFrame import MainFrame

import sys


class App(QWidget):
    def __init__(self, *args, **kwargs):
        self.app = QApplication(sys.argv)
        window = QWidget()

        super().__init__(window)

        self.main_frame = MainFrame(window)  # launch MainFrame

        self.app.exec_()  # Execute Qt App


if __name__ == '__main__':
    app = App()

import pywt
import numpy as np

from PySide2.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QCheckBox, QLabel, QLineEdit, \
    QComboBox
from PySide2.QtCore import SIGNAL, QObject
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SigProcToolbox(QWidget):

    """Class to handle all processing related to digital signal processing"""

    def __init__(self, main_frame):
        self.main_frame = main_frame
        # Initialize tab screen
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.tabs = QTabWidget()
        self.tabs.layout = QVBoxLayout()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.checkbox_states = {}
        self.wavelet_parameters = {}
        self.coeffs = dict()
        self.coeffs_zero = dict()
        self.coeffs_waverec = dict()
        self.checkbox_keep_wavelet = dict()
        self.attenauation_wavelet = dict()
        self.args = dict()
        self.fig_wavelet = dict()
        self.wavelet_combo_box = dict()
        self.sig_corrected = None
        self.order_decomp = None

        # Add tabs
        self.tabs.addTab(self.tab1, "Fourier Transform")
        self.tabs.addTab(self.tab2, "Wavelet Denoising")

        # Create first tab
        self._set_ui_tab1()


        # Create second tab
        self._set_ui_tab2()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.window.setLayout(self.layout)
        self.window.show()

    """
        FUNCTION TO SET USER INTERFACE OF DIFFERENT TABS
    """

    def _set_ui_tab1(self):
        self.tab1.layout = QVBoxLayout(self.tabs)
        self.pushButton1 = QPushButton("THIS PART WILL COME LATER")
        QObject.connect(self.pushButton1, SIGNAL('clicked()'), self.on_click)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

    def _set_ui_tab2(self):
        """"
               _set_ui_tab2

            @:brief
                Set user interface of the second tab : wavelet processing tab
                see pywt documentation

            @:parameter
                self

            @:return
                None
        """
        lay = QGridLayout(self.tab2)
        label = QLabel("Wavelet family :")
        lay.addWidget(label, 0, 1)
        # all possible method for wevelet processing
        for i, (key, text) in enumerate(
                (
                        ("haar", "Haar"),
                        ("db", "daubechies"),
                        ("sym", "Symlets"),
                        ("coif", "Coiflets"),
                        ("bior", "biorthogonal"),
                        ("rbio", "reverse-biorthogonal"),
                        ("dmey", "Discret FIR Meyer"),
                        ("gaus", "gaussian"),
                        ("mexh", "Mexican hat"),
                        ("morl", "morlet"),
                        ("cgau", "Complex Gaussian"),
                        ("shan", "Shanon"),
                        ("fbsp", "Frequency B-Spline"),
                        ("cmor", "Complex Morlet"),
                )
        ):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            lay.addWidget(checkbox, i + 1, 1)
            self.checkbox_states[key] = checkbox
            # set combo box with method
            self.wavelet_combo_box[key] = QComboBox()
            l = pywt.wavelist(key)
            self.wavelet_combo_box[key].addItems(l)
            lay.addWidget(self.wavelet_combo_box[key], i + 1, 2)

        # choose order of decomposition
        label_order_decomp = QLabel("choose order of decomposition : \t")
        lay.addWidget(label_order_decomp, 0, 0)
        self.order_decomp = QLineEdit()
        lay.addWidget(self.order_decomp, 1, 0)

        self.process_wavelet = QPushButton("Process")
        QObject.connect(self.process_wavelet, SIGNAL('clicked()'), self._on_process_wavelet)

        lay.addWidget(self.process_wavelet, i + 2, 3)
        self.tab2.setLayout(lay)

    """
        PROCESSING AND COMPUTATION FUNCTION TAB 1
    """

    def on_click(self):
        print("TBD")

    """
        PROCESSING AND COMPUTATION FUNCTION TAB 2
    """

    def _on_process_wavelet(self):
        """"
            _on_process_wavelet(self)

        @:brief
            This function is used to process all choices made by the user when it click on the process button on the
            second tab.

            We will check that user only checked one wavelet method box and that he entered all number need. Then we
            will store that information for further use

            We process the wavelet decomposition in this function

            Call wavelet_to_keep()

        @:parameter
            self

        @:return
            None
        """
        my_import = self.main_frame.dict_tabs["Tab_{}".format(self.main_frame.tabs.currentIndex())]["import"]
        x_lower = self.main_frame.dict_tabs["Tab_{}".format(self.main_frame.tabs.currentIndex())]["lim"][0]
        x_upper = self.main_frame.dict_tabs["Tab_{}".format(self.main_frame.tabs.currentIndex())]["lim"][1]
        s = 0
        for key, value in self.checkbox_states.items():
            if value.isChecked():
                self.wavelet_parameters["wavelet_family"] = self.wavelet_combo_box[key].currentText()
                s += 1

        if s != 1:
            self.main_frame.error("Error on check boxes : you have to check only one box")
        else:
            print("you have choose : {}".format(self.wavelet_parameters["wavelet_family"]))

            try:
                self.wavelet_parameters["order_decomp"] = int(self.order_decomp.text())
            except ValueError:
                self.main_frame.error("enter an integer as decomposition order")

            if my_import.type == "s" or my_import.type == "csv":
                sig = my_import.data["yspectre"][x_lower: x_upper]
            elif my_import.type == "fits":
                idx2 = my_import.fits_data["Wav"].columns.get_loc("Intensity")
                sig = my_import.fits_data["Wav"].iloc[x_lower: x_upper, idx2].to_numpy()
            else:
                raise ValueError("No x and y data for graph : unknown format of file")

            self.coeffs = pywt.wavedec(sig, self.wavelet_parameters["wavelet_family"],
                                       self.wavelet_parameters["order_decomp"])
            for j in range(len(self.coeffs)):
                self.coeffs_zero["{}".format(j)] = []
                for i in range(len(self.coeffs)):
                    if i != j:
                        self.coeffs_zero["{}".format(j)].append(np.asarray([0 for _ in range(len(self.coeffs[i]))]))
                    else:
                        self.coeffs_zero["{}".format(j)].append(np.asarray(self.coeffs[i]))

            for key, value in self.coeffs_zero.items():
                self.coeffs_waverec[key] = pywt.waverec(self.coeffs_zero[key],
                                                        self.wavelet_parameters["wavelet_family"])

            self.args["lower"] = x_lower
            self.args["upper"] = x_upper
            self.args["import"] = my_import
            self.args["lim"] = self.main_frame.dict_tabs["Tab_{}".format(self.main_frame.tabs.currentIndex())]["lim"]

            if my_import.type == "s" or my_import.type == "csv":
                self.args["x"] = my_import.data["lambda"][x_lower: x_upper]
            elif my_import.type == "fits":
                idx1 = my_import.fits_data["Wav"].columns.get_loc("Wavelength1")
                self.args["x"] = my_import.fits_data["Wav"].iloc[x_lower: x_upper, idx1].to_numpy()
            else:
                raise ValueError("No x and y data for graph : unknown format of file")

            self.wavelet_to_keep()

    def wavelet_to_keep(self):
        """
            wavelet_to_keep(self)

            @:brief
                Propose to the user all the results from the wavelet decomposition

                User have to choose what he wants to continue (which signals to keep with attenuation or not)
                If you select a graph and don't put a number in the attenuation column the default value is 1

                When button is click call : _on_wavelet_return

            @:parameter
                self

            @:return
                None
        """
        self.window = QWidget()
        lay = QGridLayout(self.window)
        i = 0
        label = QLabel("attenuation coeff (1 by default)")
        lay.addWidget(label, i, 2)
        for key, value in self.coeffs_waverec.items():
            checkbox = QCheckBox("Keep that part ?")
            checkbox.setChecked(False)
            self.checkbox_keep_wavelet[key] = checkbox
            lay.addWidget(checkbox, i + 1, 1)
            attenuation = QLineEdit()
            lay.addWidget(attenuation, i + 1, 2)
            self.attenauation_wavelet[key] = attenuation
            plt.close('all')
            figure = plt.gcf()
            figure.set_size_inches(20, 8)
            plt.plot(self.args["x"], self.coeffs_waverec[key][:len(self.args["x"])])
            self.fig_wavelet[key] = SigProcToolboxFig(figure)
            lay.addWidget(self.fig_wavelet[key], i + 1, 0)
            plt.close(figure)
            i += 1

        button = QPushButton("Process")
        QObject.connect(button, SIGNAL('clicked()'), self._on_wavelet_return)
        lay.addWidget(button, i + 1, 3)
        self.window.setLayout(lay)
        self.window.show()
        self.window.showMaximized()

    def _on_wavelet_return(self):
        """
            _on_wavelet_return

            @:brief
                Compute choices of the user for the wavelet processing

                Call MainFrame method : add_tab_from_wavelet(self.args) to add a tab with the processed signal

            @:parameter
                self

            @:return
                None
        """
        to_keep = dict()
        for key, value in self.checkbox_keep_wavelet.items():
            if value.isChecked():
                to_keep[key] = self.coeffs_waverec[key][:len(self.args["x"])]

        self.sig_corrected = 0
        for key, value in to_keep.items():
            try:
                print(self.attenauation_wavelet[key].text())
                q = float(self.attenauation_wavelet[key].text())
                if q < 0:
                    q = 0
                elif q > 1:
                    q = 1
            except ValueError:
                q = 1
            self.sig_corrected += to_keep[key] * q

        self.args["y"] = self.sig_corrected
        self.window.close()
        self.main_frame.add_tab_from_wavelet(self.args)


class SigProcToolboxFig(FigureCanvas):
    """
        A SIMPLE CLASS TO CREATE GRAPHS FOR WAVELET PROCESSING
    """
    def __init__(self, fig):
        self.fig = fig
        FigureCanvas.__init__(self, self.fig)

import csv
import json
from astropy.io import fits
import numpy as np
import pandas as pd

from PySide2.QtWidgets import QFileDialog, QMainWindow
import os


class ImportFile(QMainWindow):
    """Class to handle file import"""

    def __init__(self, type, master):

        super().__init__(master)

        self.master = master
        self.my_csv = dict()
        self.delim = dict()
        self.type = ""
        self.data = {"lambda": [], "yspectre": [], "3rd_col": []}
        self.fits_data = {}
        self.lineident = {"1st_col": [], "2nd_col": [], "3rd_col": [], "lambda": [], "element_name": []}

        self.delim["filename"] = "delim_ordre_TBL.json"

        # Check each type of file :
        if type == "s":
            self._open_s()
            self._open_delim()
        elif type == "csv":
            self._open_csv()
            self._open_delim()
        elif type == "fits":
            self._open_fits()

        self._open_lineident()
        self._lineident_json_to_dict()

    def __str__(self):
        print(self.my_csv)

    def _open_csv(self):

        """Open CSV file with data of Narval"""
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "*.csv;;*.*")

        if filename != "" and filename is not None and os.path.exists(filename[0]):
            self.my_csv["filename"] = filename[0]
            self.type = "csv"
            with open(self.my_csv["filename"], 'r') as my_file:
                self.my_csv["csv_file"] = csv.reader(my_file, delimiter=";")
                for row in self.my_csv["csv_file"]:
                    self.data["lambda"].append(float(row[0]))
                    self.data["yspectre"].append(float(row[1]))
                    self.data["3rd_col"].append(float(row[2]))
        else:
            raise ValueError("Filename empty or filename not find in path")

    def _open_s(self):
        """

            Open .s file with Narval data:
            first column : lambda
            second column : intensity of spectrum
            third column : error

        :return:
        """
        filename = QFileDialog.getOpenFileName(self, "S files", os.getcwd(), "*.s;;*.*")
        if filename != "" and filename is not None and os.path.exists(filename[0]):
            self.my_csv["filename"] = filename[0]
            self.type = "s"
            with open(self.my_csv["filename"]) as my_file:  # open file
                # read all lines, convert to float and store it in the right list
                for row in my_file:
                    r = row.rstrip().split(" ")
                    while '' in r:
                        r.remove('')
                    if len(r) == 3:
                        try:
                            self.data["lambda"].append(float(r[0]))
                            self.data["yspectre"].append(float(r[1]))
                            self.data["3rd_col"].append(float(r[2]))
                        except:
                            print("can't convert value go to next line")
        else:
            raise ValueError("Filename empty or filename not find in path")

    def _open_fits(self):
        """

        Open .fit file with data from NeoNarval instrument.

        :return:
        """
        filename = QFileDialog.getOpenFileName(self, "S files", os.getcwd(), "*.fits;;*.*")
        if filename != "" and filename is not None and os.path.exists(filename[0]):
            self.my_csv["filename"] = filename[0]
            f = fits.open(self.my_csv["filename"])  # open file
            self.type = "fits"
            error = True
            for i in range(len(f)):  # iterate through all table in fit's meta data
                try:
                    data = np.asarray(f[i].data)
                    pd_table = pd.DataFrame(data)
                    print(pd_table)
                    # check each table if it has wented data
                    # if yes, store it in a pandas dataframe
                    if "Wavelength1" in pd_table.columns and "Intensity" in pd_table.columns:
                        pd_table["Wavelength1"] = pd_table["Wavelength1"].divide(10.0)
                        if pd_table["Wavelength1"].iloc[0] > pd_table["Wavelength1"].iloc[-1]:
                            pd_table = pd_table.iloc[::-1]
                        self.fits_data["Wav"] = pd_table
                    elif "Velocity" in pd_table.columns and "Intensity" in pd_table.columns:
                        self.fits_data["vel"] = pd_table
                    elif "Orderlimit" in pd_table.columns:
                        self.fits_data["order"] = pd_table
                    else:
                        raise ValueError("Couldn't convert the table to a known format")
                    error = False

                except ValueError:
                    if len(f) == 1:
                        raise ValueError("Couldn't convert data")
                    else:
                        if i == len(f) - 1 and error:
                            raise ValueError("Couldn't convert any of the table")
                        else:
                            print("Error when converting one table : going to next")
        else:
            raise ValueError("Filename empty or filename not find in path")

    def _open_delim(self):
        """

            Open delim file to get the limit of each order
            Store limits in a list

        """
        self.delim["filename"] = "./spectrofit/core/delim_ordre_TBL.json"
        if os.path.exists(self.delim["filename"]):
            with open(self.delim["filename"]) as f:
                self.delim["delim_file"] = f
                self.delim["delim_data"] = json.load(f)
        else:
            raise ValueError("No delim order TBL (JSON file) found in path")

    def _open_lineident(self):

        """

        open lineident file. It contains all information on the lambda of each known elements
        Useful to plot line with fundamental ray for each element

        :return:
        """

        self.lineident["filename"] = 'lineident.csv'
        if os.path.exists('lineident.csv'):
            with open(self.lineident["filename"], 'r') as f:
                self.lineident["lineident_file"] = csv.reader(f, delimiter=";")
                for row in self.lineident["lineident_file"]:
                    self.lineident["1st_col"].append(float(row[0]))
                    self.lineident["2nd_col"].append(float(row[1]))
                    self.lineident["3rd_col"].append(float(row[2]))
                    self.lineident["lambda"].append(
                        float(row[3]) / 10)  # divide by ten because in file lambda in Angstrom
                    self.lineident["element_name"].append(row[4])
        else:
            raise ValueError("No lineident found in path")

    def _lineident_json_to_dict(self):
        with open("./spectrofit/core/lineident.json", 'r') as f:
            self.lineident_json = json.load(f)

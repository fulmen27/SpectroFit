import csv
import json
import os

from PySide2.QtWidgets import QFileDialog, QMainWindow
import os


class ImportFile(QMainWindow):
    def __init__(self, type, master):

        super().__init__(master)

        self.master = master
        self.my_csv = dict()
        self.delim = dict()
        self.data = {"lambda": [], "yspectre": [], "3rd_col": []}
        self.lineident = {"1st_col": [], "2nd_col": [], "3rd_col": [], "lambda": [], "element_name": []}

        self.delim["filename"] = "delim_ordre_TBL.json"

        if type == "s":
            self._open_s()
        elif type == "csv":
            self._open_csv()
        self._open_delim()
        self._open_lineident()
        self._lineident_json_to_dict()

    def __str__(self):
        print(self.my_csv)

    def _open_csv(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "*.csv;;*.*")

        if filename != "" and filename is not None and os.path.exists(filename[0]):
            self.my_csv["filename"] = filename[0]
            with open(self.my_csv["filename"], 'r') as my_file:
                self.my_csv["csv_file"] = csv.reader(my_file, delimiter=";")
                for row in self.my_csv["csv_file"]:
                    self.data["lambda"].append(float(row[0]))
                    self.data["yspectre"].append(float(row[1]))
                    self.data["3rd_col"].append(float(row[2]))
        else:
            raise ValueError("Filename empty or filename not find in path")

    def _open_s(self):
        filename = QFileDialog.getOpenFileName(self, "S files", os.getcwd(), "*.s;;*.*")
        if filename != "" and filename is not None and os.path.exists(filename[0]):
            self.my_csv["filename"] = filename[0]
            with open(self.my_csv["filename"]) as my_file:
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

    def _open_delim(self):
        # ouvrir et classer les delimitations des ordres
        self.delim["filename"] = "./spectrofit/core/delim_ordre_TBL.json"
        if os.path.exists(self.delim["filename"]):
            self.delim["delim_file"] = open(self.delim["filename"])
            self.delim["delim_data"] = json.load(self.delim["delim_file"])
            # pprint(self.delim["delim_data"])
            # print(self.delim["delim_data"]['ordre_32']['lim_basse'])
        else:
            raise ValueError("No delim order TBL (JSON file) found in path")

    def _open_lineident(self):
        self.lineident["filename"] = 'lineident.csv'
        if os.path.exists('lineident.csv'):
            with open(self.lineident["filename"], 'r') as f:
                self.lineident["lineident_file"] = csv.reader(f, delimiter=";")
                for row in self.lineident["lineident_file"]:
                    self.lineident["1st_col"].append(float(row[0]))
                    self.lineident["2nd_col"].append(float(row[1]))
                    self.lineident["3rd_col"].append(float(row[2]))
                    self.lineident["lambda"].append(float(row[3]) / 10)
                    self.lineident["element_name"].append(row[4])
        else:
            raise ValueError("No lineident found in path")

    def _lineident_json_to_dict(self):
        with open("./spectrofit/core/lineident.json", 'r') as f:
            self.lineident_json = json.load(f)

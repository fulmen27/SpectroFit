import csv
import json
import os
from pprint import pprint

from tkinter.filedialog import askopenfilename


class ImportCSV:
    def __init__(self):
        print("import_csv")
        self.my_csv = dict()
        self.delim = dict()
        self.data = {"lambda": [], "yspectre": [], "3rd_col": []}
        self.delim["filename"] = "delim_ordre_TBL.json"
        self._open_csv()
        self._open_delim()

    def __str__(self):
        print(self.my_csv)

    def _open_csv(self):
        filename = askopenfilename(title="Choisissez un fichier csv",
                                   filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))

        if filename != "" and filename is not None and os.path.exists(filename):
            self.my_csv["filename"] = filename
            with open(self.my_csv["filename"], 'r') as self.my_csv["filename"]:
                self.my_csv["csv_file"] = csv.reader(self.my_csv["filename"], delimiter=";")
                for row in self.my_csv["csv_file"]:
                    self.data["lambda"].append(float(row[0]))
                    self.data["yspectre"].append(float(row[1]))
                    self.data["3rd_col"].append(float(row[2]))

    def _open_delim(self):
        # ouvrir et classer les delimitations des ordres
        self.delim["filename"] = "./spectrofit/core/delim_ordre_TBL.json"
        self.delim["delim_file"] = open(self.delim["filename"])
        self.delim["delim_data"] = json.load(self.delim["delim_file"])
        # pprint(self.delim["delim_data"])
        # print(self.delim["delim_data"]['ordre_32']['lim_basse'])

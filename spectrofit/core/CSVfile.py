import csv
import os

from tkinter.filedialog import askopenfilename


class ImportCSV:
    def __init__(self):
        print("import_csv")
        self.my_csv = {}
        self.delim = {}
        self.delim["filename"] = "delim_ordre_TBL.json"
        self._open_csv()
        self._open_deim()

    def __str__(self):
        print(self.my_csv)

    def _open_csv(self):
        filename = askopenfilename(title="Choisissez un fichier csv",
                                   filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))

        if filename != "" and filename is not None and os.path.exists(filename):
            self.my_csv["filename"] = filename
            with open(self.my_csv["filename"], 'rb') as self.my_csv["filename"]:
                self.my_csv["csv_file"] = csv.reader(self.my_csv["filename"], delimiter=' ', quotechar='|')

    def _open_delim(self):
        #ouvrir et classer les delimitations des ordres
        with open(self.delim["filename"], 'rb') as self.delim["filename"]:
            self.delim["csv_file"] = csv.reader(self.delim["filename"], delimiter=' ', quotechar='|')

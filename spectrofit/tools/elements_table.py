from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTabWidget
from PySide2.QtCore import SIGNAL, QObject

from silx.gui.widgets import PeriodicTable


class ElementTable(QWidget):

    def __init__(self, master, window):
        super().__init__(window)
        self.master = master
        self.window = window
        self.set_ui()
        self.window.show()
        self.selected_elements = []

    def set_ui(self):
        layout = QVBoxLayout()
        b_pt = QPushButton('Periodic Table')
        QObject.connect(b_pt, SIGNAL('clicked()'), self._start_periodic_table)
        layout.addWidget(b_pt)
        b_pt.show()
        btn_quit = QPushButton('Quit')
        QObject.connect(btn_quit, SIGNAL('clicked()'), self.quit)
        layout.addWidget(btn_quit)
        btn_quit.show()
        self.window.setLayout(layout)

    def _start_periodic_table(self):
        self.w = QTabWidget()
        self.pt = PeriodicTable.PeriodicTable(self.w)
        self.pt.sigElementClicked.connect(self._my_slot)
        self.pc = PeriodicTable.PeriodicCombo(self.w)
        self.pl = PeriodicTable.PeriodicList(self.w)
        self.pl.sigSelectionChanged.connect(self.change_list)
        self.pc.sigSelectionChanged.connect(self.change_combo)

        comboContainer = QWidget(self.w)
        comboContainer.setLayout(QVBoxLayout())
        comboContainer.layout().addWidget(self.pc)

        self.w.addTab(self.pt, "PeriodicTable")
        self.w.addTab(self.pl, "PeriodicList")
        self.w.addTab(comboContainer, "PeriodicCombo")

        self.pt.show()
        self.pl.show()
        self.pc.show()

        self.w.show()

    def _my_slot(self, item):
        self.pt.elementToggle(item)
        tmp = list()
        for e in self.pt.getSelection():
            tmp.append(e.symbol)

        if len(tmp) > len(self.selected_elements):
            self.selected_elements = tmp
            self._plot_element()
        else:
            to_erase = list(set(self.selected_elements) - set(tmp))
            self._supress_plot_element(to_erase)
            self.selected_elements = tmp

    def _plot_element(self):
        e = self.selected_elements[-1]
        ordre = "ordre_{}".format(int(self.master.num_ordre.text()))
        x_lower = \
            self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["import"].delim["delim_data"][
                ordre][
                'lim_basse']
        x_upper = \
            self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["import"].delim["delim_data"][
                ordre][
                'lim_haute']
        ele_in_lims = []
        key_list = []

        for key in self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["import"].lineident_json[e]:
            if key != 'number':
                if x_lower < self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())][
                    "import"].lineident_json[e][key]["lambda"] < x_upper:
                    ele_in_lims.append(self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())][
                                           "import"].lineident_json[e][key]["lambda"])
                    key_list.append(key)

        y = [self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["canvas"].y_lim[0],
             self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["canvas"].y_lim[1]]
        for i in range(len(ele_in_lims)):
            x = [ele_in_lims[i], ele_in_lims[i]]
            self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].plot(x, y, linewidth=2.0,
                                                                                               linestyle='-.',
                                                                                               label="{}".format(
                                                                                                   key_list[i]),
                                                                                               color='b')
            self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].text(ele_in_lims[i],
                                                                                               self.master.dict_tabs[
                                                                                                   "Tab_{}".format(
                                                                                                       self.master.tabs.currentIndex())][
                                                                                                   "canvas"].y_lim[
                                                                                                   0], "{}".format(e),
                                                                                               color='b', fontsize=12)
            self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["fig"].canvas.draw()

    def _supress_plot_element(self, to_erase):
        k = 0
        l = len(self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].lines)
        for j in range(l):
            line = self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].lines[j - k]
            if line.get_label()[0:2].replace(" ", "") == to_erase[0]:
                self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].lines.remove(line)
                k += 1
        self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["fig"].canvas.draw()

        k = 0
        l = len(self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].texts)
        for j in range(l):
            txt = self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].texts[j - k]
            if txt.get_text() == to_erase[0]:
                self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["ax"].texts.remove(txt)
                k += 1
        self.master.dict_tabs["Tab_{}".format(self.master.tabs.currentIndex())]["fig"].canvas.draw()

    def change_list(self, items):
        print("New list selection:", [item.symbol for item in items])

    def change_combo(self, item):
        print("New combo selection:", item.symbol)

    def click_table(self, item):
        print("New table click: %s (%s)" % (item.name, item.subcategory))

    def quit(self):
        self.window.close()

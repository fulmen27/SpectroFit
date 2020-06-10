from PySide2.QtWidgets import QSlider
from PySide2.QtCore import Signal


class Slider(QSlider):
    # create our our signal that we can connect to if necessary
    doubleValueChanged = Signal(float)

    def __init__(self, decimals=3, *args, **kargs):
        super(Slider, self).__init__(*args, **kargs)
        self._multi = 10 ** decimals

        self.valueChanged.connect(self.emitDoubleValueChanged)

    def emitDoubleValueChanged(self):
        value = float(super(Slider, self).value()) / self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super(Slider, self).value()) / self._multi

    def setMinimum(self, value):
        return super(Slider, self).setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super(Slider, self).setMaximum(value * self._multi)

    def setSingleStep(self, value):
        return super(Slider, self).setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super(Slider, self).singleStep()) / self._multi

    def setValue(self, value):
        super(Slider, self).setValue(int(value * self._multi))

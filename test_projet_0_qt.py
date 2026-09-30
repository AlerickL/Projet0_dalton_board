from __future__ import annotations
#import test_projet_0 as mod
import sys
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGroupBox


class QSliderWithValue(QWidget):
    valueSliderChanged:Signal = Signal(int)
    def __init__(self, maximum: int=100,parent=None) -> None:
        super().__init__(parent)
        self.__slider:QSlider = QSlider()
        self.__slider.setOrientation(Qt.Orientation.Horizontal)
        self.__slider.setRange(0,maximum)
        self.__nber:QLabel = QLabel("0")

        layout:QHBoxLayout = QHBoxLayout()
        layout.addWidget(self.__slider)
        layout.addWidget(self.__nber)

        self.setLayout(layout)

        self.__slider.valueChanged.connect(self.__nber.setNum)
        self.valueSliderChanged.emit(self.__slider.valueChanged)

    @Slot(int)
    def setNum(self,value:int) ->None:
        # self.__nber.setNum(value)
        # self.valueSliderChanged.emit(value)
        self.__slider.setValue(value)

    def value(self) -> int:
        return self.__slider.value()

class QSliderValueTitle(QWidget):
    def __init__(self,title:str,maximum:int=100,parent=None):
        super().__init__(parent)
        titleLabel:QLabel = QLabel(title)
        self.__sliderValue:QSliderWithValue = QSliderWithValue(maximum)

        layout:QHBoxLayout = QHBoxLayout()
        layout.addWidget(titleLabel)
        layout.addWidget(self.__sliderValue)
        self.setLayout(layout)

    def value(self) -> int:
        return self.__sliderValue.value()

    

class QGaltonApp(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)


def main() -> None:
    app:QApplication = QApplication(sys.argv)

    w:QSliderWithValue = QSliderValueTitle("a")
    w.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
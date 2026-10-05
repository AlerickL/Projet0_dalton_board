from __future__ import annotations
#import test_projet_0 as mod
import sys
from PySide6.QtCore import Qt, Signal, Slot, Signal, QPoint
from PySide6.QtWidgets import QWidget, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGroupBox
from PySide6.QtGui import QImage, QPaintDevice, QPainter, QPen, QBrush, QColor, QPixmap

class QGaltonApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Galton Board")
        
        self.__mainLayout:QHBoxLayout = QHBoxLayout()

        self.__QHeightSlider: QSliderWithValueTitle = QSliderWithValueTitle("Height", 100)
        self.__QHeightSlider.setSliderValue(5)
        self.__mainLayout.addWidget(self.__QHeightSlider)

        self.__galtonBoard: QGaltonBoard = QGaltonBoard(self.__QHeightSlider.value())
        self.__mainLayout.addWidget(self.__galtonBoard)

        #Connection des signaux
        self.__QHeightSlider.valueSliderChanged.connect(self.__galtonBoard.setHeight)
        # self.sizechanged.connect(self.__galtonBoard.drawBoard)


        self.setLayout(self.__mainLayout)

class QGaltonBoard(QWidget):
    def __init__(self, height: int, parent=None):
        super().__init__(parent)
        self.__delta_p: int = self.width() // height + 2
        self.__mainLayout:QVBoxLayout = QVBoxLayout()   
        self.__label: QLabel = QLabel()
        
        self.__pegImage: QImage = QImage()
        self.__pixmap: QPixmap = QPixmap(self.__pegImage)
        self.drawBoard()
        
        self.__label.setPixmap(self.__pixmap)

        self.__mainLayout.addWidget(self.__label)
        

        self.setLayout(self.__mainLayout)

    @Slot()
    def drawBoard(self):
        with QPainter(self.__pixmap) as painter:
            pen: QPen = QPen(Qt.GlobalColor.black)
            brush: QBrush = QBrush(Qt.GlobalColor.darkBlue)
            painter.setPen(pen)
            painter.setBrush(brush)
            for j in range(self.height()):
                for i in range(self.height() - j):
                    point: QPoint = QPoint((j + i + 1) * self.__delta_p, (j + 1) * self.__delta_p)
                    painter.drawEllipse(point, self.__delta_p // 4, self.__delta_p // 4)
    @Slot()
    def setHeight(self, height: int) -> None:
        self.__height = height
        self.drawBoard()



class QSliderWithValueTitle(QWidget):
    valueSliderChanged:Signal = Signal(int)
    def __init__(self, title: str, maximum: int=100, parent = None) -> None:
        super().__init__(parent)
        self.__title: QLabel = QLabel(title)
        self.__slider:QSlider = QSlider()
        self.__slider.setOrientation(Qt.Orientation.Horizontal)
        self.__slider.setRange(0,maximum)
        self.__nber:QLabel = QLabel("0")

        layout:QHBoxLayout = QHBoxLayout()
        layout.addWidget(self.__title)
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

    def setSliderValue(self,value:int) -> None:
        self.__slider.setValue(value)




def main() -> None:
    app: QApplication = QApplication(sys.argv)

    w: QGaltonApp = QGaltonApp()
    w.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

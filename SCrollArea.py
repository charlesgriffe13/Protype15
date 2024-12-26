from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 600, 450)
        self._flag = True
        self.lstObject = []
        self.initUI()

    def initUI(self):
        self.scrollArea =  QScrollArea()
        self.widget = QWidget()
        self.vbox = QGridLayout()

        for i in range(0, 50):
            for j in range(0, 4):
                object = QLabel()
                object.setStyleSheet('padding-left: 20px; padding-bottom: 20px')
                self.vbox.addWidget(object, i, j)
                vidcap = cv2.VideoCapture('malinois.mp4')
                vidcap.set(cv2.CAP_PROP_POS_MSEC, 166 * 1000)
                success, image = vidcap.read()
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if success:
                    image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    pixmap01 = QPixmap.fromImage(image)
                    object.setScaledContents(True)
                    x, y = int(self.widget.width() / 6), int(self.widget.width() / 6 * 0.54)
                    object.setPixmap(pixmap01.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.lstObject.append(object)

        self.widget.setLayout(self.vbox)

        #  ScrollArea
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

        self.setCentralWidget(self.scrollArea)

        self.show()

    def resizeEvent(self, e):
        if not self._flag:
            self._flag = True
            # self.setLabel()
            QTimer.singleShot(50, lambda: setattr(self, "_flag", False))
        for itm in self.lstObject:
            itm.setFixedHeight(int(itm.width() * 0.70))
        super().resizeEvent(e)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
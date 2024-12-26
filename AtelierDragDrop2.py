import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 600)

        self.grpTree = QGroupBox(self)
        self.grpTree.setFixedSize(300, 500)
        self.grpTree.setStyleSheet('background-color: gray')
        self.grpTree.move(50, 50)

        source_widget = DraggableWidget(self.grpTree)
        # source_widget.setText('Draggable')
        source_widget.move(50, 50)

        target_Box = DraggableWidget(self.grpTree)
        # source_widget.setText('Target')
        target_Box.move(50, 300)


class DraggableWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(200, 25)
        #
        pixmap = QPixmap('ressources/dossier25.png')
        pixmapLabel = QLabel(self)
        pixmapLabel.setPixmap(pixmap)
        pixmapLabel.move(0, 0)
        #
        textLabel = QLabel(self)
        textLabel.setText('ressources/dossier25.png')
        textLabel.move(30, 0)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        print('e.source().text()')
        e.source().move(10, 100)

    def mousePressEvent(self, e):
        mime_data = QMimeData()
        mime_data.setText('toto')
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.CopyAction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
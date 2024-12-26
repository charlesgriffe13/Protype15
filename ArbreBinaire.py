import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow


class DraggableLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = self.create_mime_data()
        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        drop_action = drag.exec_(Qt.MoveAction)

    def create_mime_data(self):
        mime_data = super().createMimeData()
        mime_data.setText(self.text())
        return mime_data


class TargetLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.setText(text)
        self.setStyleSheet("background-color: lightgreen;")
        event.acceptProposedAction()


class DragAndDropExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop Example')
        self.setGeometry(100, 100, 400, 200)

        draggable_label = DraggableLabel('Drag me', self)
        draggable_label.move(50, 50)

        target_label = TargetLabel('Drop here', self)
        target_label.setGeometry(200, 50, 100, 100)

        self.show()


def main():
    app = QApplication(sys.argv)
    ex = DragAndDropExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

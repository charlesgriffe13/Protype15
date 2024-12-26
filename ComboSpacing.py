import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QStyledItemDelegate

class SpacedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(SpacingDelegate(self))

class SpacingDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spacing = 30  # Ajustez cette valeur selon vos besoins

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + self.spacing)
        return size

class CustomComboBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom ComboBox Example")
        self.setGeometry(100, 100, 300, 150)

        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        self.combo_box = SpacedComboBox()
        self.combo_box.addItem("Item 1")
        self.combo_box.addItem("Item 2")
        self.combo_box.addItem("Item 3")

        layout.addWidget(self.combo_box)
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomComboBoxExample()
    window.show()
    sys.exit(app.exec_())

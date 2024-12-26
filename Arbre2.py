import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Bouton 1"))
        layout.addWidget(QPushButton("Bouton 2"))

        # Supprimer les marges intérieures
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setWindowTitle("Exemple de suppression des marges intérieures")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

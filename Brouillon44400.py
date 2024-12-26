import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDropEvent

class FileDropWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)  # Autoriser le widget à accepter les événements de glisser-déposer
        layout = QVBoxLayout()
        self.label = QLabel("Faites glisser un fichier ici depuis le bureau.")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        # Événement lorsqu'un fichier est glissé sur le widget
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Événement lorsqu'un fichier est déposé sur le widget
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            self.label.setText(f"Fichier glissé et déposé : {file_path}")

class FileDropApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Glisser-Déposer de Fichier")
        self.setGeometry(100, 100, 400, 200)

        central_widget = FileDropWidget()
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDropApp()
    window.show()
    sys.exit(app.exec_())

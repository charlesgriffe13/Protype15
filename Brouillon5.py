import sys
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Création des actions pour les boutons
        action1 = QAction('Bouton 1', self)
        action2 = QAction('Bouton 2', self)
        action3 = QAction('Bouton 3', self)

        # Création de la barre d'outils et ajout des actions
        toolbar = self.addToolBar('Barre d\'outils')
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        toolbar.addAction(action3)

        # Création du widget principal
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        # Création de la zone de défilement
        scroll_area = QScrollArea(main_widget)
        scroll_area.setWidgetResizable(True)

        # Création du contenu à ajouter à la zone de défilement
        content_widget = QWidget(scroll_area)
        content_layout = QVBoxLayout(content_widget)
        for i in range(20):
            button = QPushButton(f'Bouton {i+1}', content_widget)
            content_layout.addWidget(button)

        # Définition du contenu de la zone de défilement
        scroll_area.setWidget(content_widget)

        # Ajout de la zone de défilement au layout principal
        layout.addWidget(scroll_area)

        # Définition du widget principal comme widget central de la fenêtre
        self.setCentralWidget(main_widget)

        # Configuration de la fenêtre
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Exemple de barre d\'outils avec QScrollArea')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

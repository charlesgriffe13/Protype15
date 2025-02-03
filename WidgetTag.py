
import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from AtelierDesign2022 import ParagrapheRecord, VideoFileRecord

class WidgetTag(QDialog):
    def __init__(self, parent, videoPath, videoID, marqueCour, boolCreer):
        super(WidgetTag, self).__init__()
        QDialog.__init__(self)
        self.setGeometry(100, 100, 500, 500)
        self.grpBoxTag = QGroupBox(self)
        #  GroupBox global
        self.grpBoxTag.resize(QSize(400, 400))
        self.grpBoxTag.move(50, 50)
        self.lytTag = QVBoxLayout(self.grpBoxTag)
        #  Zone de saisie du tag
        self.lneTag = QLineEdit()
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.lytTag.addWidget(self.lneTag)
        self.lneTag.keyPressEvent = self.keyPressEvent
        #  Zone d'affichage des tags
        self.grpBoxAffichTag = QGroupBox()
        self.grpBoxAffichTag.setStyleSheet('background-color: orange')
        self.lytTag.addWidget(self.grpBoxAffichTag)
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        #  Ajout de l'ascenseur
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.grpBoxAffichTag)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(200)
        layout = QVBoxLayout(self.grpBoxTag)
        layout.addWidget(self.scroll)

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
            print('enter')
        else:
            aux = self.lneTag.text() + event.text()
            self.lneTag.setText(aux)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aux = 'C:/VideoFinder/Protype/video/Keep It - Preview.mp4'
    win = WidgetTag(app, videoPath=aux, videoID=223, marqueCour=125, boolCreer=True)
    win.show()
    sys.exit(app.exec_())
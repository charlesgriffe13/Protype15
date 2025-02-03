from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class FormCreerNote(QDialog):
    def __init__(self):
        super(FormCreerNote, self).__init__()
        self.setGeometry(100, 100, 672, 673)
        self.setStyleSheet('background-color: gray')
        self.setupUI()

    def setupUI(self):
        lytMain = QVBoxLayout()
        #  Zonne du haut
        lytTop = QHBoxLayout()
        label = QLabel("Saisie d'une nouvelle note")
        lytTop.addWidget(label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytTop.addItem(spacerItem)
        lblTimeCode = QLabel('../../..')
        lytTop.addWidget(lblTimeCode)
        #  Zone du tabWidget
        lytTabWidget = QVBoxLayout()
        tabWidgetNote = QTabWidget()
        tabWidgetNote.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lytTabWidget.addWidget(tabWidgetNote)
        #
        # Tab 1
        #
        tabTitre = QWidget()
        tabWidgetNote.addTab(tabTitre, 'Titre')
        lytTitre = QVBoxLayout(tabTitre)
        tedTitre = QTextEdit()
        lytTitre.addWidget(tedTitre)
        tedTitre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tedTitre.setStyleSheet('background-color: orange')
        lytTitreBtn = QHBoxLayout()
        btnSauverTitre = QPushButton('Sauver le titre')
        lytTitreBtn.addWidget(btnSauverTitre)
        btnEffacerTitre = QPushButton('Effacer le titre')
        lytTitreBtn.addWidget(btnEffacerTitre)
        btnTagTitre = QPushButton('Tag (Ctrl+T')
        lytTitreBtn.addWidget(btnTagTitre)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytTitreBtn.addItem(spacerItem1)
        btnFermer0 = QPushButton('Fermer')
        lytTitreBtn.addWidget(btnFermer0)
        #
        # Tab 2
        #
        tabImage = QWidget()
        tabWidgetNote.addTab(tabImage, 'Image')
        lytImage = QVBoxLayout(tabImage)
        lblImage = QLabel()
        lblImage.setStyleSheet('background-color: green')
        lytImage.addWidget(lblImage)
        lneLegende = QLineEdit()
        lneLegende.setText('ceci est un exemple')
        lytImage.addWidget(lneLegende)
        lytImageBtn = QHBoxLayout()
        btnSauverImage = QPushButton("Sauver l'image")
        lytImageBtn.addWidget(btnSauverImage)
        btnEffacerImage = QPushButton("Effacer l'image")
        lytImageBtn.addWidget(btnEffacerImage)
        btnTagImage = QPushButton("'Tag (Ctrl+T'")
        lytImageBtn.addWidget(btnTagImage)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytImageBtn.addItem(spacerItem2)
        btnFermer1 = QPushButton('Fermer')
        lytImageBtn.addWidget(btnFermer1)
        #
        # Tab 3
        #
        tabTexte = QWidget()
        tabWidgetNote.addTab(tabTexte, 'Note')
        lytTexte = QVBoxLayout(tabTexte)
        tedTexte = QTextEdit()
        tedTexte.setStyleSheet('background-color: pink')
        lytTexte.addWidget(tedTexte)
        lyttexteBtn = QHBoxLayout()
        btnSauverTexte = QPushButton('Sauver la note')
        lyttexteBtn.addWidget(btnSauverTexte)
        btnEffacererTexte = QPushButton('Effacer la note')
        lyttexteBtn.addWidget(btnEffacererTexte)
        btnTagTexte = QPushButton("'Tag (Ctrl+T'")
        lyttexteBtn.addWidget(btnTagTexte)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lyttexteBtn.addItem(spacerItem3)
        btnFermer2 = QPushButton('Fermer')
        lyttexteBtn.addWidget(btnFermer2)

        lytMain.addLayout(lytTop)
        lytMain.addLayout(lytTabWidget)
        lytMain.addLayout(lytTitre)
        lytTitre.addLayout(lytTitreBtn)
        lytMain.addLayout(lytImage)
        lytImage.addLayout(lytImageBtn)
        lytMain.addLayout(lytTexte)
        lytTexte.addLayout(lyttexteBtn)
        self.setLayout(lytMain)


if __name__ == '__main__':
    # don't auto scale.
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)


    formCreerNote = FormCreerNote()
    formCreerNote.show()



    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
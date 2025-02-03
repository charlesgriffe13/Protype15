import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Win(QDialog):
    def __init__(self):
        super(Win, self).__init__()
        self.setGeometry(100, 100, 400, 400)
        self.listLien = []

        lyt = QVBoxLayout()

        self.btnTexte = QPushButton(self)
        self.btnTexte.setText('Mode HTML')
        self.btnTexte.clicked.connect(self.modeTexte)
        lyt.addWidget(self.btnTexte)

        self.textEdit = QTextBrowser()
        self.textEdit.setFont(QFont('Arial', 12))
        aux = 'Ceci est un exemple de lien vers un site internet.'
        self.textEdit.setText(aux)
        lyt.addWidget(self.textEdit)
        self.textEdit.setReadOnly(False)
        self.setLayout(lyt)

        self.shortcutTest = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcutTest.activated.connect(self.creerLien)

        self.shortcutTest = QShortcut(QKeySequence('Ctrl+T'), self)
        self.shortcutTest.activated.connect(self.populateLien)
        self.populateLien()

    def modeTexte(self):
        if self.btnTexte.text() == 'Mode HTML':
            self.textEdit.setReadOnly(True)
            self.btnTexte.setText('Mode texte')
        else:
            self.textEdit.setReadOnly(False)
            self.btnTexte.setText('Mode HTML')

    def creerLien(self):
        self.textEdit.setReadOnly(True)
        cursor = self.textEdit.textCursor()
        lien = cursor.selectedText()
        text, ok = QInputDialog.getText(self, 'Insérer une page Web', "Saisir l'URL")
        if ok:
            self.listLien.append((lien, text))
        else:
            return

        auxText = self.textEdit.toPlainText()

        for tpl in self.listLien:
            mot, url = tpl
            auxHTML = f'<a href="{url}" target="_blank">{mot}</a>'
            auxText = auxText.replace(mot, auxHTML)
        self.textEdit.setText(auxText)
        self.textEdit.setOpenExternalLinks(True)

        # url = "https://meteofrance.re/fr"
        # url = "https://www.google.com/maps
        self.btnTexte.setText('Mode texte')

    def populateLien(self):
        print('ok')
        self.textEdit.setReadOnly(True)
        # cursor = self.tedTexte.textCursor()
        # lien = cursor.selectedText()
        auxText = self.textEdit.toPlainText()

        self.listLien = [('exemple', 'https://meteofrance.re/fr'), ('site', 'https://www.google.com/maps')]

        for tpl in self.listLien:
            mot, url = tpl
            auxHTML = f'<a href="{url}" target="_blank">{mot}</a>'
            auxText = auxText.replace(mot, auxHTML)
        self.textEdit.setText(auxText)
        self.textEdit.setOpenExternalLinks(True)
        self.btnTexte.setText('Mode texte')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
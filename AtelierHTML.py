import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCharFormat, QColor, QTextDocument
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet('background: orange')

        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('c:/videoFinder/Atelier_Constructor/data/VideoLearnerX.db')
        db.setDatabaseName('data/dataTest.db')
        if db.open():
            # Remplacer les notes (Null) par 0
            # query = QSqlQuery()
            # query.exec('UPDATE videoFileTab SET note = 0 WHERE note IS NULL')
            pass

        #  Barre de boutons
        barTool = QGroupBox(self)
        barTool.setFixedSize(500, 50)
        barTool.setStyleSheet('background: white')
        barTool.move(50, 10)

        #  QTexedit
        self.ted = QTextEdit(self)
        self.ted.setFixedSize(500, 250)
        self.ted.setStyleSheet('background: white')
        self.ted.move(50, 70)
        aux = """Des averses faibles arrivent parfois à la côte sur la partie orientale de l'île et au pied du volcan. Ailleurs le temps est calme. Le ciel est très nuageux entre l'Anse des cascades et St-Philippe avec parfois de petites pluies.
        
Les températures sont fraîches dans l'intérieur, elles sont proches de la normale sur la côte.

Le vent est faible et la mer est localement agitée dans le sud."""
        self.ted.setText(aux)
        self.ted.viewport().installEventFilter(self)

        #  QLabel
        self.lbl = QTextEdit(self)
        self.lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.lbl.setFixedSize(500, 100)
        self.lbl.setStyleSheet('background: white')
        self.lbl.viewport().installEventFilter(self)
        self.lbl.move(50, 330)
        self.lbl.textChanged.connect(self.documentChange)

        # btnForme
        self.btnForme = QPushButton(barTool)
        self.btnForme.setText('Forme')
        self.btnForme.move(10, 10)
        self.btnForme.clicked.connect(self.evt_btnForme_clicked)

        # btnLien
        self.btnLien = QPushButton(barTool)
        self.btnLien.setText('Transfert')
        self.btnLien.move(120, 10)
        self.btnLien.clicked.connect(self.evt_btnLien_clicked)

        # btnSauve
        self.btnSauve = QPushButton(barTool)
        self.btnSauve.setText('Sauve')
        self.btnSauve.move(230, 10)
        self.btnSauve.clicked.connect(self.evt_btnSauve_clicked)

        # btnCharge
        self.btnCharge = QPushButton(barTool)
        self.btnCharge.setText('Charge')
        self.btnCharge.move(340, 10)
        self.btnCharge.clicked.connect(self.evt_btnCharge_clicked)

    def evt_btnForme_clicked(self):
        cursor = self.ted.textCursor()
        selected_text = cursor.selectedText()
        format = QTextCharFormat()
        format.setFontWeight(QFont.Bold)
        format.setFontUnderline(True)
        cursor.mergeCharFormat(format)
        self.ted.mergeCurrentCharFormat(format)

    def evt_btnLien_clicked(self):
        self.lbl.setText(self.ted.toHtml())

    def evt_btnSauve_clicked(self):
        aux = self.ted.toHtml()
        aux = aux.replace("'", "²")
        aux = aux.replace("\n", "<br>")
        aux = aux.replace("\t", "&#09")
        tplChamps = ('note', 'cle')
        tplData = (aux, 1)
        query3 = QSqlQuery()
        bOK3 = query3.exec(f'INSERT INTO tabNote {tplChamps} VALUES {tplData}')

    def evt_btnCharge_clicked(self):
        query = QSqlQuery()
        query.exec('SELECT * FROM tabNote WHERE cle = 1')
        if query.next():
            aux = query.value('note')
        aux = aux.replace("²", "'")
        aux = aux.replace('<br>', '')
        aux = aux.replace("&#09", "\t")
        self.lbl.setText(aux)

    def documentChange(self):
        documentSize = self.lbl.document().size()
        print(documentSize.height())
        self.lbl.setFixedHeight(int(documentSize.height() + 10))
        # self.lbl.resize(500, documentSize.height())

    def eventFilter(self, source, event):
        if source is self.ted.viewport() and event.type() == event.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                cursor = self.ted.cursorForPosition(event.pos())
                self.ted.setTextCursor(cursor)
                cursor = self.ted.textCursor()
                format = cursor.charFormat()
                if format.fontWeight() == QFont.Bold:
                    QDesktopServices.openUrl(QUrl('www.google.com'))
                else:
                    pass
        if source is self.lbl.viewport() and event.type() == event.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                cursor = self.lbl.cursorForPosition(event.pos())
                self.lbl.setTextCursor(cursor)
                cursor = self.lbl.textCursor()
                format = cursor.charFormat()
                if format.fontWeight() == QFont.Bold:
                    QDesktopServices.openUrl(QUrl('www.google.com'))
                else:
                    pass
        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

from AtelierDesign2022 import ParagrapheRecord, NotePicture


from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from FormSaisie_UI import Ui_DlgSaisieParagraph as dialogSaisie
from FormSaisieCréer_UI import Ui_DlgSaisieParagraph as dialogCreer
# from formCreerNote1_UI import Ui_Dialog as dialogCreer
from formCreerNote import FormCreerNote
from formClasseur_UI import Ui_Dialog as dialogClasseur
from formParametres_UI import Ui_DialogParameters as DialogParameters
from PyQt5.QtMultimediaWidgets import QVideoWidget
from formListVideo1_UI import Ui_DialogListVideo
from Paragraph_UI import Ui_mainParagraph
from frmBiblio_UI import Ui_mainWindowBiblio as DialogBiblio
from frmStatut_UI import Ui_mainWindowStatut as DialogStatut
import datetime
from datetime import datetime
import time
import os
from functools import partial
from unicodedata import normalize, combining
from MetaDataMP4 import GrpBoxMetaData11
import exiftool
import subprocess
import html

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        A T E L I E R   P A R A G R A P H           **************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class AtelierParagraph(QMainWindow):
    def __init__(self, videoID):
        super().__init__()
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet('background: #111111')
        self.videoID = videoID
        self.setWindowTitle('Module Paragraph')


        # db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('data/videoLearnerX.db')
        # if db.open():
        #     print('dataBase Open')

        # **********************************
        #  QScrollArea
        # **********************************
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        scroll_area.setStyleSheet(styleQScrollBar)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # *******************************************************************************************

        # Recherche des timeCodes de la video 263
        self.listTimeNote = []
        query = QSqlQuery()
        query.exec(f'SELECT DISTINCT timeNote FROM paragraph WHERE cleVideo = {self.videoID} ORDER BY timenote')
        while query.next():
            self.listTimeNote.append(query.value('timeNote'))

        self.listNote = []
        self.listWidget = []
        self.listTed = []
        self.listTimeCodeNote = []
        self.top = 20
        for timeNote in self.listTimeNote:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM paragraph WHERE timeNote={timeNote} AND cleVideo={self.videoID}')
            # while query.next():
            #     self.listNote.append(query.value('cle'))
            titreAux = None
            imageAux = None
            texteAux = None
            boolModif = True
            while query.next():
                aux = ParagrapheRecord(query.value('cle'))
                if aux.titre:
                    titreAux = aux
                if aux.picture:
                    imageAux = aux
                if aux.note:
                    texteAux = aux
            # ***************************
            # ****  T I T R E  **********
            if titreAux != None and timeNote == 0:  # Titre général
                # GroupBox pour les boutons modif et play
                grpBouton = QGroupBox(self)
                grpBouton.setFixedSize(500, 50)
                grpBouton.setStyleSheet('border: 0px')
                layout.addWidget(grpBouton)
                self.icon = QIcon('ressources/modif.png')
                # aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModif = QPushButton(grpBouton)
                self.btnModif.setIcon(self.icon)
                self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                            'border-style: solid; border-color: gray; border-width: 0px;'
                                            'background-color: #201F1F')
                self.btnModif.setFixedSize(25, 25)
                self.btnModif.move(5, 5)
                self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                #
                self.icon = QIcon('ressources/playNote.png')
                self.btnPlayNote = QPushButton(grpBouton)
                self.btnPlayNote.setIcon(self.icon)
                self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                               'border-style: solid; border-color: gray; border-width: 0px;'
                                               'background-color: #201F1F')
                self.btnPlayNote.setFixedSize(25, 25)
                self.btnPlayNote.move(35, 5)
                # QTextEdit
                font = QFont()
                font.setFamily('Arial')
                font.setPointSize(16)
                font.setBold(True)
                tedNote = QTextEdit(self)
                tedNote.setText(titreAux.texte)
                tedNote.setFont(font)
                tedNote.viewport().installEventFilter(self)
                tedNote.setAlignment(Qt.AlignCenter | Qt.AlignTop)
                tedNote.setFixedSize(500, 100)
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                # tedNote.move(50, int(self.top))
                layout.addWidget(tedNote)
                self.listWidget.append(tedNote)
                boolModif = False
                # **************************
                # **** PARAGRAPH   *********
                if titreAux != None and timeNote > 0:  # Titre général
                    # GroupBox pour les boutons modif et play
                    grpBouton = QGroupBox(self)
                    grpBouton.setFixedSize(500, 50)
                    grpBouton.setStyleSheet('border: 0px')
                    layout.addWidget(grpBouton)
                    self.icon = QIcon('ressources/modif.png')
                    # aux = strTime(self.paragraphCour.timeNote)
                    aux = ''
                    self.btnModif = QPushButton(grpBouton)
                    self.btnModif.setIcon(self.icon)
                    self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                'border-style: solid; border-color: gray; border-width: 0px;'
                                                'background-color: #201F1F')
                    self.btnModif.setFixedSize(25, 25)
                    self.btnModif.move(5, 5)
                    self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                    #
                    self.icon = QIcon('ressources/playNote.png')
                    self.btnPlayNote = QPushButton(grpBouton)
                    self.btnPlayNote.setIcon(self.icon)
                    self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                   'border-style: solid; border-color: gray; border-width: 0px;'
                                                   'background-color: #201F1F')
                    self.btnPlayNote.setFixedSize(25, 25)
                    self.btnPlayNote.move(35, 5)
                    # QTextEdit
                    font = QFont()
                    font.setFamily('Arial')
                    font.setPointSize(16)
                    font.setBold(True)
                    tedNote = QTextEdit(self)
                    tedNote.setText(titreAux.texte)
                    tedNote.setFont(font)
                    tedNote.viewport().installEventFilter(self)
                    tedNote.setAlignment(Qt.AlignCenter | Qt.AlignTop)
                    tedNote.setFixedSize(500, 100)
                    tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                    # tedNote.move(50, int(self.top))
                    layout.addWidget(tedNote)
                    self.listWidget.append(tedNote)
                    boolModif = False
            # **************************
            # ****  I M A G E  *********
            if imageAux != None:
                query1 =QSqlQuery()
                query1.exec(f'SELECT * FROM videoFileTab WHERE cle={self.videoID}')
                if query1.next():
                    cleBiblio = query1.value('cleBiblio')
                    internalPath = query1.value('internalPath')
                    videoName = query1.value('videoName')
                query2 = QSqlQuery()
                query2.exec(f'SELECT path FROM biblioTab WHERE cle={cleBiblio}')
                if query2.next():
                    pathBiblio = query2.value('path')
                videoPath = pathBiblio + internalPath + videoName
                notePicture = NotePicture(self, timeNote=imageAux.timeNote, picture=imageAux.picture,
                                          texte=imageAux.texte, cle=imageAux.cle, videoPath=videoPath,
                                          videoID=self.videoID, icone=imageAux.icone, indentation=imageAux.indentation,
                                          boolModif=boolModif)
                layout.addWidget(notePicture)
                self.listWidget.append(notePicture)
                boolModif = False
            # **************************
            # ****   N O T E   *********
            if texteAux != None:
                self.listLien = []
                query = QSqlQuery()
                query.exec(f'SELECT * FROM linkTab WHERE cleVideo={self.videoID}')
                while query.next():
                    aux = (query.value('timeCode'), query.value('URL'), query.value('mot'))
                    self.listLien.append(aux)
                # GroupBox pour les boutons modif et playboo
                if boolModif:
                    grpBouton = QGroupBox(self)
                    grpBouton.setFixedSize(500, 50)
                    grpBouton.setStyleSheet('background: #111111; border: 0px')
                    layout.addWidget(grpBouton)
                    self.btnModif = QPushButton(grpBouton)
                    self.icon = QIcon('ressources/modif.png')
                    self.btnModif.setIcon(self.icon)
                    self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                'border-style: solid; border-color: gray; border-width: 0px;'
                                                'background-color: #201F1F')
                    self.btnModif.setFixedSize(25, 25)
                    self.btnModif.move(5, 5)
                    self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                    #
                    self.icon = QIcon('ressources/playNote.png')
                    self.btnPlayNote = QPushButton(grpBouton)
                    self.btnPlayNote.setIcon(self.icon)
                    self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                   'border-style: solid; border-color: gray; border-width: 0px;'
                                                   'background-color: #201F1F')
                    self.btnPlayNote.setFixedSize(25, 25)
                    self.btnPlayNote.move(35, 5)
                # QTextEdit
                tedNote = QTextEdit(self)
                tedNote.viewport().installEventFilter(self)
                tedNote.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                tedNote.setFixedSize(500, 100)
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                layout.addWidget(tedNote)
                self.listWidget.append(tedNote)
                self.listNote.append(tedNote)
                query = QSqlQuery()
                query.exec(f'SELECT * FROM paragraph WHERE timeNote={timeNote} AND cleVideo={self.videoID} AND  note')
                if query.next():
                    aux = query.value('texte')
                    aux = aux.replace("²", "'")
                    aux = aux.replace('<br>', '')
                    aux = aux.replace("&#09", "\t")
                tedNote.setText(aux)
                documentSize = tedNote.document().size()
                tedNote.setFixedHeight(int(documentSize.height() + 10))
                self.top += documentSize.height() + 20
                boolModif = False
                self.tedNote = tedNote
                self.listTed.append(tedNote)
                self.listTimeCodeNote.append(timeNote)

        # # *******************************************************************************************
        spacerItem = QSpacerItem(40, 200, QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addItem(spacerItem)
        scroll_area.setWidget(widget)
        self.setCentralWidget(scroll_area)

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            i = 0
            index = 0
            textEdit = None
            for itm in self.listTed:
                if source == itm.viewport():
                    index = i
                else:
                    i += 1

            cursor = self.listTed[index].cursorForPosition(event.pos())
            cursor.select(QTextCursor.WordUnderCursor)
            selected_text = cursor.selectedText()
            # print(selected_text)
            format = cursor.charFormat()
            # liste des liens du timeCode
            listAux = [(mot, URL) for (timeCode, mot, URL) in self.listLien if timeCode==self.listTimeCodeNote[index]]
            # print(listAux)
            if format.fontWeight() == QFont.Bold and format.fontUnderline():
                for tpl in listAux:
                    URL, lien = tpl
                    if selected_text in lien:
                        QDesktopServices.openUrl(QUrl(URL))
            else:
                pass
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ObjNote1(226)
    win.show()
    sys.exit(app.exec_())
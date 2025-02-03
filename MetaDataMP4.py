import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
# from AtelierDesign2022 import *
# from PyQt5.QtWebEngineWidgets import *

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
import exiftool
import subprocess

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             G R P B O X M E T A D A T A 1 1      ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GrpBoxMetaData11(QGroupBox):
    def __init__(self, parent, videoID, lytMain):
        super().__init__()
        self.setStyleSheet('background-color: gray')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumHeight(240)
        self.parent = parent
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False
        self.indexCour = -1
        self.setStyleSheet('margin: 0px')
        self.lneTag = QLineEdit(self)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.lneTag.setStyleSheet('margin: 0px')
        self.lneTag.setFixedWidth(600)  # 640
        lytMain.addWidget(self.lneTag)
        self.listTag = []

        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))

        self.grpBoxAffichTag = QGroupBox()
        self.grpBoxAffichTag.setStyleSheet('border: 0px')
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        self.grpBoxAffichTag.setFixedWidth(590)  # 590

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(self.grpBoxAffichTag)
        scroll.setWidgetResizable(True)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        self.populateGrpBoxAffichTag()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            menu = QMenu(self)
            menu.addAction('Effacer', self.effaceTag)
            menu.addSeparator()
            menu.addAction('Modifier', self.modifTag)
            self.motCour = source.text()
            if menu.exec_(event.globalPos()):
                return True
        return super().eventFilter(source, event)

    def effaceTag(self):
        del self.listTag[self.listTag.index(self.motCour)]
        self.boolModif = False
        self.majMetaData()

    def modifTag(self):
        self.lneTag.setText(self.motCour)
        self.boolModif = True
        self.indexCour = self.listTag.index(self.motCour)

    def majMetaData(self):
        aux = ''
        for tag in self.listTag:
            aux += tag + ','
        aux = aux[:-1]

        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            video = mainWindow.racine + query.value('internalPath') + query.value('VideoName')

        with exiftool.ExifTool("exiftool.exe") as et:
            et.execute(f'-Comment={aux}', video)
        self.populateGrpBoxAffichTag()

    def sauverTag(self):
        mot = self.lneTag.text()

        if mot in self.listTag and not self.boolModif:
            QMessageBox.information(self, 'Enregistrement annulé', 'Le tag existe déja pour cette vidéo.')
            return
        if self.boolModif:
            self.listTag[self.indexCour] = mot
        else:
            self.listTag.append(mot)
        self.boolModif = False
        self.indexCour = -1
        self.majMetaData()
        # self.populateGrpBoxAffichTag()

    def populateGrpBoxAffichTag(self):
        # Effacer le contenu de lytAffichTag
        while 1:
            child = self.lytAffichTag.takeAt(0)
            if not child:
                break
            try:
                child.widget().deleteLater()
            except:
                pass
        self.listTag = []
        #  Mise à jour de la listTag
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            video = mainWindow.racine + query.value('internalPath') + query.value('VideoName')
        #  Récupération detoutes les rubriques dans le métaData
        exe = "exiftool.exe"
        process = subprocess.Popen([exe, video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True)
        metaDict = {}
        try:
            for e in process.stdout:
                line = e.strip().split(':')
                x = line[0].strip()
                y = line[1]
                metaDict[x] = y
                # print(f'{x}: {y}')
        except:
            return
        #  Récupération des tags dans la rubrique Comment du MétaData
        try:
            self.listTag = metaDict.get('Comment').lstrip().split(',')
        except:
            self.listTag = []

        if len(self.listTag) == 0:
            return
        i = 0
        continuerLigne = True
        largLigneTag = 0
        largeur = 320
        offSet = 8
        lenList = len(self.listTag)
        grpBox = QGroupBox()
        grpBox.setFixedHeight(35)
        grpBox.setStyleSheet('border: 0px')
        lyt = QHBoxLayout()
        grpBox.setLayout(lyt)
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(self.listTag[i], '#55aa7f')
                lblTag.installEventFilter(self)
                largLigneTag += lblTag.width  # + offSet
                lyt.addWidget(lblTag)
                if i + 1 == lenList:
                    self.lytAffichTag.addWidget(grpBox)
                    continuerLigne = False
                    continuerColonne = False
                    spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
                    lyt.addItem(spacerItem)
                else:
                    if largLigneTag > largeur:
                        largLigneTag = 0
                        lblTag.close()
                        i -= 1
                        self.lytAffichTag.addWidget(grpBox)
                        grpBox = QGroupBox()
                        grpBox.setStyleSheet('border: 0px')
                        grpBox.setFixedHeight(35)
                        lyt = QHBoxLayout()
                        grpBox.setLayout(lyt)
                        continuerColonne = False
                i += 1
        spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lytAffichTag.addItem(spacerItem)
        self.lneTag.setText('')

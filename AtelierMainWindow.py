import AtelierClassCommun

import AtelierGridWindow

# AtelierGridWindow.py
# AtelierMainParagraph.py
# AtelierGlobal.py
# AtelierMainWindow.py ----> Main
# AtelierClassCommun.py
# AtelierDragDrop1.py

import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# from PyQt5.QtWebEngineWidgets import *
from AtelierClassCommun import MainWindowCustom, DialogCustom, VideoFileRecord, LabelIndex, BoutonOffOn, \
    ParagrapheRecord, BoutonIndex,FormBlockNote, PastilleSimple, MainWindowDossier

from PyQt5.QtSql import QSqlDatabase
# from AtelierTabObjectScreen import TabObjectScreen
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
from AtelierGridWindow import GridWindow, FormSavedSearch, FormEditionVideo

from functools import partial
from unicodedata import normalize, combining
from MetaDataMP4 import GrpBoxMetaData11
import exiftool
import subprocess
import html

global toto


# *********************************************************************************************************************
# ***************            M A I N W I N D O W            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        toto = 42
        #
        self.setGeometry(100, 60, 1326, 780)
        self.cadreGridVignette = CadreGridVignette()
      
        self.cleBiblio = None
        self.boolSearch = False
        self.searchString = ''
        self.boolModifExecuterSearch = False

        statusBar = QStatusBar(self)
        self.setStatusBar(statusBar)
        f = open('styles/statuBar.txt', 'r')
        style = f.read()
        styleQStatusBar = style
        statusBar.setStyleSheet(styleQStatusBar)

        # global lstIndiceChampTab

        self.lstIndiceChampTab = ["videoFileTab", "videoFileTab", "videoFileTab", "tagTab", "videoFileTab",
                                  'videoFileTab', "videoFileTab", "videoFileTab", "videoFileTab", "Paragraph"]

        lblVersion = QLabel('Version : 13.00')
        lblVersion.setStyleSheet('padding-left: 10px')
        statusBar.addWidget(lblVersion)
        global fileAttenteVideo
        fileAttenteVideo = [(-1, -1)]
        self.btnGroupCour = -1

        self.lstGridVideo = []
        self.lstVideo = []
        self.URLCour = None
        self.nbTab = 0

        self.filtreCour = None
        self.NbVideosRecentes = 5
        self.cmbSortIndex = 0
        self.nbColonnes = 4

        self.dossierSelectCour = -1  # cle du dossier à afficher dans le GridVideo
        self.leftTopSelectCour = -1  # 1->AllItems  -  2->Recents  -  3->Favoris  -  4->deleted

        f = open('styles/QMainWindow.txt', 'r')
        style = f.read()
        styleQMainWindow = style
        self.setStyleSheet(styleQMainWindow)
        self.setStyleSheet("background-color: #222222")

        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/VideoLearnerX.db')

        # Intructions obligatoires sinon la base de données ne fonctionne pas
        if db.open():
            # Obtenir la liste des tables dans la base de données
            tables = db.tables()
            # Afficher la liste des tables
            for table in tables:
                pass

        #  Initialisation du nombre de colonnes de la GridVignette
        self.lngCourGlobal = ''
        query = QSqlQuery()
        query.exec(f'SELECT nbColonnes FROM parametersTab WHERE cle=1')
        if query.next():
            self.nbColonnes = query.value('nbColonnes')
        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'
        #  Remettre le flagCouper à False dans la table ParametersTab
        query = QSqlQuery()
        tplChamps = ('flagCut', 'videoPaste')
        tplData = (False, -1)
        bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')

        listeX = []
        query = QSqlQuery()
        query.exec('SELECT * FROM biblioTreeTab')
        while query.next():
            listeX.append(query.value('data'))

        #  ***********************************************
        #  Cas de la première utilisation
        #  Intégrer la vidéo (dans un premier temps un tuto sur GitHub puis, à terme
        #  il y aura une vidéo de présentation de VideoFinder avec l'enrichissement déja
        #  dans la table Paragraph)
        # #  ***********************************************
        # query = QSqlQuery()
        # query.exec('SELECT * FROM videoFileTab')
        # if not query.next(): #  Pas de vidéo saisie dans la base
            #  Récupérer la vidéo de présentation
     


        #  ***********************************************
        #  Mise en place du menu principal
        #  ***********************************************
        f = open('styles/StyleBaseMenu.txt', 'r')
        # f = open('styles/QMenuBar.txt', 'r')
        style = f.read()
        styleBarMenu = style

        barMenu = self.menuBar()
        barMenu.setStyleSheet(styleBarMenu)
        barMenu.setFont(QFont('Arial', 10))
        #
        menuPreferences = barMenu.addMenu(self._trad("Préférences", self.lngCourGlobal))

        menuItemAbout = QAction(QIcon('ressources/about.png'),
                                self._trad("A propos de VidéoFinder", self.lngCourGlobal), self)
        # menuItemAbout = QAction(QIcon(None), self._trad("About VideoFinder", self.lngCourGlobal), self)
        menuItemAbout.setStatusTip(self._trad("A propos de VidéoFinder", self.lngCourGlobal))
        menuItemAbout.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuPreferences.addAction(menuItemAbout)

        menuItemPreferences = QAction(QIcon('ressources/library.png'),
                                      self._trad("Préférences", self.lngCourGlobal), self)
        menuItemPreferences.setStatusTip(self._trad("Préférences", self.lngCourGlobal))
        menuItemPreferences.triggered.connect(self.evt_actPreferences_clicked)
        menuPreferences.addAction(menuItemPreferences)

        self.insertSelectZoneGauche()
        self.insertSelectZoneDroit()
        self.stackedWidget.addWidget(self.cadreGridVignette)
        self.stackedWidget.setCurrentWidget(self.cadreGridVignette)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def editVideo(self, cle):
        formEditionVideo = FormEditionVideo(cle)
        formEditionVideo.show()

    def insertSelectZoneGauche(self):
        #  Sélection All items, Récents, etc
        self.selectZoneGauche = SelectZoneGauche(self)
        self.cadreGridVignette.lytLeft.addWidget(self.selectZoneGauche)
        #  Module de gestion des dossiers
        self.mainWindowDossier = MainWindowDossier(self)
        self.cadreGridVignette.lytLeft.addWidget(self.mainWindowDossier)

        # Widget pour forcer le widget suivant en haut
        spacer = QWidget()
        spacer.setStyleSheet('background-color: orange')
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def insertSelectZoneDroit(self):
        self.selectZoneDroit = SelectZoneDroit(self)
        self.cadreGridVignette.lytRight.addWidget(self.selectZoneDroit)

    def evt_actPreferences_clicked(self):
        try:
            self.gridWindow.formEditionVideo.close()
        except:
            pass
        self.formPreferencesVideo = FormPreferencesVideo(self)
        self.formPreferencesVideo.show()

    def evt_actAddVideo_clicked(self):
        # self._trad("Préférences", self.lngCourGlobal)

        file, b = QFileDialog.getOpenFileName(self, self._trad("Enregistrer une nouvelle vidéo", self.lngCourGlobal),
                                              self.racine, '*.mp4')
        lenBiblio = len(self.racine)
        fullPath = file[:lenBiblio]
        if fullPath != self.racine:
            QMessageBox.information(self, 'Problème de bibliothèque', 'La vidéo doit appartenir au répertoire '
                                                                      'de la bibliothèque')
            return
        internalPathAux = file[lenBiblio:].split('/')
        l = len(internalPathAux) - 2
        internalPath = ''
        if l > -1:
            for x in range(0, l + 1):
                internalPath += internalPathAux[x] + '/'
        if file:
            query = QSqlQuery()
            bOK = query.exec(f'SELECT * FROM videoFileTab WHERE videoFullPath = {file}')
            if bOK:  # Vidéo déja enregistrée
                rep = QMessageBox.information(self, 'Vidéo déjà enregistrée', 'La vidéo a déjà été enregistrée '
                                                                              'dans la base de données.')

    def displayGridWindow(self, lstVideo):
        self.gridWindow = GridWindow(self, lstVideo)

    def displayTabWindow(self, lstVideo):
        lstVideoOnglet = lstVideo
        self.tabObjetScreen = TabObjectScreen(self, lstVideoOnglet)
        self.stackedWidget.addWidget(self.tabObjetScreen)
        self.stackedWidget.setCurrentWidget(self.tabObjetScreen)

    def evt_btnPlusTab_clicked(self):
        #  vider la video chargée dans mediaPlayer et sauver la date de lecture et la position de la lecture en cours
        d = datetime.now().strftime('%Y-%m-%d')
        for pushOnglet in self.tabObjetScreen.barOnglet.lstOnglet:
            cleVideo = pushOnglet.cleVideo
            query = QSqlQuery()
            tplChamps = ('marquePage', 'DateLastView')
            tplData = (int(formScreen1.mediaPlayer.position() // 1000), d)
            bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle = {cleVideo}')
        formScreen1.mediaPlayer.setMedia(QMediaContent(None))

        self.setCursor(Qt.WaitCursor)
        self.stackedWidget.setCurrentWidget(self.cadreGridVignette)
        self.unsetCursor()


    def removeTab(self, cleVideo):
        i = 0
        ongletCour = 0
        for onglet in self.tabObjetScreen.barOnglet.lstOnglet:
            if onglet.cleVideo == cleVideo:
                ongletCour = i
            i += 1
        #  supprimer l'onglet concerné
        self.tabObjetScreen.barOnglet.lstOnglet[ongletCour].close()
        #  Vider les mediaPlayer des vidéos chargées
        formScreen1.mediaPlayer.setMedia(QMediaContent(None))

        del self.tabObjetScreen.barOnglet.lstOnglet[ongletCour]
        if len(self.tabObjetScreen.barOnglet.lstOnglet) != 0:
            cleVideo = self.tabObjetScreen.barOnglet.lstOnglet[0].cleVideo
            self.tabObjetScreen.barOnglet.majCurrentOnglet(cleVideo)
        else:
            self.stackedWidget.setCurrentWidget(self.cadreGridVignette)
        #  Repositionner les onglets
        i = 0
        for onglet in self.tabObjetScreen.barOnglet.lstOnglet:
            onglet.move(136*i + 10, 10)
            i += 1
        self.tabObjetScreen.barOnglet.btnPlus.move(136*i + 10, 15)

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        strHeure, strMinute, strSeconde = '', '', ''
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        A T E L I E R   P A R A G R A P H           **************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class AtelierParagraph(QMainWindow):
    def __init__(self, parent, videoID):
        super().__init__()
        self.parent = parent
        # self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet('background: #111111')
        self.videoID = videoID

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.setWindowTitle(self._trad('Module Paragraph', self.lngCourGlobal))
        # ***********************************
        self.chkImage = True
        self.chkNote = True
        self.chkTitre = True
        # **********************************
        #  QScrollArea
        # **********************************
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        self.scroll_area.setStyleSheet(styleQScrollBar)
        self.widget = QWidget()
        self.widget.setStyleSheet('background: #111111')
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.populateParagraph(self.videoID)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def initChkNote(self, chkImage, chkNote, chkTitre):
        self.chkImage = chkImage
        self.chkNote = chkNote
        self.chkTitre = chkTitre

    def populateParagraph(self, cleVideo):
        self.effacer()
        # Recherche des timeCodes de la video
        self.listTimeNote = []
        query = QSqlQuery()
        query.exec(f'SELECT DISTINCT timeNote FROM paragraph WHERE cleVideo = {cleVideo} ORDER BY timenote')
        while query.next():
            aux = query.value('timeNote')
            self.listTimeNote.append(aux)

        self.listNote = []
        self.listWidget = []
        self.listTed = []
        self.listTimeCodeNote = []
        self.top = 20
        self.timeNoteCour = 0
        for timeNote in self.listTimeNote:
            self.timeNoteCour = timeNote
            query = QSqlQuery()
            query.exec(f'SELECT * FROM paragraph WHERE timeNote={timeNote} AND cleVideo={cleVideo}')

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
                grpBouton.setFixedSize(425, 30)
                self.layout.addWidget(grpBouton)
                self.icon = QIcon('ressources/modif.png')
                # aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModifTitre0 = BoutonIndex(grpBouton, timeNote, self.videoID)
                self.btnModifTitre0.setIcon(self.icon)
                self.btnModifTitre0.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                  'border-style: solid; border-color: gray; border-width: 0px;'
                                                  'background-color: #201F1F')
                self.btnModifTitre0.setFixedSize(25, 25)
                self.btnModifTitre0.move(5, 5)
                self.btnModifTitre0.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnModifTitre0.clicked.connect(self.evt_btnModif_clicked)
                #
                self.icon = QIcon('ressources/playNote.png')
                self.btnPlayNoteTitre0 = BoutonIndex(grpBouton, timeNote, self.videoID)
                self.btnPlayNoteTitre0.setIcon(self.icon)
                self.btnPlayNoteTitre0.setStyleSheet(
                    'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                    'border-style: solid; border-color: gray; border-width: 0px;'
                    'background-color: #201F1F')
                self.btnPlayNoteTitre0.setFixedSize(25, 25)
                self.btnPlayNoteTitre0.move(35, 5)
                self.btnPlayNoteTitre0.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnPlayNoteTitre0.clicked.connect(self.evt_btnPlayNote_clicked)
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
                tedNote.setFixedSize(420, 100)
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                self.layout.addWidget(tedNote)
                self.listWidget.append(tedNote)
                boolModif = False
            # **************************
            # **** PARAGRAPH   *********
            if titreAux != None and timeNote > 0 and self.chkTitre:  # Titre général
                # GroupBox pour les boutons modif et play
                if boolModif:
                    grpBouton = QGroupBox(self)
                    grpBouton.setFixedSize(425, 30)
                    grpBouton.setStyleSheet('background: #111111;')
                    self.layout.addWidget(grpBouton)
                    self.icon = QIcon('ressources/modif.png')
                    aux = ''
                    self.btnModifTitre1 = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.btnModifTitre1.setIcon(self.icon)
                    self.btnModifTitre1.setStyleSheet(
                        'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                        'border-style: solid; border-color: gray; border-width: 0px;'
                        'background-color: #201F1F')
                    self.btnModifTitre1.setFixedSize(25, 25)
                    self.btnModifTitre1.move(5, 5)
                    self.btnModifTitre1.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnModifTitre1.clicked.connect(self.evt_btnModif_clicked)
                    #
                    self.icon = QIcon('ressources/playNote.png')
                    self.btnPlayNoteTitre1 = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.btnPlayNoteTitre1.setIcon(self.icon)
                    self.btnPlayNoteTitre1.setStyleSheet(
                        'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                        'border-style: solid; border-color: gray; border-width: 0px;'
                        'background-color: #201F1F')
                    self.btnPlayNoteTitre1.setFixedSize(25, 25)
                    self.btnPlayNoteTitre1.move(35, 5)
                    self.btnPlayNoteTitre1.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnPlayNoteTitre1.clicked.connect(self.evt_btnPlayNote_clicked)
                # QTextEdit
                font = QFont()
                font.setFamily('Arial')
                font.setPointSize(13)
                font.setBold(True)
                tedNote = QTextEdit(self)
                tedNote.setText(titreAux.texte)
                tedNote.setFont(font)
                tedNote.viewport().installEventFilter(self)
                tedNote.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                tedNote.setFixedSize(425, 50)
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                self.layout.addWidget(tedNote)
                self.listWidget.append(tedNote)
                boolModif = False
            # **************************
            # ****  I M A G E  *********
            if imageAux != None and self.chkImage:
                #  Récupération du cemin complet de la video pour extraction
                query1 = QSqlQuery()
                query1.exec(f'SELECT * FROM videoFileTab WHERE cle={cleVideo}')
                textLegende = ''
                videoPath = ''
                if query1.next():
                    videoPath = query1.value('videoFullPath')
                #  Recherche de la légende
                query = QSqlQuery()
                query.exec(f'SELECT texte FROM Paragraph WHERE timeNote={self.timeNoteCour} AND cleVideo={cleVideo} '
                           f'AND picture={True}')
                if query.next():
                    textLegende = query.value('texte')
                img = self.extractPicture(videoPath, 423, 249, timeNote)
                qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                self.pixmap01 = QPixmap.fromImage(qimg)

                grpBouton = QGroupBox(self)
                grpBouton.setFixedSize(425, 30)
                grpBouton.setStyleSheet('background: #111111;')
                self.layout.addWidget(grpBouton)
                self.icon = QIcon('ressources/modif.png')
                if boolModif:
                    # aux = strTime(self.paragraphCour.timeNote)
                    aux = ''
                    self.btnModifPicture = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.btnModifPicture.setIcon(self.icon)
                    self.btnModifPicture.setStyleSheet(
                        'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                        'border-style: solid; border-color: gray; border-width: 0px;'
                        'background-color: #201F1F')
                    self.btnModifPicture.setFixedSize(25, 25)
                    self.btnModifPicture.move(0, 5)
                    self.btnModifPicture.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnModifPicture.clicked.connect(self.evt_btnModif_clicked)
                    #
                    self.icon = QIcon('ressources/playNote.png')
                    self.btnPlayNotePicture = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.btnPlayNotePicture.setIcon(self.icon)
                    self.btnPlayNotePicture.setStyleSheet(
                        'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                        'border-style: solid; border-color: gray; border-width: 0px;'
                        'background-color: #201F1F')
                    self.btnPlayNotePicture.setFixedSize(25, 25)
                    self.btnPlayNotePicture.move(35, 5)
                    self.btnPlayNotePicture.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnPlayNotePicture.clicked.connect(self.evt_btnPlayNote_clicked)
                #
                self.icon = QIcon('ressources/fullScreen.png')
                self.btnfullScreen = BoutonIndex(grpBouton, timeNote, self.videoID)
                self.btnfullScreen.setIcon(self.icon)
                self.btnfullScreen.setStyleSheet(
                    'font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                    'border-style: solid; border-color: gray; border-width: 0px;'
                    'background-color: #201F1F')
                self.btnfullScreen.setFixedSize(25, 25)
                if boolModif:
                    x = 65
                else:
                    x = 0
                self.btnfullScreen.move(x, 5)
                self.btnfullScreen.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnfullScreen.clicked.connect(self.evt_fullScreen_clicked)
                #  GrpBox principal
                grpPicture = QLabel(self)
                grpPicture.setPixmap(self.pixmap01.scaled(423, 249, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                if textLegende == '' or textLegende == None:
                    pass
                else:
                    #  GrpBox légende
                    grpLegende = QGroupBox(grpPicture)
                    grpLegende.setFixedSize(423, 20)
                    grpLegende.setStyleSheet('background: white')
                    grpLegende.move(0, 220)
                    #  label légende
                    lblLegende = QLabel(grpLegende)
                    lblLegende.setText(textLegende)
                    lblLegende.setFixedSize(423, 20)
                    lblLegende.setAlignment(Qt.AlignCenter)
                    lblLegende.setStyleSheet('background: white; color: black')
                    lblLegende.move(0, 0)
                #
                self.layout.addWidget(grpPicture)
                self.layout.setAlignment(grpPicture, Qt.AlignLeft | Qt.AlignTop)
                self.listWidget.append(grpPicture)
                boolModif = False

            # **************************
            # ****   N O T E   *********
            if texteAux != None and self.chkNote:
                self.listLien = []
                query = QSqlQuery()
                query.exec(f'SELECT * FROM linkTab WHERE cleVideo={cleVideo}')
                while query.next():
                    aux = (query.value('timeCode'), query.value('URL'), query.value('mot'))
                    self.listLien.append(aux)
                # GroupBox pour les boutons modif et playboo
                if boolModif:
                    grpBouton = QGroupBox(self)
                    grpBouton.setFixedSize(500, 50)
                    grpBouton.setStyleSheet('background: #111111; border: 0px')
                    self.layout.addWidget(grpBouton)
                    self.btnModifNote = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.icon = QIcon('ressources/modif.png')
                    self.btnModifNote.setIcon(self.icon)
                    self.btnModifNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                    'border-style: solid; border-color: gray; border-width: 0px;'
                                                    'background-color: #201F1F')
                    self.btnModifNote.setFixedSize(25, 25)
                    self.btnModifNote.move(5, 5)
                    self.btnModifNote.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnModifNote.clicked.connect(self.evt_btnModif_clicked)
                    #
                    self.icon = QIcon('ressources/playNote.png')
                    self.btnPlayNote = BoutonIndex(grpBouton, timeNote, self.videoID)
                    self.btnPlayNote.setIcon(self.icon)
                    self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                   'border-style: solid; border-color: gray; border-width: 0px;'
                                                   'background-color: #201F1F')
                    self.btnPlayNote.setFixedSize(25, 25)
                    self.btnPlayNote.move(35, 5)
                    self.btnPlayNote.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btnPlayNote.clicked.connect(self.evt_btnPlayNote_clicked)
                # QTextEdit
                tedNote = QTextEdit(self)
                tedNote.viewport().installEventFilter(self)
                tedNote.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                tedNote.setFixedSize(425, 100)
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                self.layout.addWidget(tedNote)
                self.listWidget.append(tedNote)
                self.listNote.append(tedNote)
                query = QSqlQuery()
                query.exec(f'SELECT * FROM paragraph WHERE timeNote={timeNote} AND cleVideo={cleVideo} AND  note')
                if query.next():
                    aux = query.value('texte')
                    aux = aux.replace("²", "'")
                    aux = aux.replace('<br>', '')
                    aux = aux.replace("&#09", "\t")
                tedNote.setText(aux)
                documentSize = tedNote.document().size()
                tedNote.setFixedHeight(int(documentSize.height() + 10))
                self.tedNote = tedNote
                self.listTed.append(tedNote)
                self.listTimeCodeNote.append(timeNote)

        # # *******************************************************************************************
        self.spacerItem = QSpacerItem(40, 200, QSizePolicy.Expanding, QSizePolicy.Maximum)
        # self.layout.addItem(self.spacerItem)
        self.scroll_area.setWidget(self.widget)
        self.setCentralWidget(self.scroll_area)

        formScreen1.marqueNote.videoID = cleVideo
        formScreen1.marqueNote.populateMarqueNote()

    def extractPicture(self, video, haut, large, timeNote):
        vidcap = cv2.VideoCapture(video)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
        success, image = vidcap.read()
        if success:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image

    def evt_fullScreen_clicked(self):
        dlgFullScreen = QDialog(self)
        dlgFullScreen.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        dlgFullScreen.setGeometry(100, 100, 700, 500)
        dlgFullScreen.show()
        lytPicture = QVBoxLayout(dlgFullScreen)
        dlgFullScreen.setLayout(lytPicture)
        lblPicture = QLabel()
        lytPicture.addWidget(lblPicture)
        #
        sender = self.sender()
        timeCode = sender.timeCode
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            videoPath = query.value('videoFullPath')
            img = self.extractPicture(videoPath, self.width(), self.height(), timeCode)
            qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            pixmap01 = QPixmap.fromImage(qimg)
            lblPicture.setPixmap(pixmap01)
            lblPicture.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def evt_btnModif_clicked(self):
        sender = self.sender()
        timeCode = sender.timeCode
        cle = formScreen1.videoID
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={cle}')
        if query.next():
            videoPath = query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, cle, timeCode, False)
            formGererNote.populateNoteModif()
            formGererNote.show()

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
            format = cursor.charFormat()
            # liste des liens du timeCode
            listAux = [(mot, URL) for (timeCode, mot, URL) in self.listLien if timeCode == self.listTimeCodeNote[index]]
            if format.fontWeight() == QFont.Bold and format.fontUnderline():
                for tpl in listAux:
                    URL, lien = tpl
                    if selected_text in lien:
                        QDesktopServices.openUrl(QUrl(URL))
            else:
                pass
        return super().eventFilter(source, event)

    def effacer(self):
        for i in reversed(range(self.layout.count())):
            try:
                self.layout.itemAt(i).widget().deleteLater()
            except:
                spacer = self.layout.itemAt(0)
                self.layout.removeItem(spacer)

    def evt_btnPlayNote_clicked(self):
        # if e.button() == Qt.LeftButton:  # lecture de la vidéo à partir du timeNote de l'image
        sender = self.sender()
        timeCode = sender.timeCode
        formScreen1.mediaPlayer.setPosition(timeCode * 1000)
        formScreen1.marqueNote.testMarque(-timeCode + 5)
        if formScreen1.mediaPlayer.state() == QMediaPlayer.PlayingState:
            formScreen1.mediaPlayer.pause()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            formScreen1.mediaPlayer.setPlaybackRate(formScreen1.vitesseCour)
            formScreen1.mediaPlayer.play()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************         M A I N P A R A G R A P H         ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainParagraph(QMainWindow, Ui_mainParagraph):
    def __init__(self, parent, videoID, mainWin):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.videoID = videoID[0]
        self.mainWin = mainWin

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        #  Récupération position du marque page
        self.marquePage = 0
        self.videoName = ''
        query = QSqlQuery()
        query.exec(f'SELECT marquePage, videoName FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            self.marquePage = query.value('marquePage')
            self.videoName = query.value('videoName')
        self.setStyleSheet('background-color: #333; border: 0px')

        #  ***************************************************************************
        #  Top Zone
        #  ***************************************************************************
        btnSize = QSize(32, 20)
        btnSizea = QSize(70, 20)
        btnSize1 = QSize(80, 20)
        btnSize2 = QSize(100, 25)
        #
        self.btnMarquePage = QPushButton(self)
        self.btnMarquePage.setIcon(QIcon('ressources/marquePage.png'))
        self.btnMarquePage.setFixedSize(QSize(20, 20))
        self.btnMarquePage.clicked.connect(self.evt_btnMarquePage_clicked)
        self.btnMarquePage.setCursor(Qt.PointingHandCursor)
        self.lytTop.addWidget(self.btnMarquePage)
        self.lblMarquePage = QLabel(self)
        self.lblMarquePage.setText(self.strTime(self.marquePage))
        self.lytTop.addWidget(self.lblMarquePage)
        self.lytTop.addSpacing(0)
        #
        self.btnAllerA = self.btnMarquePage = QPushButton(self)
        self.btnAllerA.setIcon(QIcon('ressources/descendre.png'))
        self.btnAllerA.setFixedSize(btnSize)
        self.btnAllerA.setCursor(Qt.PointingHandCursor)
        self.btnAllerA.clicked.connect(self.evt_btnAllerA_clicked)
        self.lytTop.addWidget(self.btnAllerA)
        #
        self.btnRetour = QPushButton(self._trad('Retour', self.lngCourGlobal), self)
        self.btnRetour.move(80, 10)
        self.btnRetour.setVisible(False)
        self.lytTop.addWidget(self.btnRetour)
        self.lytTop.addSpacing(50)
        #
        self.chkImage = QCheckBox(self._trad('Images', self.lngCourGlobal), self)
        self.chkImage.setStyleSheet('color: white')
        self.chkImage.move(140, 10)
        self.chkImage.setChecked(True)
        self.chkImage.repaint()
        self.lytTop.addWidget(self.chkImage)
        #
        self.chkNote = QCheckBox(self._trad('Notes', self.lngCourGlobal), self)
        self.chkNote.move(300, 10)
        self.chkNote.setChecked(True)
        self.chkNote.setStyleSheet('color: white')
        self.lytTop.addWidget(self.chkNote)
        #
        self.chkTitre = QCheckBox(self._trad('Titres', self.lngCourGlobal), self)
        self.chkTitre.move(380, 10)
        self.chkTitre.setChecked(True)
        self.chkTitre.setStyleSheet('color: white')
        self.lytTop.addWidget(self.chkTitre)

        #############################################
        ###  signal handler
        #############################################
        self.chkTitre.clicked.connect(self.majChkNote)
        self.chkNote.clicked.connect(self.majChkNote)
        self.chkImage.clicked.connect(self.majChkNote)
        # self.chkLien.clicked.connect(self.loadNotes)
        self.btnMarquePage.clicked.connect(self.evt_btnMarquePage_clicked)

        #  ***************************************************************************
        #  Note Zone
        #  ***************************************************************************
        global objNote
        #  Ancienne méthode
        # self.objNote = ObjNote1(self, self.videoID)
        #  Nouvelle méthode
        self.objNote = AtelierParagraph(self, self.videoID)

        self.lytNote.addWidget(self.objNote)
        self.repaint()
        self.unsetCursor()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        strHeure, strMinute, strSeconde = '', '', ''
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')

    def majChkNote(self):
        try:
            mainXX = mainWindow.tabObjetScreen.docParagraph.widget()
            mainXX.objNote.initChkNote(self.chkImage.isChecked(), self.chkNote.isChecked(), self.chkTitre.isChecked())
            mainXX.objNote.populateParagraph(self.videoID)
        except:
            pass

    def loadNotes(self):
        self.objNote.populateParagraph(formScreen1.videoID)

    def evt_btnMarquePage_clicked(self):
        self.marquePage = int(self.mainWin.tabObjetScreen.barOnglet.formScreen1.mediaPlayer.position()/1000)
        self.lblMarquePage.setText(self.strTime(self.marquePage))
        #  Enregistrer le marquePage
        tplData = (self.videoName, self.marquePage)
        tplChamps = ('videoName', 'marquePage')
        query = QSqlQuery()
        query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle = {self.videoID}')

    def evt_btnAllerA_clicked(self):
        self.mainWin.tabObjetScreen.barOnglet.formScreen1.mediaPlayer.setPosition(self.marquePage * 1000)



# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************      T A B O B J E C T S C R E E N        ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TabObjectScreen(QMainWindow):
    def __init__(self, parent, lstVideoOnglet):
        super(TabObjectScreen, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(500, 500)
        self.setStyleSheet('background-color: #222')
        self.parent = parent  # -> MainWindow
        self.mainWin = parent
        self.lstVideoOnglet = lstVideoOnglet


        #  *******************************************************************

        #   P A R A G R A P H
        self.docParagraph = QDockWidget('Paragraph', self)
        self.docParagraph.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.docParagraph.setFloating(False)
        self.docParagraph.setStyleSheet('background: #555; color: white')
        textEdit = QTextEdit()
        textEdit.setFontPointSize(16)

        #  S C R E E N
        self.barOnglet = BarOnglet(self, lstVideoOnglet, self.mainWin)
        self.setCentralWidget(self.barOnglet)
        # self.barOnglet.setStyleSheet('background: orange')

        return  # /////
        self.barOnglet.majCurrentOnglet(lstVideoOnglet[0])


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                P U S H O N G L E T             ******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class PushOnglet(QLabel):
    def __init__(self, parent=None, cleVideo=None, boolEnabled=None):
        super().__init__(parent)
        self.parent = parent
        self.boolEnabled = boolEnabled
        self.setFixedSize(131, 50)
        self.setAlignment(Qt.AlignVCenter)

        self.checked = False

        self.cleVideo = cleVideo

        videoCour = VideoFileRecord(self.cleVideo)

        self.setText('      ' + videoCour.videoName)

        self.btnRemove = QPushButton(self)
        self.btnRemove.setFixedSize(25, 25)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(8)
        font.setBold(False)
        self.btnRemove.setFont(font)
        self.btnRemove.setText('X')
        self.btnRemove.setStyleSheet('QPushButton {background-color: transparent; color: #888; border-radius: 4px; '
                                     'padding: 2px; outline: none; border: none} '
                                     'QPushButton::hover{color: red; background-color: #555}')
        # self.btnRemove.move(103, 0)
        self.btnRemove.move(0, 3)
        self.btnRemove.clicked.connect(lambda: mainWindow.removeTab(self.cleVideo))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.majCurrentOnglet(self.cleVideo)

    def setStylePushOnglet(self, boolEnabled):
        if boolEnabled:
            self.setStyleSheet('QLabel {background: #4e5254; color: white; border-top-left-radius: 7px; '
                               'border-top-right-radius: 7px; padding-right: 10} QLabel::hover{background-color: #666}')
        else:
            self.setStyleSheet('QLabel {background: #3c3f41; color: #999; border-top-left-radius: 7px; '
                               'border-top-right-radius: 7px; padding-right: 10} QLabel::hover{background-color: #666}')



# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************               B A R O N G L E T           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BarOnglet(QWidget):
    def __init__(self, parent, lstVideoOnglet, mainWin):
        super().__init__()
        self.setGeometry(100, 100, 100, 600)
        self.setGeometry(100, 100, mainWindow.width(), 600)
        self.setStyleSheet('background-color: #333')
        # return  # /////return
        self.lytMain = QVBoxLayout()
        self.setLayout(self.lytMain)
        self.lstVideoOnglet = lstVideoOnglet
        self.cleVideo = lstVideoOnglet[0]
        self.videoTabCle = lstVideoOnglet[0]
        self.parent = parent
        self.mainWin = mainWin
        self.lstOnglet = []

        lytOnglet = QHBoxLayout()
        self.lytMain.addLayout(lytOnglet)
        self.lytMain.setSpacing(2)
        self.grpBoxOnglet = QGroupBox()
        self.grpBoxOnglet.setFixedHeight(30)
        self.grpBoxOnglet.setStyleSheet('border: 0px; color: #aaa')
        lytOnglet.addWidget(self.grpBoxOnglet)
        self.createFormScreen1()
        # ***************************************************************************************
        #   P A R A G R A P H
        self.mainParagraph = MainParagraph(self.parent.docParagraph, lstVideoOnglet, self.mainWin)
        self.parent.docParagraph.setWidget(self.mainParagraph)
        self.parent.docParagraph.setFloating(False)
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.parent.docParagraph)
        # ***************************************************************************************

        self.lstOnglet = []
        i = 0
        for cle in lstVideoOnglet:
            pushOnglet = PushOnglet(self, cle)
            pushOnglet.move(136*i + 10, 10)
            self.lstOnglet.append(pushOnglet)
            i += 1
        try:
            if self.btnPlus:
                pass
        except:
            self.btnPlus = QPushButton(self)
            self.btnPlus.setFixedSize(16, 22)
            self.btnPlus.setText('+')
            self.btnPlus.setStyleSheet('QPushButton {background-color: #aaa; color: #121212; '
                                         'padding: 2px; outline: none; border: none} QPushButton::hover{color: white;}')
            self.btnPlus.setFont(QFont('Arial', 20))
            self.btnPlus.move(136*i + 10, 15)

        self.btnPlus.clicked.connect(mainWindow.evt_btnPlusTab_clicked)
        self.majCurrentOnglet(self.lstOnglet[0].cleVideo)

    def createFormScreen1(self):
        qwidget = QWidget()

        global formScreen1
        try:
            if formScreen1:
                formScreen1.close()
        except:
            pass
        formScreen1 = FormScreen1(qwidget, self.cleVideo, mainWindow)
        self.formScreen1 = formScreen1
        self.lytMain.addWidget(formScreen1)

    def majCurrentOnglet(self, cleVideo):
        for onglet in self.lstOnglet:
            if onglet.cleVideo == cleVideo:
                onglet.setStylePushOnglet(True)
                onglet.checked = True
                onglet.setFixedHeight(30)
                self.videoTabCle = cleVideo
                formScreen1.loadVideo(onglet.cleVideo)
                self.mainParagraph.videoID = onglet.cleVideo
                self.mainParagraph.loadNotes()
            else:
                onglet.setStylePushOnglet(False)
                onglet.checked = False
                onglet.setFixedHeight(30)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************      S L I D E R T I M E C O D E          ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class SliderTimeCode(QSlider):
    def __init__(self, parent=None):
        super(SliderTimeCode, self).__init__()
        self.parent = parent

        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFixedHeight(10)
        self.setRange(0, 0)
        sStyleSliderH = """
                                      QSlider{background-color: gray}
                                      QSlider::groove:horizontal {
                                      border: 1px solid #3A3939;
                                      height: 6px;
                                      background: #201F1F;
                                      margin: 0px 0;
                                      border-radius: 4px;
                                                                  }
                                      QSlider::handle:horizontal {
                                      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);
                                      border: 1px solid #3A3939;
                                      width: 14px;
                                      height: 14px;
                                      margin: -1px 0;
                                      border-radius: 0px;
                                                          }
                          """
        self.setStyleSheet(sStyleSliderH)



# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           F O R M S C R E E N 1           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormScreen1(QMainWindow):
    def __init__(self, parent, videoID, mainWin):
        super(FormScreen1, self).__init__()
        self.resize(700, 411)
        self.parent = parent
        self.videoCour = -1
        self.durationCour = 0
        self.videoID = videoID
        self.videoPath = ''
        self.vitesseCour = 1
        self.mainWin = mainWin
        self.pixmap = None
        self.installEventFilter(self)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
        if aux == 'Français':
            self.lngCourGlobal = 'fr'
        if aux == 'Anglais':
            self.lngCourGlobal = 'en'

        centralWidget = QWidget()
        centralWidget.setStyleSheet('background-color: #333')
        self.setCentralWidget(centralWidget)
        lytMain = QVBoxLayout(centralWidget)  # Layout principal

        #  ***************************************************************************
        #  Zone de titre
        #  ***************************************************************************
        #  Titre de la vidéo
        lytTitre = QHBoxLayout()
        lblTitre = QLabel(self._trad('Titre complet de la vidéo affichée dans le player', self.lngCourGlobal))
        lblTitre.setFixedHeight(30)
        lblTitre.setStyleSheet('background-color: transparent; color: #aaa')
        lblTitre.setAlignment(Qt.AlignHCenter)
        # Bouton 1:1
        self.btn11 = QPushButton('1:1')
        self.btn11.setStyleSheet('border-radius: 0px; border: 1px;')
        self.btn11.setFixedSize(QSize(24, 24))
        lytTitre.addWidget(self.btn11)
        lytTitre.addWidget(lblTitre)
        lytMain.addLayout(lytTitre)

        #  ***************************************************************************
        #  Widget Player
        #  ***************************************************************************
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet('background-color: orange')
        lytMain.addWidget(self.videoWidget)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setVolume(30)
        #  *****************************************)**********************************
        #  Slider Zone
        #  ***************************************************************************
        lytSlider = QVBoxLayout()
        # lytSliderMain.addLayout(lytSlider)
        self.sldVideo = SliderTimeCode(self)
        lytSlider.addWidget(self.sldVideo)
        lytMain.addLayout(lytSlider)
        video = VideoFileRecord(self.videoID)
        lblTitre.setText(video.videoName)
        v = cv2.VideoCapture(video.videoPath)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        v.release()

        self.marqueNote = MarqueNote(self, self.videoID, duration)
        self.marqueNote.installEventFilter(self)
        lytSlider.addWidget(self.marqueNote)

        lblNavigMarque = QLabel()
        lblNavigMarque.setFixedHeight(30)
        btnPlusMarque = QPushButton(lblNavigMarque)
        btnPlusMarque.setFixedHeight(24)
        btnPlusMarque.setIcon(QIcon('ressources/btnPlus.png'))
        f = open('styles/QPushButton.txt', 'r')
        style = f.read()
        styleQPushButton = style
        btnPlusMarque.setStyleSheet(styleQPushButton)
        btnPlusMarque.move(83, 0)
        btnMoinsMarque = QPushButton(lblNavigMarque)
        btnMoinsMarque.setFixedHeight(24)
        f = open('styles/QPushButton.txt', 'r')
        style = f.read()
        styleQPushButton = style
        btnMoinsMarque.setStyleSheet(styleQPushButton)
        btnMoinsMarque.setIcon(QIcon('ressources/btnMoins.png'))
        btnMoinsMarque.move(0, 0)
        btnEditMarque = QPushButton(lblNavigMarque)
        btnEditMarque.setText(self._trad('Editer', self.lngCourGlobal))
        btnEditMarque.setStyleSheet(styleQPushButton)
        btnEditMarque.setFixedSize(QSize(70, 24))
        btnEditMarque.move(20, 0)
        lytSlider.addWidget(lblNavigMarque)

        #  ***************************************************************************
        #  Control Zone
        #  ***************************************************************************
        btnSize = QSize(32, 20)
        btnSizea = QSize(70, 20)
        btnSize1 = QSize(80, 20)
        btnSize2 = QSize(100, 20)
        lytControl = QHBoxLayout()
        # Label lecture écoulée
        self.lblPosition = QLabel('00:00:00')
        self.lblPosition.setFixedSize(60, 25)
        self.lblPosition.setAlignment(Qt.AlignCenter)
        self.lblPosition.setStyleSheet('background-color: #333333; color: #ffffff')
        lytControl.addWidget(self.lblPosition)
        #
        self.btnStart = QPushButton('')
        self.btnStart.setFixedSize(btnSize)
        self.btnStart.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.btnStart.setStyleSheet('background-color: #5FACF2')
        lytControl.addWidget(self.btnStart)
        #
        self.btnMoins30 = QPushButton('-30')
        self.btnMoins30.setFixedSize(btnSize)
        self.btnMoins30.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnMoins30)
        #
        self.btnMoins5 = QPushButton('-5')
        self.btnMoins5.setFixedSize(btnSize)
        self.btnMoins5.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnMoins5)
        #
        self.btnMoins1 = QPushButton('-1')
        self.btnMoins1.setFixedSize(btnSize)
        self.btnMoins1.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnMoins1)
        #
        self.btnMoins01 = QPushButton('-0.1')
        self.btnMoins01.setFixedSize(btnSize)
        self.btnMoins01.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnMoins01)
        #
        self.btnPlay = QPushButton()
        self.btnPlay.setFixedSize(btnSize)
        self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btnPlay.setStyleSheet('background-color: #5FACF2')
        lytControl.addWidget(self.btnPlay)
        #
        self.btnPlus01 = QPushButton('+0.1')
        self.btnPlus01.setFixedSize(btnSize)
        self.btnPlus01.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnPlus01)
        #
        self.btnPlus1 = QPushButton('+1')
        self.btnPlus1.setFixedSize(btnSize)
        self.btnPlus1.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnPlus1)
        #
        self.btnPlus5 = QPushButton('+5')
        self.btnPlus5.setFixedSize(btnSize)
        self.btnPlus5.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnPlus5)
        #
        self.btnPlus30 = QPushButton('+30')
        self.btnPlus30.setFixedSize(btnSize)
        self.btnPlus30.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnPlus30)
        #
        self.btnEnd = QPushButton()
        self.btnEnd.setFixedSize(btnSize)
        self.btnEnd.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.btnEnd.setStyleSheet('color:black; background-color: #5FACF2')
        lytControl.addWidget(self.btnEnd)
        #
        self.lblDuration = QLabel('00:00:00')
        self.lblDuration.setStyleSheet('background-color: #333333; color: #ffffff')
        self.lblDuration.setFixedSize(60, 25)
        lytControl.addWidget(self.lblDuration)
        #
        lytControl.addStretch()
        #
        self.lblVolume = QLabel('')
        pxVolume = QPixmap('ressources/volume.png')
        self.lblVolume.setPixmap(pxVolume)
        lytControl.addWidget(self.lblVolume)
        #
        self.sldVolume = QSlider(Qt.Horizontal)
        f = open('styles/QSlider.txt', 'r')
        style = f.read()
        self.sldVolume.setStyleSheet(style)
        self.sldVolume.setRange(0, 100)
        self.sldVolume.setFixedWidth(100)
        self.sldVolume.setValue(30)
        lytControl.addWidget(self.sldVolume)
        #
        pxZoom = QPixmap('ressources/zoom.png')
        lblZoom = QLabel()
        lblZoom.setPixmap(pxZoom)
        self.cmbZoom = QComboBox()
        f = open('styles/QComboBox.txt', 'r')
        style = f.read()
        self.cmbZoom.setStyleSheet(style)
        self.cmbZoom.addItem('Z1', (700, 411))
        self.cmbZoom.addItem('Z2', (840, 494))
        self.cmbZoom.addItem('Z3', (1008, 588))
        self.cmbZoom.addItem('Z4', (1209, 711))
        # lytControl.addWidget(self.cmbZoom)
        #
        pxVitesse = QPixmap('ressources/vitesse.png')
        lblVitesse = QLabel()
        lblVitesse.setPixmap(pxVitesse)
        lytControl.addWidget(lblVitesse)
        self.cmbVitesse = QComboBox(self)
        self.cmbVitesse.setFixedWidth(80)
        f = open('styles/QComboBox.txt', 'r')
        style = f.read()
        self.cmbVitesse.setStyleSheet(style)
        btnMoinsMarque.setStyleSheet(styleQPushButton)
        self.cmbVitesse.addItem('x 0.25', '0.25')
        self.cmbVitesse.addItem('x 0.5', '0.5')
        self.cmbVitesse.addItem('x 0.75', '0.75')
        self.cmbVitesse.addItem('x 1', '1')
        self.cmbVitesse.addItem('x 1.25', '1.25')
        self.cmbVitesse.addItem('x 1.5', '1.5')
        self.cmbVitesse.addItem('x 1.75', '1.75')
        self.cmbVitesse.addItem('x 2', '2')
        self.cmbVitesse.addItem('x 3', '3')
        self.cmbVitesse.addItem('x 4', '4')
        self.cmbVitesse.setCurrentIndex(3)
        lytControl.addWidget(self.cmbVitesse)

        #  +++++++++++++++++++++++++++++++++++++++++
        lytMain.addLayout(lytControl)
        #  ***************************************************************************
        #  Marquage Zone
        #  ***************************************************************************
        lytMarquage = QHBoxLayout()
        lytMarquage.addStretch()
        self.lblFixeMarque = QLabel(lblNavigMarque)
        self.lblFixeMarque.setStyleSheet('color: #ffffff')
        self.lblFixeMarque.setText(self._trad('Fixer la marque :', self.lngCourGlobal))
        self.lblFixeMarque.move(150, 3)
        #
        self.btnMarque = QPushButton(lblNavigMarque)
        f = open('styles/QPushButton.txt', 'r')
        style = f.read()
        self.btnMarque.setStyleSheet(style)
        self.btnMarque.setText('--:--:--')
        self.btnMarque.move(260, 3)
        self.btnMarque.setFixedSize(btnSize2)
        #
        self.btnMarqueRetour = QPushButton(lblNavigMarque)
        self.btnMarqueRetour.setText(self._trad('Retour marque', self.lngCourGlobal))
        self.btnMarqueRetour.setStyleSheet(style)
        self.btnMarqueRetour.setFixedSize(btnSize2)
        self.btnMarqueRetour.move(370, 3)
        #
        self.btnCreerNote = QPushButton(lblNavigMarque)
        self.btnCreerNote.setText(self._trad('Créer note', self.lngCourGlobal))
        self.btnCreerNote.setStyleSheet(style)
        self.btnCreerNote.setFixedSize(btnSize2)
        self.btnCreerNote.move(480, 3)
        #  ++++++++++++++++++++++
        lytMain.addLayout(lytMarquage)

        #############################################
        ###  signal handler
        #############################################
        self.btnStart.clicked.connect(self.evt_btnStart_clicked)
        self.btnMoins30.clicked.connect(self.evt_btnMoins30_clicked)
        self.btnMoins5.clicked.connect(self.evt_btnMoins5_clicked)
        self.btnMoins1.clicked.connect(self.evt_btnMoins1_clicked)
        self.btnMoins01.clicked.connect(self.evt_btnMoins01_clicked)
        self.btnPlay.clicked.connect(self.evt_btnPlay_clicked)
        self.btnPlus01.clicked.connect(self.evt_btnPlus01_clicked)
        self.btnPlus1.clicked.connect(self.evt_btnPlus1_clicked)
        self.btnPlus5.clicked.connect(self.evt_btnPlus5_clicked)
        self.btnPlus30.clicked.connect(self.evt_btnPlus30_clicked)
        self.btnEnd.clicked.connect(self.evt_btnEnd_clicked)
        btnMoinsMarque.clicked.connect(self.evt_btnMoinsMarque_clicked)
        btnPlusMarque.clicked.connect(self.evt_btnPlusMarque_clicked)
        btnEditMarque.clicked.connect(self.evt_btnEditMarque_clicked)
        #
        self.mediaPlayer.stateChanged.connect(self.evt_mediaPlayer_stateChanged)
        self.mediaPlayer.positionChanged.connect(self.evt_mediaPlayer_positionChanged)
        self.mediaPlayer.durationChanged.connect(self.evt_mediaPlayer_changeDuration)
        #
        self.cmbZoom.currentIndexChanged.connect(self.evt_cmbZoom_currentIndexChanged)
        #
        self.btn11.clicked.connect(self.evt_btn11_clicked)
        #
        self.cmbVitesse.currentIndexChanged.connect(self.evt_cmbVitesse_currentIndexChanged)
        self.cmbVitesse.setFixedWidth(65)
        #
        self.sldVolume.sliderMoved.connect(self.evt_sldVolume_sliderMoved)
        self.sldVideo.sliderMoved.connect(self.evt_sldVideo_sliderMoved)
        #
        self.btnMarque.clicked.connect(self.evt_btnMarque_clicked)
        self.btnMarqueRetour.clicked.connect(self.evt_btnMarqueRetour_clicked)
        self.btnCreerNote.clicked.connect(self.evt_btnCreerNote_clicked)

        self.mediaPlayer.error.connect(self.handleError)
        self.repaint()

        self.loadVideo(self.videoID)

        self.mediaPlayer.pause()
        self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def evt_btnEditMarque_clicked(self):
        if self.marqueNote.marqueCour == -1:
            return
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            videoPath = query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            # formGererNote = FormGererNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueNote.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif()
                formGererNote.show()

    def evt_btnMoinsMarque_clicked(self):
        if self.marqueNote.marqueCour == -1:
            return
        index = self.marqueNote.listeMarques.index(self.marqueNote.marqueCour)
        if index == 0:
            self.marqueNote.marqueCour = -1
            self.marqueNote.setLabel()
            self.marqueNote.majLblMarque()
        else:
            index -= 1
            self.marqueNote.marqueCour = self.marqueNote.listeMarques[index]
            self.marqueNote.setLabel()
            self.marqueNote.majLblMarque()
            self.mediaPlayer.setPosition(self.marqueNote.marqueCour * 1000)

    def evt_btnPlusMarque_clicked(self):
        if self.marqueNote.marqueCour == self.marqueNote.listeMarques[self.marqueNote.nbPicot - 1]:
            return
        else:
            if self.marqueNote.marqueCour == -1:
                self.marqueNote.marqueCour = 0
            else:
                index = self.marqueNote.listeMarques.index(self.marqueNote.marqueCour) + 1
                self.marqueNote.marqueCour = self.marqueNote.listeMarques[index]
            self.marqueNote.setLabel()
            self.marqueNote.majLblMarque()
            self.mediaPlayer.setPosition(self.marqueNote.marqueCour * 1000)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.RightButton):
            pos = event.pos()
            self.xCour = event.x()
            self.yCour = event.y()
        if event.type() == QEvent.ContextMenu:
            menu = QMenu()
            menu.addAction(self._trad('Editer', self.lngCourGlobal), self.editMarque)
            menu.addSeparator()
            menu.addAction(self._trad('Aller à', self.lngCourGlobal), self.allerMarque)
            if menu.exec_(event.globalPos()):
                return True
        return QWidget.eventFilter(self, source, event)

    def editMarque(self):
        self.marqueNote.testMarque(self.xCour)
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')

        if query.next():
            videoPath = query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueNote.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif(paragraphCour)
                formGererNote.show()

    def allerMarque(self):
        self.marqueNote.testMarque(self.xCour)
        self.mediaPlayer.setPosition(self.marqueNote.marqueCour * 1000)

    def loadVideo(self, videoID):
        self.videoID = videoID
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={videoID}')
        if query.next():
            self.videoPath = query.value('VideoFullPath')
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoPath)))

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.setPlaybackRate(self.vitesseCour)
            self.mediaPlayer.play()
            time.sleep(1)
            self.mediaPlayer.play()
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    # ************************************************************************************
    # ****** Slot Handler
    # ************************************************************************************
    def closeEvent(self, event):
        #  sauver le marque page (marqueCour) + DateLastView
        marqueCour = int(self.mediaPlayer.position() // 1000)
        query = QSqlQuery()
        tplChamps = ('marquePage', 'DateLastView')
        d = datetime.now().strftime('%Y-%m-%d')
        tplData = (int(self.mediaPlayer.position() // 1000), d)

    def evt_btnStart_clicked(self):
        position = 0
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()
        self.sldVideo.setValue(0)

    def evt_btnMoins30_clicked(self):
        # self.mediaPlayer.pause()
        position = self.mediaPlayer.position() - 30000
        if position < 0:
            position = 0
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()
        self.sldVideo.setValue(position)

    def evt_btnMoins5_clicked(self):
        position = self.mediaPlayer.position() - 5000
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnMoins1_clicked(self):
        position = self.mediaPlayer.position() - 1000
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnMoins01_clicked(self):
        position = self.mediaPlayer.position() - 100
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnPlay_clicked(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.setPlaybackRate(self.vitesseCour)
            self.mediaPlayer.play()
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def evt_btnPlus01_clicked(self):
        position = self.mediaPlayer.position() + 100
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnPlus1_clicked(self):
        position = self.mediaPlayer.position() + 1000
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnPlus5_clicked(self):
        position = self.mediaPlayer.position() + 5000
        self.mediaPlayer.setPosition(position)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_btnPlus30_clicked(self):
        self.mediaPlayer.pause()
        position = self.mediaPlayer.position() + 30000
        self.mediaPlayer.setPosition(position)

    def evt_btnEnd_clicked(self):
        self.mediaPlayer.setPosition(self.durationCour - 100)
        time.sleep(0.1)
        self.mediaPlayer.pause()

    def evt_mediaPlayer_changeDuration(self, duration):
        self.durationCour = duration
        self.lblDuration.setText(self.strTime(duration // 1000))
        self.sldVideo.setRange(0, duration // 1000)

    def evt_mediaPlayer_stateChanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def evt_mediaPlayer_positionChanged(self, position):
        if position < 1000:
            return
        self.sldVideo.setValue(position // 1000)
        self.lblPosition.setText(self.strTime(position // 1000))

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')

    def evt_cmbZoom_currentIndexChanged(self, idx):
        self.zoomCour = list(self.cmbZoom.itemData(idx))
        # self.parent.dockEcran.setFixedSize(self.zoomCour[0], self.zoomCour[1])
        # self.videoWidget.setFixedSize(int(self.zoomCour[0]*1.3), int(self.zoomCour[1]*1.3))
        self.mainWin.setFixedSize(int(self.zoomCour[0] * 1.8), int(self.zoomCour[1] * 1.8))

    def evt_btn11_clicked(self):
        self.zoomCour = list(self.cmbZoom.itemData(0))
        self.cmbZoom.setCurrentIndex(0)
        # self.videoWidget.setFixedSize(int(self.zoomCour[0]*1.3), int(self.zoomCour[1]*1.3))
        self.mainWin.resize(QSize(1326, 780))

    def evt_cmbVitesse_currentIndexChanged(self, idx):
        self.vitesseCour = float(self.cmbVitesse.itemData(idx))
        self.mediaPlayer.setPlaybackRate(self.vitesseCour)

    def evt_sldVolume_sliderMoved(self, position):
        self.mediaPlayer.setVolume(position)
        if position == 0:
            btnSize = QSize(24, 20)
            icon = self.style().standardIcon(QStyle.SP_MediaVolumeMuted)
            pxmap = icon.pixmap(btnSize)
            self.lblVolume.setPixmap(pxmap)
        else:
            btnSize = QSize(24, 24)
            btnSize = QSize(24, 20)
            icon = self.style().standardIcon(QStyle.SP_MediaVolume)
            pxmap = icon.pixmap(btnSize)
            self.lblVolume.setPixmap(pxmap)

    def evt_btnParagraph_clicked(self):
        if self.btnParagraph.text() == 'Paragraph >>':
            self.btnParagraph.setText('<< Paragraph')
            self.formParagraph = MainParagraph(self, videoID=self.videoID)
            self.formParagraph.show()
            for i in range(self.lytMarque.count()):
                try:
                    aux = self.lytMarque.itemAt(i).widget().setVisible(True)
                except:
                    pass
            self.formParagraph.exec_()
        else:
            self.btnParagraph.setText('Paragraph >>')
            for i in range(self.lytMarque.count()):
                try:
                    aux = self.lytMarque.itemAt(i).widget().setVisible(False)
                except:
                    pass
            self.formParagraph.close()

    def evt_btnMarque_clicked(self):
        if self.videoID == -1:
            return
        self.btnMarque.setText(self.strTime(self.mediaPlayer.position() // 1000))
        self.marqueCour = self.mediaPlayer.position() // 1000


    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        strHeure, strMinute, strSeconde = '', '', ''
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')

    def evt_btnMarqueRetour_clicked(self):
        if self.btnMarque.text() == '--:--:--':
            return
        self.mediaPlayer.setPosition(self.marqueCour * 1000)

    def evt_btnCreerNote_clicked(self):
        if self.btnMarque.text() == '--:--:--':
            return
        boolCreer = True
        self.formCreerNote = FormBlockNote(self, self.videoPath, self.videoID, self.marqueCour, boolCreer)
        self.formCreerNote.show()

    def evt_sldVideo_sliderMoved(self, position):
        self.mediaPlayer.setPosition(position * 1000)

    def evt_btnFermer_clicked(self):
        self.parent.screen.close()
        self.parent.paragraph.close()

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')

    # ****************************************************************************
    # ****************************************************************************
    # ****************************************************************************
    def handleError(self):
        QMessageBox.information(self, 'error', str(self.mediaPlayer.error()))


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            M A R Q U E N O T E            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MarqueNote(QLabel):
    def __init__(self, parent=None, videoID=None, duration=None):
        super(MarqueNote, self).__init__()

        self.parent = parent
        self.videoID = videoID
        self.duration = duration
        self._flag = False
        self.listeMarques = []
        self.marqueCour = -1
        self.largeur = 0
        self.nbPicot = 0
        self.marqueMax = 0

        query = QSqlQuery()
        query.exec(f'SELECT MAX(timeNote) AS max FROM paragraph WHERE cleVideo={self.videoID}')
        if query.next():
            self.marqueMax = query.value('max')

        self.populateMarqueNote()

    def populateMarqueNote(self):
        self.listeMarques = []
        query = QSqlQuery()
        query.exec(f'SELECT timeNote FROM paragraph WHERE cleVideo={self.videoID} ORDER BY timeNote ASC')
        aux = -1
        while query.next():
            if aux != query.value('timeNote'):
                self.listeMarques.append(query.value('timeNote'))
            aux = query.value('timeNote')
        self.nbPicot = len(self.listeMarques)
        self.init_ui()
        self.resizeEvent(QResizeEvent(self.size(), self.size()))

    def evt_lblPlusmoins_clicked(self):
        if self.marqueCour == -1:
            return
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.videoID, self.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif(paragraphCour)
                formGererNote.show()

    def testMarque(self, x):
        if x >= 0:
            tps = int((x - 14) / self.width() * self.duration)
        else:
            tps = -x
            self.marqueCour = tps

        if int(tps) > int(self.marqueMax):
            tps = self.marqueMax - 3

        i = 0
        len0 = len(self.listeMarques)
        if tps <= self.listeMarques[0]:
            self.marqueCour = self.listeMarques[i]
            self.setLabel()
            self.majLblMarque()
            return self.listeMarques[0]
        for i in range(0, len0, 1):
            if tps >= self.listeMarques[i]:
                pass
            else:
                d1 = tps - self.listeMarques[i - 1]
                d2 = self.listeMarques[i] - tps
                if d1 > d2:
                    self.marqueCour = self.listeMarques[i]
                    self.setLabel()
                    self.majLblMarque()
                    return (self.listeMarques[i], self.marqueCour)
                else:
                    self.marqueCour = self.listeMarques[i - 1]
                    self.setLabel()
                    self.majLblMarque()
                    return self.listeMarques[i - 1]

    def majLblMarque(self):
        return
        if self.marqueCour == -1:
            aux = f'0/{self.nbPicot}'
        else:
            index = self.listeMarques.index(self.marqueCour) + 1
            aux = f'{index}/{self.nbPicot}'
        self.lblPlusMoins.setText(aux)

    def init_ui(self):
        self.setMinimumSize(1, 25)

    def evt_btnMoins_clicked(self):
        if self.marqueCour == -1:
            return
        index = self.listeMarques.index(self.marqueCour)
        if index == 0:
            self.marqueCour = -1
            self.setLabel()
            self.majLblMarque()
        else:
            index -= 1
            self.marqueCour = self.listeMarques[index]
            self.setLabel()
            self.majLblMarque()
            formScreen1.mediaPlayer.setPosition(self.marqueCour * 1000)

    def evt_btnPlus_clicked(self):
        if self.marqueCour == self.listeMarques[self.nbPicot - 1]:
            return
        else:
            if self.marqueCour == -1:
                self.marqueCour = 0
            else:
                index = self.listeMarques.index(self.marqueCour) + 1
                self.marqueCour = self.listeMarques[index]
            self.setLabel()
            self.majLblMarque()
            formScreen1.mediaPlayer.setPosition(self.marqueCour * 1000)

    def setLabel(self):
        if self.duration == 0:
            return
        self.clear()
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        for picot in self.listeMarques:
            x = int(self.largeur / self.duration * picot)
            point = QPoint(x - 6, 5)
            if self.marqueCour == picot:
                image = QPixmap('ressources/picot1.png')
            else:
                image = QPixmap('ressources/picot.png')
            painter.drawPixmap(point, image)
        self.setPixmap(pixmap)
        painter.end()

    def resizeEvent(self, e):
        if not self._flag:
            self._flag = True
            self.setLabel()
            QTimer.singleShot(50, lambda: setattr(self, "_flag", False))
        self.largeur = self.width()
        super().resizeEvent(e)
        self.setLabel()




#  ************************************************************************************************************
#  ************************************************************************************************************
#  *************    C A D R E  G R I D  V I G N E T T E     ***************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class CadreGridVignette(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1326, 700)
        self.setStyleSheet('background-color: #222222')

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        #  Zone gauche
        self.widgetLeft = QWidget()
        self.widgetLeft.setStyleSheet('border: 1px solid #333')
        self.lytLeft = QVBoxLayout()
        self.grpLeft = QGroupBox()
        self.grpLeft.setStyleSheet('border: 0px')
        self.lytLeft.addWidget(self.grpLeft)
        self.widgetLeft.setLayout(self.lytLeft)
        mainLayout.addWidget(self.widgetLeft, 0)
        self.lytLeft.setSpacing(0)

        #  Zone Droite
        self.widgetRight = QWidget()
        self.widgetRight.setStyleSheet('border: 2px solid #333')
        self.lytRight = QVBoxLayout()
        self.grpRight = QGroupBox()
        self.grpRight.setStyleSheet('border: 0px')
        self.lytRight.addWidget(self.grpRight)
        self.widgetRight.setLayout(self.lytRight)
        mainLayout.addWidget(self.widgetRight)

        #  Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.widgetLeft)
        splitter.addWidget(self.widgetRight)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        splitter.setSizes([180, 480])

        mainLayout.addWidget(splitter)


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************     S E L E C T Z O N E D R O I T        ***************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class SelectZoneDroit(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.vignetteWidth = 0
        self.lstVideoSelect = []
        self.lstVignette = []
        self.vignetteCour = None
        self.nbRangs = 5

        self.populateLstVideoSelect()
        self.initUI()

    def initUI(self):
        self.resize(640, 400)
        # Créer un QScrollArea
        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vBox = QGridLayout()

        #  Chargement du contenu
        self.lstVignette = []
        #  Initialisation des indices de la double boucle
        lenListVideo = len(self.lstVideoSelect)
        indexRang = lenListVideo // self.parent.nbColonnes
        indexCour = 0
        for i in range(0, indexRang + 1):
            for j in range(0, self.parent.nbColonnes):
                indexCour += 1
                if indexCour <= lenListVideo:
                    # ****************************************************************
                    #  VIGNETTE
                    # ****************************************************************
                    #  Contenant
                    cle = self.lstVideoSelect[indexCour - 1]
                    videoCour = VideoFileRecord(cle)
                    #
                    #  Image vignette
                    vidcap = cv2.VideoCapture(videoCour.videoPath)
                    query = QSqlQuery()
                    query.exec(f'SELECT timeNote FROM paragraph WHERE cleVideo={videoCour.cle} AND icone={True}')
                    timeCodeIconeAux = 0
                    if query.next():
                        timeCodeIconeAux = query.value('timeNote')
                    if videoCour.timeCodeIcone == 0:
                        timeCodeIconeAux = 228
                    vidcap.set(cv2.CAP_PROP_POS_MSEC, timeCodeIconeAux * 1000)
                    success, image = vidcap.read()
                    try:
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    except:
                        pass
                    pixmap01 = None

                    w = self.width()
                    w = int(w / self.nbRangs)
                    h = int(w * 0.74)

                    if success:
                        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                        pixmap01 = QPixmap.fromImage(image).scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    object = QLabel()
                    object = LabelIndex(self, cle, pixmap01, i, j)
                    # object.installEventFilter(self)
                    object.setStyleSheet('background-color: #222; border: 1px solid #666; padding: 10')
                    self.vBox.addWidget(object, i, j)
                    self.lytObject = QVBoxLayout()
                    #  Info vidéo
                    lblInfo = QLabel(object)
                    duree = self.strTime(self.videoDuration(videoCour.videoPath))
                    auxHTML = f'<p><FONT color="#ffffff" size=4 face="calibri">{videoCour.videoName}</B></FONT>' \
                              f'<FONT color="#aaaaaa" size=3 face="arial"><br>Durée: {duree}</FONT></p>'
                    lblInfo.setText(auxHTML)
                    lblInfo.setAlignment(Qt.AlignTop)
                    lblInfo.setStyleSheet('background-color: #222')
                    lblInfo.setWordWrap(True)
                    lblInfo.move(5, 358)
                    #  Pastille
                    lblPastille = QLabel(lblInfo)
                    lblPastille.setFixedSize(20, 20)
                    lblPastille.setStyleSheet('background-color: transparent')
                    lblPastille.move(0, 0)
                    pastille = PastilleSimple(lblPastille, 8, videoCour.colorStatut)
                    pastille.move(0, 0)
                    pastille.setToolTip(videoCour.nomStatut)
                    pastille.setStyleSheet(
                        "QToolTip { color: #ffffff; background-color: #555; border: 1px solid #555555; }")

                    self.lstVignette.append((object, object.lblImage, lblInfo))

        self.widget.setLayout(self.vBox)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)
        self.show()
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        self.scrollArea.setStyleSheet(style)
        self.setStyleSheet('background-color: #222222; border: 0px')

        # #  label qui remplacera la vignette pour un déplacement vers un
        # #  autre dossier. Il est utilisé par la classe LabelIndex
        # self.lblFantome = QLabel(self)
        # #  Préparation du lblFantom en cas de drag and drop sur un dossier
        # self.lblFantome.setFixedSize(100, 100)
        # self.lblFantome.setStyleSheet('background-color: red')
        # self.lblFantome.move(100, 100)
        # self.lblFantome.setVisible(False)
        # self.lblFantome.setAlignment(Qt.AlignCenter)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._dragging = True
    #         self._drag_offset = event.pos()
    #         event.accept()
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     if self._dragging == True:
    #         new_pos = self.mapToParent(event.pos() - self._drag_offset)
    #         self.move(new_pos)
    #         event.accept()
    #
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         event.accept()
    #     else:
    #         event.ignore()
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._dragging = False


    
    # def eventFilter(self, object, event):
        # if self == object:
        # if event.type() == QEvent.MouseButtonPress:
        #     self._dragging = True
        # if event.type() == QEvent.Enter:
        #     return True
        # elif event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton:
        #     self._dragging = True
        #     return True
        # elif event.type() == QEvent.MouseMove and self._dragging:
        #     new_pos = self.mapToParent(event.pos() - self._drag_offset)
        #     self.move(new_pos)
        #     return  True
        # return super().eventFilter(object, event)

    def onResize(self):
        w = 0
        for obj in self.lstVignette:
            object, lblImage, lblInfo = obj
            w = self.width()
            w = int(w / self.parent.nbColonnes) - 20
            h = int(w * 0.7)
            object.setFixedSize(w, w + 20)
            object.lblImage.setFixedSize(w, h)
            lblInfo.setStyleSheet('border: 0px')
            lblInfo.setFixedSize(w, 120)
            lblInfo.move(0, h)
        self.vignetteWidth = w

    def resizeEvent(self, event):
        # Redéfinition de la méthode resizeEvent pour capturer l'événement de redimensionnement
        super().resizeEvent(event)
        self.onResize()

    def populateLstVideoSelect(self):

        self.lstVideoSelect = []
        if self.parent.selectZoneGauche.lblSavedSearch.boolSelect: #  Filtre du SavedSearch
            self.parent.selectZoneGauche.lblSavedSearch.boolSelect = False
            self.parent.selectZoneGauche.lblSavedSearch.setStyleSheet('QPushButton {background-color: transparent; '
                                                                      'border: 0px; color: #aaaaaa; '
                                                                      'text-align: left; padding-left: 0px;} '
                                                                      'QPushButton::hover{background-color: #444}')
            self.parent.mainWindowDossier.unSelectBtnSelect()
            self.parent.selectZoneGauche.unSelectTopLeft()
            listLine = self.parent.selectZoneGauche.formSavedSearch.cadreBuildSearch.listLineSavedSearch
            listSQL = []
            if len(listLine) > 0:
                listSQL, selectAux = self.buildLineSql(listLine)
                if len(listSQL) == 1: #  Requete à une ligne
                    auxRequete, champ = listSQL[0]
                    query = QSqlQuery()
                    query.exec(selectAux + auxRequete) # + ' GROUP BY videoFullPath')
                    while query.next():
                        aux = query.value('cle')
                        if aux in self.lstVideoSelect:
                            pass
                        else:
                            self.lstVideoSelect.append(aux)
                    #  Remettre le bouton saved search en position non activé
                    self.parent.selectZoneGauche.lblSavedSearch.setStyleSheet('QPushButton {background-color: transparent; '
                                                                              'border: 0px; color: #aaaaaa; '
                                       'text-align: left; padding-left: 0px;} '
                                       'QPushButton::hover{background-color: #444}')
                else:  #  Requete à plusieurs lignes
                    i = 0
                    requete = ''
                    for itm in listSQL:
                        auxRequete, champ = itm
                        requete += auxRequete
                        if i < len(listSQL) - 1:
                            requete += ' AND '
                        i += 1
                    query = QSqlQuery()
                    bOk = query.exec(selectAux + requete + ' GROUP BY videoFullPath')
                    while query.next():
                        aux = query.value('cle')
                        self.lstVideoSelect.append(aux)
        else:

            auxLeftTop = ''
            auxDossier = ''
            # 1->AllItems  -  2->Recents  -  3->Favoris  -  4->deleted
            if self.parent.leftTopSelectCour == -1 and self.parent.dossierSelectCour == -1:  # pas de critères de sélection
                self.lstVideoSelect = []
            if self.parent.leftTopSelectCour == 1:  # AllItems
                auxLeftTop = ' NOT deleted '
            if self.parent.leftTopSelectCour == 2:  # Recents
                auxLeftTop = ' LIMIT 7 ORDER BY DESC '
            if self.parent.leftTopSelectCour == 3:  # Favoris
                auxLeftTop = ' Favori '
            if self.parent.leftTopSelectCour == 4:  # Deleted
                auxLeftTop = ' deleted '

            if self.parent.dossierSelectCour > 0:  # un dossier sélectionné
                auxDossier = f' cleClasseur={self.parent.dossierSelectCour} AND NOT deleted '

            auxRequete = ''
            if auxLeftTop == '' and auxDossier != '':
                auxRequete = f'SELECT cle FROM videoFileTab WHERE {auxDossier}'
                query = QSqlQuery()
                query.exec(auxRequete)
                while query.next():
                    self.lstVideoSelect.append(query.value('cle'))

            if auxLeftTop != '' and auxDossier == '':
                auxRequete = f'SELECT cle FROM videoFileTab WHERE {auxLeftTop}'
                query = QSqlQuery()
                query.exec(auxRequete)
                while query.next():
                    self.lstVideoSelect.append(query.value('cle'))

            if auxLeftTop != '' and auxDossier != '':
                query = QSqlQuery()
                query.exec(auxRequete)
                while query.next():
                    self.lstVideoSelect.append(query.value('cle'))

        self.parent.selectZoneGauche.setCursor(Qt.WaitCursor)
        self.initUI()
        self.parent.selectZoneGauche.setCursor(Qt.ArrowCursor)

    def buildLineSql(self, listLine):
        # Contruction de fromAux et de jointureAux pour initialiser le selectAux
        lstchampAux = []
        for line in listLine:
            if line.cmbChamp.currentIndex() not in lstchampAux:
                lstchampAux.append(line.cmbChamp.currentIndex())
        selectAux = ''
        fromAux = ''
        jointureAux = ''
        i = 0

        for indice in lstchampAux:
            if self.parent.lstIndiceChampTab[indice] not in fromAux:
                fromAux += self.parent.lstIndiceChampTab[indice] + ", "
            if 'videoFileTab' not in fromAux:
                fromAux += 'videoFileTab, '

        for indice in lstchampAux:
            if self.parent.lstIndiceChampTab[indice] != 'videoFileTab':
                jointureAux += self.parent.lstIndiceChampTab[indice] + '.cleVideo=videoFileTab.cle AND '

        selectAux = 'SELECT videoFileTab.cle FROM ' + fromAux[:-2] + chr(32) + 'WHERE ' + jointureAux

        listSQL = []
        for line in listLine:
            indiceChamp = line.cmbChamp.currentIndex()
            if indiceChamp == 0:  # nom de la vidéo
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # égal à
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(videoName)=UPPER({chr(34)+lneValeurAux+chr(34)})', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # différent de
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(videoName)<>UPPER({chr(34)+lneValeurAux+chr(34)}) ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # contient
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(videoName) LIKE UPPER({chr(34)+"%"+lneValeurAux+"%"+chr(34)}) ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 3:  # ne contient pas
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(videoName) NOT LIKE UPPER({chr(34)+"%"+lneValeurAux+"%"+chr(34)}) ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 1:  # Dossier
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # est présent dans
                    lneValeurAux = line.cmbValeur.currentData()
                    aux = (f' cleClasseur={lneValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # est absent dans
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' cleClasseur<>{lneValeurAux} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 2:  # Favori
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # est favori
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' favori ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # n'est pas favori
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' NOT favori ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 3:  # Tag Paragraph ----> tagTab !!!!!!!!
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # égal à
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(tagTab.mot) = UPPER({chr(34)+lneValeurAux+chr(34)}) ', 'cleVideo')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # différent de
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(tagTab.nom) <> UPPER({chr(34)+lneValeurAux+chr(34)}) ', 'cleVideo')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # contient
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(tagTab.nom) LIKE UPPER({chr(34)+lneValeurAux+chr(34)}) ', 'cleVideo')
                    listSQL.append(aux)
                if indiceOperateur == 3:  # ne contient pas
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(tagTab.nom) NOT LIKE UPPER({chr(34)+lneValeurAux+chr(34)}) ', 'cleVideo')
            if indiceChamp == 4:  # Création, date d'entrée de la vidéo dans la base
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # égal à
                    dateAux = line.dateValeur.text()
                    annee, mois, jour = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateCreation = {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # avant
                    dateAux = line.dateValeur.text()
                    annee, mois, jour = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateCreation <= {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # après
                    dateAux = line.dateValeur.text()
                    annee, mois, jour = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateCreation >= {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 5:  # Duration
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # Moins que
                    timeValeurAux = line.timeValeur.value()
                    aux = (f' duration < {timeValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # Plus que
                    timeValeurAux = line.timeValeur.value()
                    aux = (f' duration > {timeValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # Egal à
                    timeValeurAux = line.timeValeur.value()
                    aux = (f' duration = {timeValeurAux} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 6:  # Rating
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # plus que
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' note > {lneValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # moins que
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' note < {lneValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # égal à
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' note = {lneValeurAux} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 7:  # lastView - Dernier visionnage
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # avant
                    dateAux = line.dateValeur.text()
                    annee, mois, jour = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateLastView <= {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # après
                    dateAux = line.dateValeur.text()
                    jour, mois, annee = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateLastView > {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 2:  # égal
                    dateAux = line.dateValeur.text()
                    annee, mois, jour = map(int, dateAux.split('/'))
                    if mois < 10:
                        mois = '0' + str(mois)
                    if jour < 10:
                        jour = '0' + str(jour)
                    dateAux = f'{annee}-{mois}-{jour}'
                    aux = (f' dateLastView = {chr(34) + dateAux + chr(34)} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 8:  # Statut Label
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # est présent dans
                    # lneValeurAux = line.cmbValeur.currentData()
                    lneValeurAux = line.indiceValeur
                    aux = (f' cleClasseur={lneValeurAux} ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # est absent dans
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' statut<>{lneValeurAux} ', 'cle')
                    listSQL.append(aux)
            if indiceChamp == 9:  # Note
                indiceOperateur = line.cmbOperateur.currentIndex()
                if indiceOperateur == 0:  # est présent dans
                    lneValeurAux = line.lneValeur.text()
                    aux = (f' UPPER(Texte) LIKE UPPER({chr(34)+"%"+lneValeurAux+"%"+chr(34)}) ', 'cle')
                    listSQL.append(aux)
                if indiceOperateur == 1:  # est absent dans
                    lneValeurAux = line.cmbValeur.currentIndex()
                    aux = (f' UPPER(videoName) NOT LIKE UPPER({chr(34)+"%"+lneValeurAux+"%"+chr(34)}) ', 'cle')
                    listSQL.append(aux)
        return listSQL, selectAux

    def videoDuration(self, video):
        v = cv2.VideoCapture(video)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = 1
        try:
            duration = frame_count / fps
        except:
            duration = 1

        v.release()
        heureTxt = '00'
        if duration > 3600:
            heure = int(duration / 3600)
            duration = duration - (3600 * heure)
            if heure < 10:
                heureTxt = f'0{heure}'

        minute = int(duration / 60)
        if minute < 10:
            minuteTxt = f'0{minute}'
        else:
            minuteTxt = f'{minute}'
        seconde = int((duration - minute * 60) * .6)
        if seconde < 10:
            secondeTxt = f'0{seconde}'
        else:
            secondeTxt = f'{seconde}'

        duree = f'{heureTxt}:{minuteTxt}:{secondeTxt}'
        return duration

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        strHeure, strMinute, strSeconde = '', '', ''
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************     B T N S E L E C T T O P              ***************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class BtnSelectTop(QPushButton):
    def __init__(self, parent, text=None, image=None, indiceBtn=None, boolMenu=None):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('QPushButton {background-color: transparent; border: 0px; color: #aaaaaa; '
                                       'text-align: left; padding-left: 0px;} '
                                       'QPushButton::hover{background-color: #444}')
        self.setFixedSize(250, 30)
        self.setText(text)
        self.installEventFilter(self)
        pixmap = QIcon(image)
        self.setIcon(pixmap)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.setFont(font)
        self.indiceBtn = indiceBtn
        self.boolSelect = False
        self.boolMenu = boolMenu

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton:
            if self.boolSelect:
                self.boolSelect = False
                self.setStyleSheet('QPushButton {background-color: transparent; border: 0px; color: #aaaaaa; '
                                   'text-align: left; padding-left: 0px;} '
                                   'QPushButton::hover{background-color: #444}')
            else:
                self.boolSelect = True
                self.setStyleSheet('QPushButton {background-color: #395da4; border: 0px; color: #aaaaaa; '
                                   'text-align: left; padding-left: 0px;} ')
                for btn in self.parent.listBtnSelectTop:
                    if self != btn:
                        btn.setSelected(False)
                self.parent.parent.leftTopSelectCour = self.indiceBtn
                self.parent.parent.boolExecuterSearch = False
                self.parent.parent.mainWindowDossier.unSelectBtnSelect()
                if self.parent.parent.selectZoneGauche.lblSavedSearch != self:
                    self.parent.parent.selectZoneDroit.populateLstVideoSelect()
        if event.type() == QEvent.ContextMenu:
            if self.boolMenu:
                menu = QMenu()
                menu.addAction(self._trad('Vider la corbeille', self.lngCourGlobal), self.viderCorbeille)
                if menu.exec_(event.globalPos()):
                    return True
        return QWidget.eventFilter(self, source, event)

    def viderCorbeille(self):
        self.dialog = DialogCustom()
        aux = 'Vous êtes en train de Supprimer les vidéos de la corbeille. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            query = QSqlQuery()
            query.exec(f'DELETE FROM videoFileTab WHERE deleted={True}')
            self.parent.parent.selectZoneDroit.populateLstVideoSelect()

    def setSelected(self, boolSelect):
        if not boolSelect:
            self.setStyleSheet('QPushButton {background-color: transparent; border: 0px; color: #aaaaaa; '
                               'text-align: left; padding-left: 0px;} '
                               'QPushButton::hover{background-color: #444}')
            self.boolSelect = False
        else:
            self.setStyleSheet('QPushButton {background-color: #395da4; border: 0px; color: #aaaaaa; '
                               'text-align: left; padding-left: 0px;} ')
            self.boolSelect = True



#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************     S E L E C T Z O N E G A U C H E      ***************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class SelectZoneGauche(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.parent = parent
        self.setFixedSize(300, 180)
        self.setStyleSheet('background-color: transparent; border: 0px; margin-top: 0')
        # self.setAcceptDrops(True)
        self.boolDeleted = False
        self.boolFavori = False
        self.boolRecent = False
        self.boolAllItems = False
        self._dragging = False
        # QTextEdit
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.listBtnSelectTop = []
        #  ***********************************************************************************************
        #  Bouton all items
        self.lblAllItems = BtnSelectTop(self, text=self._trad('   Toutes', self.lngCourGlobal),
                                        image='ressources/allItems1.png', indiceBtn=1,
                                        boolMenu=False)
        self.lblAllItems.move(0, 0)
        self.listBtnSelectTop.append(self.lblAllItems)
        self.lblAllItems.clicked.connect(self.evt_lblAllItems_clicked)
        #  ***********************************************************************************************
        #  Bouton Récents
        self.lblRecents = BtnSelectTop(self, text=self._trad('   Récents', self.lngCourGlobal),
                                       image='ressources/recents1.png', indiceBtn=2,
                                       boolMenu=False)
        self.lblRecents.move(0, 35)
        self.listBtnSelectTop.append(self.lblRecents)
        self.lblRecents.clicked.connect(self.evt_lblRecents_clicked)
        #  ***********************************************************************************************
        #  Bouton Favoris
        self.lblFavoris = BtnSelectTop(self, text=self._trad('   Favoris', self.lngCourGlobal),
                                       image='ressources/favoriGris.png', indiceBtn=3,
                                       boolMenu=False)
        self.lblFavoris.move(0, 70)
        self.listBtnSelectTop.append(self.lblFavoris)
        self.lblFavoris.clicked.connect(self.evt_lblFavoris_clicked)
        #  ***********************************************************************************************
        #  Bouton Deleted
        self.lblDeleted = BtnSelectTop(self, text=self._trad('   Corbeille', self.lngCourGlobal),
                                       image='ressources/poubelle.png', indiceBtn=4,
                                       boolMenu=True)
        self.lblDeleted.setAcceptDrops(True)
        self.lblDeleted.move(0, 105)
        self.listBtnSelectTop.append(self.lblDeleted)
        #  ***********************************************************************************************
        #  Saved Search
        self.lblSavedSearch = BtnSelectTop(self, text=self._trad('   Requètes sauvegardées', self.lngCourGlobal),
                                           image='ressources/savedSearch.png',
                                           indiceBtn=5, boolMenu=False)
        self.lblSavedSearch.move(0, 140)
        self.listBtnSelectTop.append(self.lblSavedSearch)
        self.lblSavedSearch.clicked.connect(self.evt_lblSavedSearch_clicked)
        #  ***********************************************************************************************
        #  Trait de séparation
        lblTrait = QLabel(self)
        lblTrait.resize(300, 1)
        lblTrait.setStyleSheet('background-color: #444; border: 1px solid #999')
        lblTrait.move(0, 175)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def evt_lblSavedSearch_clicked(self):
        self.formSavedSearch = FormSavedSearch(self, self.parent)
        self.formSavedSearch.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.pos()
        event.accept()

    def dragEnterEvent(self, event):
        pos = event.pos()
        self.posDel = [0, 105, 250, 135]
        x1, y1, x2, y2 = self.posDel[0], self.posDel[1], self.posDel[2], self.posDel[3]
        if pos.x() in range(x1, x2) and pos.y() in range(y1, y2):
            self.lblDeleted.setStyleSheet('background-color: transparent; border: 2px solid  #74d7fe; color: #aaaaaa; '
                                          'text-align: left;')
        event.accept()

    def dragLeaveEvent(self, event):
        self.lblDeleted.setStyleSheet('background-color: transparent; border: 0px solid  #74d7fe; color: #aaaaaa; '
                                      'text-align: left; ')

    def dropEvent(self, event):
        pos = event.pos()
        x1, y1, x2, y2 = self.posDel[0], self.posDel[1], self.posDel[2], self.posDel[3]
        if pos.x() in range(x1, x2) and pos.y() in range(y1, y2):
            self.lblDeleted.setStyleSheet('background-color: transparent; border: 0px solid  #74d7fe; color: #aaaaaa; '
                                          'text-align: left;')
        #  Mettre la vidéo dans la corbeille - mettre cleClasseur à -1
        cle = event.source().index
        query = QSqlQuery()
        tptData = (True)
        tplChamps = ('deleted')
        bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tptData} WHERE cle={cle}')
        self.parent.selectZoneDroit.populateLstVideoSelect()

    def unSelectTopLeft(self):
        self.boolAllItems = False
        self.parent.leftTopSelectCour = -1
        self.lblAllItems.setSelected(False)
        #
        self.boolRecent = False
        self.parent.leftTopSelectCour = -1
        self.lblRecents.setSelected(False)
        #
        self.boolFavori = False
        self.parent.leftTopSelectCour = -1
        self.lblFavoris.setSelected(False)
        #
        self.boolDeleted = False
        self.parent.leftTopSelectCour = -1
        self.lblDeleted.setSelected(False)

    def evt_lblAllItems_clicked(self):
        self.parent.boolExecuterSearch = False
        self.parent.mainWindowDossier.unSelectBtnSelect()
        if self.boolAllItems:
            self.lblAllItems.setSelected(False)
            self.boolAllItems = False
            self.parent.leftTopSelectCour = -1
        else:
            self.lblAllItems.setSelected(False)
            self.boolAllItems = True
            self.parent.leftTopSelectCour = 1

        self.lblRecents.setSelected(False)
        self.boolRecent = False

        self.lblFavoris.setSelected(False)
        self.boolFavori = False

        self.lblDeleted.setSelected(False)
        self.boolDeleted = False
        self.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_lblRecents_clicked(self):
        self.parent.boolExecuterSearch = False
        self.parent.mainWindowDossier.unSelectBtnSelect()

        self.lblAllItems.setSelected(False)
        self.boolAllItems = False

        if self.boolRecent:
            self.lblRecents.setSelected(False)
            self.boolRecent = False
            self.parent.leftTopSelectCour = -1
        else:
            self.lblRecents.setSelected(True)
            self.boolRecent = True
            self.parent.leftTopSelectCour = 2

        self.lblFavoris.setSelected(False)
        self.boolFavori = False

        self.lblDeleted.setSelected(False)
        self.boolDeleted = False
        self.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_lblFavoris_clicked(self):
        self.parent.boolExecuterSearch = False
        self.lblSavedSearch.setSelected(False)
        self.parent.mainWindowDossier.unSelectBtnSelect()

        self.lblAllItems.setSelected(False)
        self.boolAllItems = False

        self.lblRecents.setSelected(False)
        self.boolRecent = False
        if self.boolFavori:

            self.boolFavori = False
            self.lblFavoris.setSelected(False)
            self.parent.leftTopSelectCour = -1
        else:

            self.lblFavoris.setSelected(True)

            self.boolFavori = True
            self.parent.leftTopSelectCour = 3

        self.lblDeleted.setSelected(False)
        self.boolDeleted = False

        self.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_lblDeleted_clicked(self):
        self.parent.boolExecuterSearch = False
        self.parent.mainWindowDossier.unSelectBtnSelect()

        self.lblAllItems.setSelected(False)
        self.boolAllItems = False

        self.lblRecents.setSelected(False)
        self.boolRecent = False

        self.lblFavoris.setSelected(False)
        self.boolFavori = False
        if self.boolDeleted:
            self.lblDeleted.setSelected(False)
            self.boolDeleted = False
            self.parent.leftTopSelectCour = -1
        else:
            self.lblDeleted.setSelected(True)
            self.boolDeleted = True
            self.parent.leftTopSelectCour = 4
        self.parent.selectZoneDroit.populateLstVideoSelect()


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************  F O R M P R E F E R E N C E S V I D E O ***************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class FormPreferencesVideo(MainWindowCustom):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setGeometry(200, 100, 910, 580)
        self.setBtnMax(False)
        self.setBtnMini(False)
        self.colorLabel = ''
        self.cleBiBlioCour = -1
        self.nomBiblioCour = ''

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        # Titre
        lblPreferences = QLabel(self)
        lblPreferences.setText(self._trad('Préférences', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(20)
        font.setBold(True)
        lblPreferences.setFont(font)
        lblPreferences.setStyleSheet('background-color: transparent; color: #f05a24')
        lblPreferences.setFixedSize(250, 75)
        lblPreferences.move(20, 40)
        self.lstMenu = []
        self.styleEnbled = 'QPushButton {background-color: #222222; color: #cccccc; text-align:left} ' \
                           'QPushButton::hover{background-color: #222222}'
        self.styleDesabled = 'QPushButton {background-color: transparent; color: #cccccc; text-align:left} ' \
                             'QPushButton::hover{background-color: #222222}'

        # #  Menu Bibliotthèque
        # self.btnBiblio = QPushButton(self)
        # self.btnBiblio.setText('Bibliothèques')
        # font1 = QFont()
        # font1.setFamily('Arial')
        # font1.setPointSize(12)
        # font1.setBold(False)
        # self.btnBiblio.setFont(font1)
        # self.btnBiblio.setStyleSheet(self.styleDesabled)
        # self.btnBiblio.setFixedSize(250, 35)
        # self.btnBiblio.move(20, 100)
        # self.btnBiblio.clicked.connect(self.evt_btnBiblio_clicked)
        # self.lstMenu.append(self.btnBiblio)

        #  Menu Langues
        self.btnLangues = QPushButton(self)
        self.btnLangues.setText(self._trad('Langues', self.lngCourGlobal))
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnLangues.setFont(font1)
        self.btnLangues.setStyleSheet(self.styleDesabled)
        self.btnLangues.setFixedSize(250, 35)
        self.btnLangues.move(20, 135)
        self.btnLangues.clicked.connect(self.evt_btnLangues_clicked)
        self.lstMenu.append(self.btnLangues)

        #  Menu Paramètres video
        self.btnParametres = QPushButton(self)
        self.btnParametres.setText(self._trad('Paramètres vidéo', self.lngCourGlobal))
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnParametres.setFont(font1)
        self.btnParametres.setStyleSheet(self.styleDesabled)
        self.btnParametres.setFixedSize(250, 35)
        self.btnParametres.move(20, 170)
        self.btnParametres.clicked.connect(self.evt_btnParametres_clicked)
        self.lstMenu.append(self.btnParametres)

        #  Menu Thèmes
        self.btnThemes = QPushButton(self)
        self.btnThemes.setText(self._trad('Thèmes', self.lngCourGlobal))
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnThemes.setFont(font1)
        self.btnThemes.setStyleSheet(self.styleDesabled)
        self.btnThemes.setFixedSize(250, 35)
        self.btnThemes.move(20, 205)
        self.btnThemes.clicked.connect(self.evt_btnThemes_clicked)
        self.lstMenu.append(self.btnThemes)

        #  Menu RangeVignettes
        self.btnRangeVignettes = QPushButton(self)
        self.btnRangeVignettes.setText(self._trad('Rangement vignettes', self.lngCourGlobal))
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnRangeVignettes.setFont(font1)
        self.btnRangeVignettes.setStyleSheet(self.styleDesabled)
        self.btnRangeVignettes.setFixedSize(250, 35)
        self.btnRangeVignettes.move(20, 240)
        self.btnRangeVignettes.clicked.connect(self.evt_btnVignettes_clicked)
        self.lstMenu.append(self.btnRangeVignettes)

        #  Construire infoGeneUI
        # self.biblioUI()
        #  Construire choix des langues
        self.languesUI()
        #  Construire parametres Vidéo
        self.parametresUI()
        #  Construire Thèmes
        self.themesUI()
        #  Construire rangement des vignettes
        self.rangeVignetteUI()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    # def evt_btnBiblio_clicked(self):
    #     for itm in self.lstMenu:
    #         if itm.text() == 'Bibliothèques':
    #             itm.setStyleSheet(self.styleEnbled)
    #         else:
    #             itm.setStyleSheet(self.styleDesabled)
    #     self.cadreBiblio.setVisible(True)
    #     self.cadreLangues.setVisible(False)
    #     self.cadreParametres.setVisible(False)
    #     self.cadreThemes.setVisible(False)
    #     self.cadreVignettes.setVisible(False)

    def evt_btnLangues_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Langues':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        # self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(True)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(False)
        self.cadreVignettes.setVisible(False)

    def evt_btnParametres_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Paramètres vidéo':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        # self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(True)
        self.cadreThemes.setVisible(False)
        self.cadreVignettes.setVisible(False)

    def evt_btnThemes_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Thèmes':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        # self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(True)
        self.cadreVignettes.setVisible(False)

    def evt_btnVignettes_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Rangement vignettes':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        # self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(False)
        self.cadreVignettes.setVisible(True)

    def languesUI(self):
        self.cadreLangues = QGroupBox(self)
        self.cadreLangues.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreLangues.setFixedSize(640, 440)
        self.cadreLangues.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreLangues)
        lblTitre.setText(self._trad('Choix de la langue', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 15)

        # Langue courante
        self.lblLangueCourant = QLabel(self.cadreLangues)
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab WHERE cle={1}')
        if query.next():
            self.lblLangueCourant.setText(query.value('langue'))
            font = QFont()
            font.setFamily('Arial')
            font.setPointSize(11)
            self.lblLangueCourant.setStyleSheet('color: #f05a24')
            font.setBold(True)
            self.lblLangueCourant.setFixedWidth(250)
            self.lblLangueCourant.setFont(font)
            self.lblLangueCourant.move(20, 50)

        #  Bouton d'administration des langues
        self.btnAdmiValid1 = QPushButton(self.cadreLangues)
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiValid1.setFixedSize(39, 39)
        self.btnAdmiValid1.setIconSize(QSize(33, 33))
        self.btnAdmiValid1.move(10, 80)
        self.btnAdmiValid1.setCursor(Qt.PointingHandCursor)
        self.btnAdmiValid1.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiValid1.clicked.connect(self.evt_btnAdmiValid1_clicked)

        #  GroupBox des langues
        grpLstLangues = QGroupBox(self.cadreLangues)
        grpLstLangues.setFixedSize(260, 300)
        grpLstLangues.move(10, 130)
        grpLstLangues.setStyleSheet('background-color: #222222; border: 0px')
        # grpLstLangues
        lyt = QVBoxLayout()
        grpLstLangues.setLayout(lyt)
        # Liste des bibliothèques
        self.lstLangues = QListWidget()
        self.lstLangues.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lstLanguesIndex = -1
        self.cleLanguesTemp = -1
        self.nomLanguesTemp = ''
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lstLangues.setFont(font)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.lstLangues.setStyleSheet(style)
        lyt.addWidget(self.lstLangues)
        self.lstLangues.itemClicked.connect(self.evt_lstLangues_currentItemChanged)
        self.populateLstLangues()

        # # *********************************************************************************************
        # #  Cadre Aide
        # # *********************************************************************************************
        # self.grpCadreAide1 = QGroupBox(self.cadreLangues)
        # self.grpCadreAide.setFixedSize(340, 400)
        # self.grpCadreAide.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        # self.grpCadreAide1.move(280, 20)
        # #  Titre Aide1
        # font = QFont()
        # font.setFamily('Arial')
        # font.setPointSize(12)
        # font.setBold(True)
        # lblAide1 = QLabel(self.grpCadreAide1)
        # lblAide1.setFont(font)
        # lblAide1.setText('Aide')
        # lblAide1.setStyleSheet('color: #F05A24; border: 0px')
        # lblAide1.move(20, 25)
        # # textAide
        # font = QFont()
        # font.setFamily('Arial')
        # font.setPointSize(10)
        # font.setBold(False)
        # font.setItalic(True)
        # lblTextAide1 = QLabel(self.grpCadreAide1)
        # lblTextAide1.setWordWrap(True)
        # lblTextAide1.setFixedSize(300, 75)
        # lblTextAide1.setStyleSheet('background-color: #222222; color: #777777; border: 0px')
        # aux = "Le choix d'une nouvelle langue permet de traduire l'application. "
        # lblTextAide1.setText(aux)
        # lblTextAide1.setFont(font)
        # lblTextAide1.move(20, 60)
        #
        # self.cadreLangues.setVisible(False)

    def parametresUI(self):
        self.cadreParametres = QGroupBox(self)
        self.cadreParametres.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreParametres.setFixedSize(640, 440)
        self.cadreParametres.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreParametres)
        lblTitre.setText(self._trad('Paramètres de la vidéo', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 5)

        # Lecture vidéo
        self.lblLectureVideo = QLabel(self.cadreParametres)
        self.lblLectureVideo.setText(self._trad('Lecture vidéo', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        self.lblLectureVideo.setStyleSheet('color: white')
        font.setBold(True)
        self.lblLectureVideo.setFixedWidth(150)
        self.lblLectureVideo.setFont(font)
        self.lblLectureVideo.move(20, 60)
        #
        self.boutonOffOn = BoutonOffOn(self.cadreParametres)
        self.boutonOffOn.setBackGround('#333333')
        self.boutonOffOn.setPos(200, 55)
        query = QSqlQuery()
        query.exec(f'SELECT videoOn FROM parametersTab WHERE cle={1}')
        if query.next():
            self.boutonOffOn.initBool(query.value('videoOn'))
        #
        lblLecture = QLabel(self.cadreParametres)
        lblLecture.setStyleSheet('color: gray')
        lblLecture.setFixedSize(250, 50)
        lblLecture.setText(self._trad('La video démarre automatiquement au lancement', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        lblLecture.setFont(font)
        lblLecture.setWordWrap(True)
        lblLecture.move(330, 45)
        # Son
        self.lblLectureSon = QLabel(self.cadreParametres)
        self.lblLectureSon.setText(self._trad('Son', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        self.lblLectureSon.setStyleSheet('color: white')
        font.setBold(True)
        self.lblLectureSon.setFixedWidth(150)
        self.lblLectureSon.setFont(font)
        self.lblLectureSon.move(20, 110)
        #
        self.boutonOffOn1 = BoutonOffOn(self.cadreParametres)
        self.boutonOffOn1.setBackGround('#333333')
        self.boutonOffOn1.setPos(200, 105)
        query = QSqlQuery()
        query.exec(f'SELECT soundOn FROM parametersTab WHERE cle={1}')
        if query.next():
            self.boutonOffOn1.initBool(query.value('soundOn'))
        #
        lblSon = QLabel(self.cadreParametres)
        lblSon.setStyleSheet('color: gray')
        lblSon.setFixedSize(250, 50)
        lblSon.setText('La son est activé automatiquement au lancement')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        lblSon.setFont(font)
        lblSon.setWordWrap(True)
        lblSon.move(330, 95)

        self.cadreParametres.setVisible(False)

    def themesUI(self):
        self.cadreThemes = QGroupBox(self)
        self.cadreThemes.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreThemes.setFixedSize(640, 440)
        self.cadreThemes.move(250, 55)
        # titre
        lblTitre = QLabel(self.cadreThemes)
        lblTitre.setText(self._trad('Thèmes', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 5)
        # Thème courant
        self.lblThemeCourant = QLabel(self.cadreThemes)
        query = QSqlQuery()
        query.exec(f'SELECT theme FROM parametersTab WHERE cle={1}')
        if query.next():
            self.lblThemeCourant.setText(query.value('theme'))
            font = QFont()
            font.setFamily('Arial')
            font.setPointSize(11)
            self.lblThemeCourant.setStyleSheet('color: #f05a24')
            font.setBold(True)
            self.lblThemeCourant.setFixedWidth(250)
            self.lblThemeCourant.setFont(font)
            self.lblThemeCourant.move(20, 50)
        #  Bouton d'administration des thèmes
        self.btnAdmiValid2 = QPushButton(self.cadreThemes)
        self.btnAdmiValid2.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiValid2.setFixedSize(39, 39)
        self.btnAdmiValid2.setIconSize(QSize(33, 33))
        self.btnAdmiValid2.move(10, 80)
        self.btnAdmiValid2.setCursor(Qt.PointingHandCursor)
        self.btnAdmiValid2.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiValid2.clicked.connect(self.evt_btnAdmiValid2_clicked)
        #  GroupBox des themes
        grpLstThemes = QGroupBox(self.cadreThemes)
        grpLstThemes.setFixedSize(260, 300)
        grpLstThemes.move(10, 130)
        grpLstThemes.setStyleSheet('background-color: #222222; border: 0px')
        # grpLstThemes
        lyt = QVBoxLayout()
        grpLstThemes.setLayout(lyt)
        # Liste des bibliothèques
        self.lstThemes = QListWidget()
        self.lstThemes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lstThemesIndex = -1
        self.cleThemesTemp = -1
        self.nomThemesTemp = ''
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lstThemes.setFont(font)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.lstThemes.setStyleSheet(style)
        lyt.addWidget(self.lstThemes)
        self.lstThemes.itemClicked.connect(self.evt_lstThemes_currentItemChanged)
        self.populateLstThemes()

        self.cadreThemes.setVisible(False)

    def rangeVignetteUI(self):
        self.cadreVignettes = QGroupBox(self)
        self.cadreVignettes.setStyleSheet('background-color: #222; color: white; border: 0px')
        self.cadreVignettes.setFixedSize(640, 440)
        self.cadreVignettes.move(250, 55)
        # Titre
        lblTitre = QLabel(self.cadreVignettes)
        lblTitre.setText(self._trad('Rangement vignettes', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 5)
        #  Consigne
        lblConsigne = QLabel(self.cadreVignettes)
        lblConsigne.setStyleSheet('color: #999')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        font.setItalic(True)
        lblConsigne.setFont(font)
        lblConsigne.setText('Choisir le nombre de rangées de vignettes à afficher \ndans la grille.')
        lblConsigne.move(20, 60)
        #  Boutons
        self.lstBtnColonne = []
        for i in range(0, 9):
            btnColonne = QPushButton(self.cadreVignettes)
            btnColonne.setStyleSheet('border: 2px solid gray; border-radius: 7px')
            btnColonne.setFixedSize(35, 35)
            btnColonne.setText(str(i+1))
            btnColonne.move(50*i+20, 120)
            self.lstBtnColonne.append(btnColonne)
            btnColonne.clicked.connect(self.evt_btnColonne_clicked)
        self.lstBtnColonne[self.parent.nbColonnes - 1].setStyleSheet('border: 2px solid orange; border-radius: 7px')

    def evt_btnColonne_clicked(self):
        self.setCursor(Qt.WaitCursor)
        indice = int(self.sender().text())
        for btn in self.lstBtnColonne:
            if int(btn.text()) == indice:
                self.parent.nbColonnes = indice
                btn.setStyleSheet('border: 2px solid orange; border-radius: 7px')
                query = QSqlQuery()
                tptData = (indice, 'ok')
                tplChamps = ('nbColonnes', 'autre')
                bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tptData} WHERE cle={1}')
            else:
                btn.setStyleSheet('border: 2px solid gray; border-radius: 7px')
        self.parent.selectZoneDroit.populateLstVideoSelect()
        self.setCursor(Qt.ArrowCursor)



    def evt_btnAdmiValid_clicked(self):
        self.grpCadreAide.setVisible(True)
        if self.cleBiblioTemp == -1:
            return
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid1.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.dialog = DialogCustom(self, 100, 100)
        aux = self._trad('Vous êtes en train de sélectionner une nouvelle bibliothèque. '
                         '\nEtes-vous certain de votre choix ?', self.lngCourGlobal)
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte de la nouvelle bibliothèque
            indexCour = self.lstBiblio.currentItem().data(Qt.UserRole)
            nom = self.lstBiblio.currentItem().text()
            self.lblBiblioCourant.setText(nom)
            # self.videoRecordCour.nomClasseur = nom
            # self.videoRecordCour.cleClasseur = indexCour
        else:
            pass

        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.majBiblio()
        self.cleBiblioTemp = -1

    def evt_btnAdmiValid1_clicked(self):
        # self.grpCadreAide.setVisible(True)
        if self.cleLanguesTemp == -1:
            return
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid1.png'))
        # self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        # self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        # self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.dialog = DialogCustom(self, 100, 100)

        aux = self._trad('Vous êtes en train de sélectionner une nouvelle langue. Le logiciel va redémarrer.',
                         self.lngCourGlobal)
        self.dialog.setMessage(aux)
        self.dialog.setSaisie('', False)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte de la nouvelle langue
            indexCour = self.lstLangues.currentItem().data(Qt.UserRole)
            nom = self.lstLangues.currentItem().text()
            self.lblLangueCourant.setText(nom)
            query = QSqlQuery()
            tptData = ('ok', nom)
            tplChamps = ('autre', 'langue')
            bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tptData} '
                             f'WHERE cle={1}')
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            pass

        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.cleLanguesTemp = -1

    def evt_btnAdmiValid2_clicked(self):
        self.grpCadreAide.setVisible(True)
        if self.cleThemesTemp == -1:
            return
        self.btnAdmiValid2.setIcon(QIcon('ressources/admiValid1.png'))
        self.dialog = DialogCustom(self, 100, 100)
        aux = self._trad('Vous êtes en train de sélectionner un nouveau thème. '
                         '\nEtes-vous certain de votre choix ?', self.lngCourGlobal)
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte de la nouvelle langue
            indexCour = self.lstThemes.currentItem().data(Qt.UserRole)
            nom = self.lstThemes.currentItem().text()
            self.lblThemeCourant.setText(nom)
            query = QSqlQuery()
            tptData = ('ok', nom)
            tplChamps = ('autre', 'theme')
            bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tptData} '
                             f'WHERE cle={1}')
        else:
            pass
        self.btnAdmiValid2.setIcon(QIcon('ressources/admiValid.png'))
        self.cleThemesTemp = -1

    def evt_btnAdmiPlus_clicked(self):
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus1.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusBiblio.setVisible(True)
        self.boolModif = False

    def evt_btnAdmiModif_clicked(self):
        if self.cleBiblioTemp == -1:
            return
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusBiblio.setVisible(True)
        self.lblTitrePlusBiblio.setText('Modifier une bibliothèque')

        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif1.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTab WHERE cle={self.cleBiblioTemp}')
        if query.next():
            self.lneNom.setText(query.value('nom'))
            self.lblChemin.setText(query.value('path'))

    def evt_btnAdmiSuppr_clicked(self):
        if self.cleBiblioTemp == -1:
            return
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusBiblio.setVisible(True)
        self.lblTitrePlusBiblio.setText('Supprimer un classeur')
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr1.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTab WHERE cle={self.cleBiblioTemp}')
        if query.next():
            self.lneNom.setText(query.value('nom'))
            self.lblChemin.setText(query.value('commentaire'))
        self.btnSauverBiblio.setVisible(False)
        self.btnAnnulerBiblio.setVisible(False)

        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de supprimer une bibliothèque. \nEtes-vous certain de votre choix ?'
        self.dialog.setMessage(aux)
        self.dialog.setSaisie('', False)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Sppression de la bibliothèque
            indexCour = self.lstBiblio.currentItem().data(Qt.UserRole)
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM biblioTab WHERE cle = {indexCour}')
        else:
            pass
        self.btnSauverBiblio.setVisible(True)
        self.btnAnnulerBiblio.setVisible(True)
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.lneNom.setText('')
        self.lblChemin.setText('')
        self.grpCadrePlusBiblio.setVisible(False)
        self.grpCadreAide.setVisible(True)
        self.populateLstBiblio()
        self.cleBiblioTemp = -1

    def evt_btnAnnulerBiblio_clicked(self):
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide.setVisible(True)
        self.grpCadrePlusBiblio.setVisible(False)
        self.lneNom.setText('')
        self.lblChemin.setText('')
        self.grpCadrePlusBiblio.setVisible(False)
        self.cleBiblioTemp = -1
        self.grpCadreAide.setVisible(True)

    def populateLstBiblio(self):
        self.lstBiblio.clear()
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTab ORDER BY nom')
        while query.next():
            lbl = QLabel()
            lbl.setFixedSize(QSize(20, 17))
            lbl.setPixmap(QPixmap('ressources/dossier.png'))
            itemN = QListWidgetItem(self.lstBiblio)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(f'{query.value("nom")}')
            itemN.setData(Qt.UserRole, query.value('cle'))
            self.lstBiblio.addItem(itemN)
            # self.lstClasseur.setItemWidget(itemN, lbl)
        self.lstBiblio.setSpacing(4)

    def populateLstLangues(self):
        self.lstLangues.clear()
        lstAux = ['Français', 'Anglais', 'Allemand', 'Espagnol', 'Chinois', 'Coréen']
        i = 0
        for lng in lstAux:
            lbl = QLabel()
            lbl.setFixedSize(QSize(20, 17))
            lbl.setPixmap(QPixmap('ressources/dossier.png'))
            itemN = QListWidgetItem(self.lstLangues)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(lng)
            itemN.setData(Qt.UserRole, i)
            self.lstLangues.addItem(itemN)
            i += 1
            # self.lstClasseur.setItemWidget(itemN, lbl)
        self.lstLangues.setSpacing(4)

    def populateLstThemes(self):
        self.lstThemes.clear()
        lstAux = ['Sombre', 'Clair', 'Flashy', 'Design']
        i = 0
        for lng in lstAux:
            lbl = QLabel()
            lbl.setFixedSize(QSize(20, 17))
            lbl.setPixmap(QPixmap('ressources/dossier.png'))
            itemN = QListWidgetItem(self.lstThemes)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(lng)
            itemN.setData(Qt.UserRole, i)
            self.lstThemes.addItem(itemN)
            i += 1
            # self.lstClasseur.setItemWidget(itemN, lbl)
        self.lstThemes.setSpacing(4)

    def evt_btnParcourir_clicked(self):
        self.lblChemin.setText('')
        folder = QFileDialog.getExistingDirectory(self, 'Sélectionner la racine de la bibliothèque')
        if folder:
            racine = folder + '/'
            self.lblChemin.setText(racine)

    def evt_lstBiblio_currentItemChanged(self, current):
        try:
            self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
            self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
            self.cleBiblioTemp = current.data(Qt.UserRole)
            self.nomBiblioCour = current.text()
        except:
            pass

    def evt_lstLangues_currentItemChanged(self, current):
        try:
            self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
            self.cleLanguesTemp = current.data(Qt.UserRole)
            self.nomLanguesCour = current.text()
        except:
            pass

    def evt_lstThemes_currentItemChanged(self, current):
        try:
            self.btnAdmiValid2.setIcon(QIcon('ressources/admiValid.png'))
            self.cleThemesTemp = current.data(Qt.UserRole)
            self.nomThemesCour = current.text()
        except:
            pass

    def evt_btnSauverBiblio_clicked(self):
        if self.lneNom.text() == '' or self.lblChemin.text() == '':
            self.dialog = DialogCustom(self, 100, 100)
            aux = 'Saisie du nom et du chemin de la bibliothèque obligatoires.'
            self.dialog.setMessage(aux)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return

        if self.boolModif:
            query = QSqlQuery()
            tptData = (self.lneNom.text(), self.lblChemin.text())
            tplChamps = ('Nom', 'path')
            bOk = query.exec(f'UPDATE biblioTab SET {tplChamps} = {tptData} '
                             f'WHERE cle={self.cleBiblioTemp}')
        else:
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) FROM biblioTab')
            try:
                if query.next():
                    maxCle = query.value(0) + 1
            except:
                maxCle = 1
            query = QSqlQuery()
            tplChamps = ('cle', 'nom', 'path')
            tplData = (maxCle, self.lneNom.text(), self.lblChemin.text())
            query.exec(f'INSERT INTO biblioTab {tplChamps} VALUES {tplData}')
        self.populateLstBiblio()
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide.setVisible(True)
        self.grpCadrePlusBiblio.setVisible(False)
        self.lneNom.setText('')
        self.lblChemin.setText('')
        self.grpCadrePlusBiblio.setVisible(False)
        self.cleBiblioTemp = -1

    def majBiblio(self):
        self.setCursor(Qt.WaitCursor)
        mainWindow.cleBiblio = self.cleBiblioTemp
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTab WHERE cle = {self.cleBiblioTemp}')

        if query.next():
            mainWindow.racine = query.value('path')
            nomRacine = query.value('nom')

        query = QSqlQuery()
        tplChamps = ('cleRacine', 'autre')
        tplData = (self.cleBiblioTemp, 'ok')
        bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')

        lstVideo = []

        #  Première utilisation
        query1 = QSqlQuery()
        query1.exec(f'SELECT firstUse FROM parametersTab WHERE cle={1}')

        if query1.next():
            if query1.value('firstUse') == 1:
                QMessageBox.information(self, 'Première utilisation', "L'application va se fermer."
                                                                      "\nVeillez la redémarrer")
                query1 = QSqlQuery()
                tplChamps = ('firstUse', 'autre')
                tplData = (0, 'ok')
                bOk = query1.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')
                sys.exit()
            else:
                if mainWindow.cmbSortIndex == 0:  # recents
                    query = QSqlQuery()
                    query.exec(f'SELECT cle FROM videoFileTab WHERE cleBiblio={self.cleBiblioTemp} '
                               f'ORDER BY dateLastView DESC LIMIT {mainWindow.NbVideosRecentes}')
                    while query.next():
                        lstVideo.append(VideoFileRecord(query.value('cle')))
                if mainWindow.cmbSortIndex == 1:
                    query = QSqlQuery()
                    query.exec(f'SELECT cle FROM videoFileTab WHERE cleBiblio={self.cleBiblioTemp} '
                               f'AND favori')
                    while query.next():
                        lstVideo.append(VideoFileRecord(query.value('cle')))
                if mainWindow.cmbSortIndex == 2:
                    query = QSqlQuery()
                    query.exec(f'SELECT cle FROM videoFileTab WHERE cleBiblio={self.cleBiblioTemp}')
                    while query.next():
                        lstVideo.append(VideoFileRecord(query.value('cle')))

        mainWindow.displayGridWindow(lstVideo)
        mainWindow.setWindowTitle(f'Nom de la bibliothèque courante : {nomRacine}')
        self.unsetCursor()
        # self.close()Biblio

    def closeEvent(self, event):
        self.sauveModifParameters()

    def sauveModifParameters(self):
        #  enregistrement des données qui ont été modifiées dans videoFileTab
        query = QSqlQuery()
        tptData = (self.boutonOffOn.boolON, self.boutonOffOn1.boolON, self.lblThemeCourant.text())
        tplChamps = ('videoOn', 'soundOn', 'theme')
        bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tptData} WHERE cle={1}')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************  M O U S E C L I C K F I L T E R          ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MouseClickFilter(QObject):
    def eventFilter(self, obj, event):
        #  Intercepte les clicks de souris quelque soit le widget
        #  Nécessaire pour déplacer une vidéo de la ZoneDroite vers un autre dossier
        if event.type() == QEvent.MouseButtonPress:
            query = QSqlQuery()
            query.exec(f'SELECT flagPaste, videoPaste FROM parametersTab WHERE cle = 1')
            if query.next():
                flagPaste = query.value('flagPaste')
                videoPaste = query.value('videoPaste')
                if flagPaste == True and videoPaste != -1: #  cas d'un déplacement de vidéo en cours
                    query1 = QSqlQuery()
                    tplChamps = ('flagPaste', 'videoPaste')
                    tplData = (False, -1)
                    query.exec(f'UPDATE ParametersTab SET {tplChamps} = {tplData} WHERE cle = 1')
        self.restoreCursor()

        return super().eventFilter(obj, event)

    def changeCursor(self):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def restoreCursor(self):
        QApplication.restoreOverrideCursor()

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              __M A I N__                  ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

if __name__ == '__main__':
    def catch_exceptions(t, val, tb):
        QMessageBox.critical(None,
                             "An exception was raised",
                             "Exception type: {}".format(t))
        old_hook(t, val, tb)


    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    # mouseFilter = MouseClickFilter()
    # app.installEventFilter(mouseFilter)

    #  Création de la fenêtre principale
    global mainWindow
    mainWindow = MainWindow()
    #  **********************************************************************************************************
    # #  Récupération du paramètre NbVideosRecentes
    # query1 = QSqlQuery()
    # query1.exec(f'SELECT NbVideosRecentes FROM parametersTab')
    # NbVideosRecentes = 5
    # if query1.next():
    #     NbVideosRecentes = query1.value('NbVideosRecentes')
    # mainWindow.NbVideosRecentes = NbVideosRecentes
    # filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleBiblio={mainWindow.cleBiblio}'
    #
    # filtreSQLRecent = f' ORDER BY dateLastView DESC LIMIT {mainWindow.NbVideosRecentes}'
    # #
    # query = QSqlQuery()
    # query.exec(filtreSQL + filtreSQLRecent)
    # lstVideo = []
    # while query.next():
    #     lstVideo.append(VideoFileRecord(query.value('cle')))
    # #
    # listTempOnglet = []
    # mainWindow.filtreCour = (filtreSQL, listTempOnglet)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # mainWindow.displayGridWindow(lstVideo)
    #  **********************************************************************************************************

    mainWindow.show()
    sys.exit(app.exec_())

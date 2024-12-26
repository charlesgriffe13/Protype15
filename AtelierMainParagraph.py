import AtelierGridWindow
from AtelierMainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtSql import QSqlQuery
from AtelierGlobal import *
from AtelierClassCommun import ParagrapheRecord, FormBlockNote, LabelTag, BoutonIndex



# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        A T E L I E R   P A R A G R A P H           **************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class AtelierParagraph(QMainWindow):
    def __init__(self, parent, videoID):
        super().__init__()
        self.parent = parent
        self.setStyleSheet('background: #fff')
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
        # self.widget.setFixedHeight(150)
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
                    # aux = strTime(self.paragraphCour.timeNote)
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
                # tedNote.move(50, int(self.top))
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
                if query1.next():
                    cleBiblio = query1.value('cleBiblio')
                    internalPath = query1.value('internalPath')
                    videoName = query1.value('videoName')
                #  Recherche de la légende
                query = QSqlQuery()
                query.exec(f'SELECT texte FROM Paragraph WHERE timeNote={self.timeNoteCour} AND cleVideo={cleVideo} '
                           f'AND picture={True}')
                if query.next():
                    textLegende = query.value('texte')
                query2 = QSqlQuery()
                query2.exec(f'SELECT path FROM biblioTab WHERE cle={cleBiblio}')
                if query2.next():
                    pathBiblio = query2.value('path')
                videoPath = pathBiblio + internalPath + videoName
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
        dlgFullScreen = QWidget(self)
        dlgFullScreen.setWindowFlag(Qt.WindowMaximizeButtonHint)
        dlgFullScreen.showFullScreen()
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
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            img = self.extractPicture(videoPath, 700, 500, timeCode)
            qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            pixmap01 = QPixmap.fromImage(qimg)
            lblPicture.setPixmap(pixmap01)

    def evt_btnModif_clicked(self):
        sender = self.sender()
        timeCode = sender.timeCode
        cle = formScreen1.videoID
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={cle}')
        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
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
        super(MainParagraph, self).__init__()
        self.setupUi(self)
        # self.resize(700, 411)
        self.parent = parent
        self.videoID = videoID[0]
        self.mainWin = mainWin

        self.setStyleSheet('background-color: #111111; border: 0px')

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        #  ***************************************************************************
        #  Top Zone
        #  ***************************************************************************
        btnSize = QSize(32, 20)
        btnSizea = QSize(70, 20)
        btnSize1 = QSize(80, 20)
        btnSize2 = QSize(100, 25)
        #
        self.btnMarquePage = QPushButton(self._trad('Marque Page', self.lngCourGlobal), self)
        self.btnMarquePage.setIcon(QIcon('ressources/marquePage.png'))
        self.btnMarquePage.setFixedSize(btnSize2)
        self.btnMarquePage.move(10, 10)
        self.btnMarquePage.setStyleSheet('color: white')
        self.lytTop.addWidget(self.btnMarquePage)
        self.lytTop.addSpacing(50)
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
        self.btnRetour.clicked.connect(self.evt_btnRetour_clicked)

        #  ***************************************************************************
        #  Note Zone
        #  ***************************************************************************
        global objNote

        self.objNote = AtelierParagraph(self, self.videoID)

        self.lytNote.addWidget(self.objNote)
        self.repaint()
        self.unsetCursor()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

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
        pass

    def evt_btnRetour_clicked(self):
        pass


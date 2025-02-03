from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from AtelierDesign2022 import *
import sys

class MainWindowCustom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Masquer la barre de titre
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet('background-color: #333333')
        self.initUI_sys()
        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('c:/videoFinder/Atelier_Constructor/data/VideoLearnerX.db')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            pass

    def initUI_sys(self):
        self.boolMoveWindow = False
        self.mousePressed = False
        self.oldPos = None
        self.resizeCorner = None
        #  Barre de titre
        self.gpbTitre = QGroupBox(self)
        self.gpbTitre.setFixedSize(700, 35)
        self.gpbTitre.setStyleSheet('background-color: #3c3f41; border: 0px')
        self.gpbTitre.installEventFilter(self)
        self.lytTitre = QHBoxLayout()
        self.gpbTitre.setLayout(self.lytTitre)
        self.lytTitre.setContentsMargins(0, 0, 0, 0)
        #  Bouton mini
        self.btnMini = QPushButton(self.gpbTitre)
        self.btnMini.setFixedSize(58, 35)
        self.btnMini.setIcon(QIcon('ressources/titreMini.png'))
        self.btnMini.setIconSize(QSize(58, 35))
        self.btnMini.setStyleSheet('QPushButton:hover {background-color: #4f5254; color: white;}')
        self.btnMini.clicked.connect(self.miniWindow)
        #  Bouton max
        self.btnMax = QPushButton(self)
        self.btnMax.move(200, 200)
        self.btnMax.setFixedSize(58, 35)
        self.btnMax.setIcon(QIcon('ressources/titreNormal.png'))
        self.btnMax.setIconSize(QSize(58, 35))
        self.btnMax.setStyleSheet('QPushButton:hover {background-color: #4f5254; color: white;}')
        self.btnMax.clicked.connect(self.maxWindow)
        #  Bouton close
        self.btnClose = QPushButton(self.gpbTitre)
        self.btnClose.setFixedSize(58, 35)
        self.btnClose.setIcon(QIcon('ressources/titreClose.png'))
        self.btnClose.setIconSize(QSize(58, 35))
        self.btnClose.setStyleSheet('QPushButton:hover {background-color: #e81123; color: white;}')
        self.btnClose.clicked.connect(self.closeWindow)
        #  Menu
        combobox = QComboBox()
        combobox.addItem("Option 1")
        combobox.addItem("Option 2")
        combobox.addItem("Option 3")

        #
        # self.lytTitre.addWidget(combobox)
        self.lytTitre.addStretch()
        self.lytTitre.addWidget(self.btnMini)
        self.lytTitre.addWidget(self.btnMax)
        self.lytTitre.addWidget(self.btnClose)

        # Poignée de redimensionnement
        self.poignee = QLabel(self)
        self.poignee.setStyleSheet('background-color: orange')
        self.poignee.setFixedSize(15, 15)
        cursor = QCursor(Qt.SizeFDiagCursor)
        self.poignee.setCursor(cursor)

    def closeWindow(self):
        self.close()

    def miniWindow(self):
        self.showMinimized()

    def maxWindow(self):
        if self.isMaximized():
            self.showNormal()
            self.btnMax.setIcon(QIcon('ressources/titreNormal.png'))
        else:
            self.showMaximized()
            self.btnMax.setIcon(QIcon('ressources/titreMax.png'))

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            if source == self.gpbTitre:
                self.boolMoveWindow = True
        return QWidget.eventFilter(self, source, event)

    def resizeEvent(self, event):
        self.gpbTitre.setFixedWidth(self.width())
        w = self.width()
        w = max(w, 200)
        h = self.height()
        h = max(h, 200)
        self.setGeometry(self.x(), self.y(), w, h)
        self.poignee.setGeometry(w-15, h-15, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.boolMoveWindow:
            self.dragPos = event.globalPos()
            event.accept()
        else:
            self.mousePressed = True
            self.oldPos = event.globalPos()
            # Déterminer si la souris est dans un coin de la fenêtre
            if event.x() < 10 and event.y() < 10:
                self.resizeCorner = Qt.TopLeftCorner
            elif event.x() > self.width() - 10 and event.y() < 10:
                self.resizeCorner = Qt.TopRightCorner
            elif event.x() < 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomLeftCorner
            elif event.x() > self.width() - 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomRightCorner

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed = False
            self.oldPos = None
            self.resizeCorner = None
            self.boolMoveWindow = False
            self.unsetCursor()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.boolMoveWindow:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        else:
            delta = event.globalPos() - self.oldPos
            if self.resizeCorner == Qt.TopLeftCorner:
                self.setGeometry(self.x() + delta.x(), self.y() + delta.y(), self.width() - delta.x(),
                                 self.height() - delta.y())
            elif self.resizeCorner == Qt.TopRightCorner:
                self.setGeometry(self.x(), self.y() + delta.y(), self.width() + delta.x(), self.height() - delta.y())
            elif self.resizeCorner == Qt.BottomLeftCorner:
                self.setGeometry(self.x() + delta.x(), self.y(), self.width() - delta.x(), self.height() + delta.y())
            elif self.resizeCorner == Qt.BottomRightCorner:
                self.setGeometry(self.x(), self.y(), self.width() + delta.x(), self.height() + delta.y())
            self.oldPos = event.globalPos()

#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************  F O R M E D I T I O N V I D E O ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class FormEditionVideo(MainWindowCustom):
    def __init__(self, videoCour=None):
        super().__init__()
        self.setGeometry(100, 100, 900, 500)
        self.videoCour = videoCour
        self.videoRecordCour = VideoFileRecord(self.videoCour)
        # Titre
        lblClassement = QLabel(self)
        lblClassement.setText('Classement')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(20)
        font.setBold(True)
        lblClassement.setFont(font)
        lblClassement.setStyleSheet('background-color: #333333; color: #f05a24')
        lblClassement.setFixedSize(250, 75)
        lblClassement.move(20, 40)
        self.lstMenu = []
        self.styleEnbled = 'QPushButton {background-color: #222222; color: #cccccc; text-align:left} ' \
                           'QPushButton::hover{background-color: #222222}'
        self.styleDesabled = 'QPushButton {background-color: transparent; color: #cccccc; text-align:left} ' \
                           'QPushButton::hover{background-color: #222222}'

        #  Menu Informations générales
        self.btnInfoGene = QPushButton(self)
        self.btnInfoGene.setText('Informations générales')
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnInfoGene.setFont(font1)
        self.btnInfoGene.setStyleSheet(self.styleDesabled)
        self.btnInfoGene.setFixedSize(250, 35)
        self.btnInfoGene.move(20, 100)
        self.btnInfoGene.clicked.connect(self.evt_btnInfoGene_clicked)
        self.lstMenu.append(self.btnInfoGene)

        #  Menu Table des matières
        self.btnMatieres = QPushButton(self)
        self.btnMatieres.setText('Table des matières')
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnMatieres.setFont(font1)
        self.btnMatieres.setStyleSheet(self.styleDesabled)
        self.btnMatieres.setFixedSize(250, 35)
        self.btnMatieres.move(20, 135)
        self.btnMatieres.clicked.connect(self.evt_btnMatieres_clicked)
        self.lstMenu.append(self.btnInfoGene)

        #  Menu Tags
        self.btnTags = QPushButton(self)
        self.btnTags.setText('Tags')
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnTags.setFont(font1)
        self.btnTags.setStyleSheet(self.styleDesabled)
        self.btnTags.setFixedSize(250, 35)
        self.btnTags.move(20, 170)
        self.btnTags.clicked.connect(self.evt_btnTags_clicked)
        self.lstMenu.append(self.btnTags)

        #  Menu Classeurs
        self.btnClasseurs = QPushButton(self)
        self.btnClasseurs.setText('Classeurs')
        self.font1 = QFont()
        self.font1.setFamily('Arial')
        self.font1.setPointSize(10)
        self.font1.setBold(False)
        self.btnClasseurs.setFont(self.font1)
        self.btnClasseurs.setStyleSheet(self.styleDesabled)
        self.btnClasseurs.setFixedSize(250, 35)
        self.btnClasseurs.move(20, 205)
        self.btnClasseurs.clicked.connect(self.evt_btnClasseurs_clicked)
        self.lstMenu.append(self.btnClasseurs)

        #  Menu Labels
        self.btnLabels = QPushButton(self)
        self.btnLabels.setText('Labels')
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnLabels.setFont(font1)
        self.btnLabels.setStyleSheet(self.styleDesabled)
        self.btnLabels.setFixedSize(250, 35)
        self.btnLabels.move(20, 240)
        self.btnLabels.clicked.connect(self.evt_btnLabels_clicked)
        self.lstMenu.append(self.btnLabels)

        #  Construire infoGeneUI
        self.infoGeneUI()
        #  Construire tableMatiere
        self.tableMatiereUI()
        #  Construire tableMatiere
        self.tagUI()

    def evt_btnInfoGene_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Informations générales':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreInfoGene.setVisible(True)
        self.cadreTableMatiere.setVisible(False)


    def evt_btnMatieres_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Table des matières':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(True)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(False)

    def evt_btnTags_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Tags':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(False)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(True)

    def evt_btnClasseurs_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Classeurs':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)

    def evt_btnLabels_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Labels':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)

    def infoGeneUI(self):
        self.cadreInfoGene = QGroupBox(self)
        self.cadreInfoGene.setStyleSheet('background-color: #333333; color: white; border: 0px')
        self.cadreInfoGene.setFixedSize(600, 400)
        self.cadreInfoGene.move(300, 55)
        # titre
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setText('Informations générales')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(18)
        font.setBold(True)
        lblTitre.setFont(font)
        lblTitre.move(200, 45)
        # Statut titre
        lblStatut = QLabel(self.cadreInfoGene)
        lblStatut.setAlignment(Qt.AlignRight)
        lblStatut.setStyleSheet('color: #ffffff; background-color: #333333')
        lblStatut.setFixedWidth(180)
        lblStatut.setText('Statut de la vidéo')
        lblStatut.setFont(self.font1)
        lblStatut.move(2, 100)
        #  Statut combo
        self.cmbStatut = QComboBox(self.cadreInfoGene)
        f = open('styles/QComboBox.txt', 'r')
        style = f.read()
        styleQComboBox = style
        self.cmbStatut.setStyleSheet(styleQComboBox)
        self.cmbStatut.setFixedSize(310, 30)
        self.cmbStatut.move(200, 97)
        self.populateCmbStatut()
        self.cadreInfoGene.setVisible(False)
        #  lblTitre de la video
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setAlignment(Qt.AlignRight)
        lblTitre.setStyleSheet('color: #eeeeee; background-color: #333333')
        lblTitre.setFixedWidth(180)
        lblTitre.setText('Titre de la vidéo')
        lblTitre.setFont(self.font1)
        lblTitre.move(2, 144)
        #  lblTitre vidéo
        self.lblTitreVideo = QLabel(self.cadreInfoGene)
        self.lblTitreVideo.setText('titre de la vidéo')
        style = "color: white; background-color: #666666; border: 1px solid #455364; border-radius: 4px;"
        styleQLabel = style
        self.lblTitreVideo.setStyleSheet(styleQLabel)
        self.lblTitreVideo.setFixedSize(310, 30)
        self.lblTitreVideo.move(200, 140)
        if self.videoRecordCour.titreVideo == '':
            self.lblTitreVideo.setText(self.videoRecordCour.videoName)
        else:
            self.lblTitreVideo.setText(self.videoRecordCour.titreVideo)
        #  lblChemin
        lblChemin = QLabel(self.cadreInfoGene)
        lblChemin.setAlignment(Qt.AlignRight)
        lblChemin.setStyleSheet('color: #ffffff; background-color: transparent')
        lblChemin.setFixedWidth(180)
        lblChemin.setText('Chemin')
        lblChemin.setFont(self.font1)
        lblChemin.move(2, 188)
        #  lblChemin vidéo
        self.lblCheminVideo = QLabel(self.cadreInfoGene)
        self.lblCheminVideo.setFixedSize(310, 30)
        query = QSqlQuery()
        query.exec(f'SELECT path FROM biblioTab WHERE cle={self.videoRecordCour.cleBiblio}')
        aux = ''
        if query.next():
            aux = query.value('path')
        self.lblCheminVideo.setText(aux + self.videoRecordCour.internalPath)
        self.lblCheminVideo.setToolTip(aux + self.videoRecordCour.internalPath)
        self.pathVideo = aux + self.videoRecordCour.internalPath
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(8)
        font2.setItalic(True)
        self.lblCheminVideo.setFont(font2)
        self.lblCheminVideo.setStyleSheet('color: #888888')
        self.lblCheminVideo.move(210, 184)
        # lblDurée
        lblDuree = QLabel(self.cadreInfoGene)
        lblDuree.setAlignment(Qt.AlignRight)
        lblDuree.setStyleSheet('color: #ffffff; background-color: transparent')
        lblDuree.setFixedWidth(180)
        lblDuree.setText('Durée')
        lblDuree.setFont(self.font1)
        lblDuree.move(2, 232)
        #  Durée vidéo
        self.lblDureeVideo = QLabel(self.cadreInfoGene)
        self.lblDureeVideo.setFixedSize(310, 30)
        self.lblDureeVideo.setText(str(self.videoDuration(self.pathVideo + self.videoRecordCour.videoName)))
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblDureeVideo.setFont(font2)
        self.lblDureeVideo.setStyleSheet('color: #888888')
        self.lblDureeVideo.move(210, 228)
        # lblNom
        lblNom = QLabel(self.cadreInfoGene)
        lblNom.setAlignment(Qt.AlignRight)
        lblNom.setStyleSheet('color: #ffffff; background-color: transparent')
        lblNom.setFixedWidth(180)
        lblNom.setText('Nom du fichier')
        lblNom.setFont(self.font1)
        lblNom.move(2, 276)
        #  lblNom vidéo
        self.lblNomVideo = QLabel(self.cadreInfoGene)
        self.lblNomVideo.setFixedSize(310, 30)
        self.lblNomVideo.setText(self.videoRecordCour.videoName)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblNomVideo.setFont(font2)
        self.lblNomVideo.setStyleSheet('color: #888888')
        self.lblNomVideo.setToolTip(self.videoRecordCour.videoName)
        self.lblNomVideo.move(210, 272)
        # lblNote
        lblNote = QLabel(self.cadreInfoGene)
        lblNote.setAlignment(Qt.AlignRight)
        lblNote.setStyleSheet('color: #ffffff; background-color: transparent')
        lblNote.setFixedWidth(180)
        lblNote.setText('Note')
        lblNote.setFont(self.font1)
        lblNote.move(2, 320)
        #  lbl Note vidéo
        self.grpRating = QGroupBox(self.cadreInfoGene)
        self.lblNoteVideo = StarRating(3)
        self.grpRating.setFixedSize(250, 43)
        self.grpRating.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpRating.move(172, 295)
        lytRating = QVBoxLayout()
        lytRating.setSpacing(0)
        lytRating.addWidget(self.lblNoteVideo )
        self.grpRating.setLayout(lytRating)
        # lblFavori
        lblFavori = QLabel(self.cadreInfoGene)
        lblFavori.setAlignment(Qt.AlignRight)
        lblFavori.setStyleSheet('color: #ffffff; background-color: transparent')
        lblFavori.setFixedWidth(180)
        lblFavori.setText('Favori')
        lblFavori.setFont(self.font1)
        lblFavori.move(2, 364)
        #  lbl Favori vidéo
        self.grpFavori = QGroupBox(self.cadreInfoGene)
        self.lblFavoriVideo = WidgetFavori(boolFavori=True)
        self.grpFavori.setFixedSize(40, 40)
        self.grpFavori.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpFavori.move(205, 350)
        lytFavori = QVBoxLayout()
        lytFavori.setSpacing(0)
        lytFavori.addWidget(self.lblFavoriVideo)
        self.grpFavori.setLayout(lytFavori)

        self.cadreInfoGene.setVisible(False)

    def tableMatiereUI(self):
        self.cadreTableMatiere = QGroupBox(self)
        self.cadreTableMatiere.setStyleSheet('background-color: #333333; color: white; border: 0px')
        self.cadreTableMatiere.setFixedSize(550, 400)
        self.cadreTableMatiere.move(350, 55)
        # titre
        lblTitre = QLabel()
        lblTitre.setText('Table des matières')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(18)
        font.setBold(True)
        lblTitre.setFont(font)

        #  Mise en place du ScrollArea
        scrollArea = QScrollArea()
        widget = QWidget(self.cadreTableMatiere)
        widget.setStyleSheet('background-color: #333333')
        widget.setFixedSize(400, 400)
        widget.move(150, 100)
        lytTableMatiere = QVBoxLayout()
        #  Ajouter le contenu
        query = QSqlQuery()
        query.exec(f'SELECT texte FROM paragraph WHERE cleVideo={self.videoCour} AND titre ORDER BY timeNote')
        while query.next():
            lbl = QLabel(query.value('texte'))
            lbl.setFont(self.font1)
            lytTableMatiere.addWidget(lbl)

        #
        widget.setLayout(lytTableMatiere)
        scrollArea.setWidget(widget)
        scrollArea.setFixedSize(500, 300)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        scrollArea.setStyleSheet(styleQScrollBar)
        lytMain = QVBoxLayout()
        lytMain.addWidget(lblTitre)
        lytMain.addWidget(scrollArea)
        self.cadreTableMatiere.setLayout(lytMain)

        self.cadreTableMatiere.setVisible(False)

    def tagUI(self):

        self.cadreTag = QGroupBox(self)
        self.cadreTag.setStyleSheet('background-color: #333333; color: white; border: 0px')
        self.cadreTag.setFixedSize(600, 400)
        self.cadreTag.move(300, 55)
        # titre
        lblTitre = QLabel(self.cadreTag)
        lblTitre.setText('Tags')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(18)
        font.setBold(True)
        lblTitre.setFont(font)
        lblTitre.move(200, 45)
        #  Installation de GrpBoxMetazData
        lytTag = QVBoxLayout()
        self.cadreTag.setLayout(lytTag)
        grpBoxTag = GrpBoxMetaData(self.cadreTag, self.videoCour, lytTag)
        lytTag.addWidget(grpBoxTag)

        self.cadreTag.setVisible(False)

    def populateCmbStatut(self):
        statutCour = self.videoRecordCour.statut
        self.cmbStatut.clear()
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM statutTab ORDER BY nom')
        i = 0
        indexCour = 0
        while query.next():
            self.cmbStatut.addItem(query.value('nom'), query.value('cle'))
            lwi = QListWidgetItem(query.value('nom'))
            if query.value('cle') == statutCour:
                indexCour = i
            if query.value('defaut') == 1:
                lwi.setData(Qt.UserRole, (query.value('cle'), True))
                brush = QBrush(QColor('orange'))
                lwi.setForeground(brush)
            else:
                lwi.setData(Qt.UserRole, (query.value('cle'), False))
            i += 1
        self.cmbStatut.setCurrentIndex(indexCour)
            # self.listStatut.addItem(lwi)

    def videoDuration(self, video):
        v = cv2.VideoCapture(video)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
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

        duration = f'{heureTxt}:{minuteTxt}:{secondeTxt}'
        return duration


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************        S T A R R A T I N G       ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class StarRating(QGroupBox):
    def __init__(self, rating):
        super().__init__()
        self.setFixedSize(150, 35)
        self.setStyleSheet('background-color: #333333; border: 0px')
        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)
        self.rating = rating
        # self.parent = parent
        self.lstBtn = []
        self.initStarRating()

    def initStarRating(self):
        for i in range(0, 6):
            btn = QPushButton()
            if self.rating + 1 > i:
                btn.setIcon(QIcon('ressources/orangeStar.png'))
            else:
                btn.setIcon(QIcon('ressources/blackStar.png'))
            btn.setStyleSheet('QPushButton {background-color: transparent; border: 0px} '
                               'QPushButton:hover{background-color: #888888} QToolTip{color: white}')
            if i == 0:
                btn.setFixedSize(12, 25)
                btn.setIcon(QIcon(None))
            else:
                btn.setFixedSize(25, 25)
            btn.setToolTip(str(i))
            self.lyt.addWidget(btn)
            btn.clicked.connect(self.evt_btn_clicked)
            self.lstBtn.append(btn)

    def majRatingStar(self):
        i = 0
        for itm in self.lstBtn:
            if int(itm.toolTip()) == 0:
                pass
            else:
                if self.rating + 1 > int(itm.toolTip()):
                    pass
                    itm.setIcon(QIcon('ressources/orangeStar.png'))
                else:
                    pass
                    itm.setIcon(QIcon('ressources/blackStar.png'))

    def evt_btn_clicked(self):
        sender = self.sender()
        nbStar = int(sender.toolTip())
        self.rating = nbStar
        self.majRatingStar()


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************        W I D G E T F A V O R I       *******************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class WidgetFavori(QLabel):
    def __init__(self, boolFavori):
        super().__init__()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.boolFavori = boolFavori
        self.setFixedSize(25, 25)
        self.setStyleSheet('background-color: transparent')
        if self.boolFavori:
            self.setPixmap(QPixmap('ressources/favoriRouge'))
        else:
            self.setPixmap(QPixmap('ressources/favoriGris'))

    def mousePressEvent(self, event):
        self.boolFavori = not self.boolFavori
        if self.boolFavori:
            self.setPixmap(QPixmap('ressources/favoriRouge'))
        else:
            self.setPixmap(QPixmap('ressources/favoriGris'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FormEditionVideo(videoCour=184)
    window.show()
    sys.exit(app.exec_())

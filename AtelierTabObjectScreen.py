import AtelierGlobal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from AtelierGlobal import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlQuery
from AtelierClassCommun import VideoFileRecord
from AtelierClassCommun import FormBlockNote, ParagrapheRecord
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from AtelierMainParagraph import MainParagraph
import datetime
from datetime import datetime
import time
import sys
import cv2

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                P U S H O N G L E T             ******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class PushOnglet(QLabel):
    def __init__(self, parent=None, cleVideo=None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(131, 30)
        self.setAlignment(Qt.AlignTop)
        # self.styleDesabled = 'QLabel {background-color: #60798B; border-top-left-radius: 7px; padding: 0px; ' \
        #                      'border-top-right-radius: 7px; color: white; padding-left: 4px;} ' \
        #                      'QLabel::hover {background-color: #555555;} '
        self.styleDesabled = 'QLabel {background-color: #171717; padding: 0px; width= ' \
                        ' color: white; padding-left: 4px;} ' \
                        'QLabel::hover {background-color: #555555;} '
        self.styleEnabled = 'QLabel {background-color: #60798B; border-top-left-radius: 7px; padding: 0px; ' \
                        'border-top-right-radius: 7px; gray: white; padding-left: 4px; border: 2px solid red} ' \
                        'QLabel::hover {background-color: #555555} '

        self.checked = False
        self.setStyleSheet(self.styleDesabled)

        self.cleVideo = cleVideo

        videoCour = VideoFileRecord(self.cleVideo)
        if len(videoCour.titreVideo) > 11:
            self.setText(videoCour.titreVideo[:11] + '...')
            self.setToolTip(videoCour.titreVideo)
        else:
            self.setText('    ' + videoCour.titreVideo + '...')


        self.btnRemove = QPushButton(self)
        self.btnRemove.setFixedSize(25, 25)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        font.setBold(True)
        self.btnRemove.setFont(font)
        self.btnRemove.setText('X')
        self.btnRemove.setStyleSheet('QPushButton {background-color: #1f1f1f; color: #E0E1E3; border-radius: 4px; '
                                     'padding: 2px; outline: none; border: none} '
                                     'QPushButton::hover{color: red;}')
        # self.btnRemove.move(103, 0)
        self.btnRemove.move(0, 0)
        self.btnRemove.clicked.connect(mainWindow.removeTab)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.majCurrentOnglet(self.cleVideo)

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************               B A R O N G L E T           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BarOnglet(QWidget):
    def __init__(self, parent, lstVideoOnglet):
        super().__init__()
        self.setGeometry(100, 100, 100, 600)
        self.setGeometry(100, 100, mainWindow.width(), 600)
        # self.setStyleSheet('background-color: orange')
        self.lytMain = QVBoxLayout()
        self.setLayout(self.lytMain)
        self.lstVideoOnglet = lstVideoOnglet
        self.cleVideo = lstVideoOnglet[0]
        self.videoTabCle = lstVideoOnglet[0]
        self.parent = parent

        lytOnglet = QHBoxLayout()
        self.lytMain.addLayout(lytOnglet)
        self.lytMain.setSpacing(2)
        self.grpBoxOnglet = QGroupBox()
        self.grpBoxOnglet.setFixedHeight(30)
        self.grpBoxOnglet.setStyleSheet('border: 0px; background-color: #333333')
        lytOnglet.addWidget(self.grpBoxOnglet)
        lyt = QHBoxLayout()
        lyt.setSpacing(2)
        self.grpBoxOnglet.setLayout(lyt)

        self.styleDesabled = 'QLabel {background-color: #0a0a0a; padding: 0px; ' \
                             'color: #292929; padding-left: 4px;} ' \
                             'QLabel::hover {color: white}'
        self.styleEnabled = 'QLabel {background-color: #171717; padding: 0px; ' \
                            'color: white; padding-left: 4px; border: 0px solid 455364} ' \
                            'QLabel::hover {color: white}'

        self.createFormScreen1()

        self.lstOnglet = []
        for cle in lstVideoOnglet:
            pushOnglet = PushOnglet(self, cle)
            lyt.addWidget(pushOnglet)
            self.lstOnglet.append(pushOnglet)
        try:
            if self.btnPlus:
                pass
        except:
            self.btnPlus = QPushButton(self)
            self.btnPlus.setFixedSize(16, 30)
            self.btnPlus.setText('+')
            self.btnPlus.setStyleSheet('QPushButton {background-color: #ef5a24; color: #121212; '
                                         'padding: 2px; outline: none; border: none} QPushButton::hover{color: white;}')
            self.btnPlus.setFont(QFont('Arial', 20))
            lyt.addWidget(self.btnPlus)
            spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            lyt.addItem(spacerItem)

        self.btnPlus.clicked.connect(mainWindow.evt_btnPlusTab_clicked)

    def createFormScreen1(self):
        qwidget = QWidget()
        qwidget.setStyleSheet('background-color: orange')
        # global formScreen1
        self.formScreen1 = AtelierGlobal.formScreen1
        try:
            if AtelierGlobal.formScreen1:
                AtelierGlobal.formScreen1.close()
        except:
            formScreen1 = FormScreen1(qwidget, self.cleVideo, mainWindow)
            formScreen1.searchString = mainWindow.gridWindow.searchString
            self.lytMain.addWidget(formScreen1)

    def majCurrentOnglet(self, cleVideo):
        for onglet in self.lstOnglet:
            if onglet.cleVideo == cleVideo:
                onglet.setStyleSheet(self.styleEnabled)
                onglet.checked = True
                onglet.setFixedHeight(40)
                self.videoTabCle = cleVideo
                formScreen1.loadVideo(onglet.cleVideo)
                self.parent.mainParagraph.videoID = onglet.cleVideo
                self.parent.mainParagraph.loadNotes()
            else:
                onglet.setStyleSheet(self.styleDesabled)
                onglet.checked = False
                onglet.setFixedHeight(35)

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
            # formGererNote = FormGererNote(self, videoPath, self.videoID, self.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif(paragraphCour)
                # formGererNote.exec_()
                formGererNote.show()

    def testMarque(self, x):
        if x >= 0:
            tps = int((x - 14) / self.width() * self.duration)
        else:
            tps = -x
            self.marqueCour = tps

        if tps > self.marqueMax:
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
        # self.setStyleSheet('border-top: 1px solid gray')

        # mainWindow.actEtudeVideo.setEnabled(False)
        # mainWindow.actEtudeVideoAnnul.setEnabled(False)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        lytMain = QVBoxLayout(centralWidget)  # Layout principal
        #  ***************************************************************************
        #  Zone de titre
        #  ***************************************************************************
        #  Titre de la vidéo
        lytTitre = QHBoxLayout()
        lblTitre = QLabel('Titre complet de la vidéo affichée dans le player')
        lblTitre.setFixedHeight(30)
        lblTitre.setStyleSheet('background-color: transparent')
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
        lytMain.addWidget(self.videoWidget)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setVolume(30)
        #  ***************************************************************************
        #  Slider Zone
        #  ***************************************************************************
        # lytSliderMain = QVBoxLayout()
        lytSlider = QVBoxLayout()
        # lytSliderMain.addLayout(lytSlider)
        self.sldVideo = SliderTimeCode(self)
        lytSlider.addWidget(self.sldVideo)
        lytMain.addLayout(lytSlider)
        video = VideoFileRecord(self.videoID)
        v = cv2.VideoCapture(mainWindow.racine + video.internalPath + video.videoName)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        v.release()
        self.marqueNote = MarqueNote(self, self.videoID, duration)
        self.marqueNote.installEventFilter(self)
        lytSlider.addWidget(self.marqueNote)
        #  Widget pour naviguer entre les marques
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
        btnEditMarque.setText('Editer')
        btnEditMarque.setStyleSheet(styleQPushButton)
        btnEditMarque.setFixedSize(QSize(70, 24))
        btnEditMarque.move(20, 0)
        lytSlider.addWidget(lblNavigMarque)
        # lytSlider.setSpacing(0)

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
        # self.sldVolume.setStyleSheet('margin :1px')
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
        # pxVitesse = QPixmap('ressources/volume.png')
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
        # self.cmbVitesse.setStyleSheet('background-color: #5FACF2; color: black')
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
        self.lblFixeMarque.setText('Fixer la marque :')
        self.lblFixeMarque.move(150, 3)
        # lytMarquage.addWidget(self.lblFixeMarque)
        #
        self.btnMarque = QPushButton(lblNavigMarque)
        f = open('styles/QPushButton.txt', 'r')
        style = f.read()
        self.btnMarque.setStyleSheet(style)
        self.btnMarque.setText('--:--:--')
        # self.btnMarque.setStyleSheet('background-color: #666666; color: white')
        self.btnMarque.move(260, 3)
        self.btnMarque.setFixedSize(btnSize2)
        # lytSlider.addWidget(self.btnMarque)
        #
        self.btnMarqueRetour = QPushButton(lblNavigMarque)
        self.btnMarqueRetour.setText('Retour marque')
        self.btnMarqueRetour.setStyleSheet(style)
        self.btnMarqueRetour.setFixedSize(btnSize2)
        self.btnMarqueRetour.move(370, 3)
        # lytMarquage.addWidget(self.btnMarqueRetour)
        #
        self.btnCreerNote = QPushButton(lblNavigMarque)
        self.btnCreerNote.setText('Créer note')
        self.btnCreerNote.setStyleSheet(style)
        self.btnCreerNote.setFixedSize(btnSize2)
        self.btnCreerNote.move(480, 3)
        # lytMarquage.addWidget(self.btnCreerNote)
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

    def evt_btnEditMarque_clicked(self):
        if self.marqueNote.marqueCour == -1:
            return
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            # formGererNote = FormGererNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueNote.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif()
                # formGererNote.exec_()
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
            menu.addAction('Editer', self.editMarque)
            menu.addSeparator()
            menu.addAction('Aller à', self.allerMarque)
            if menu.exec_(event.globalPos()):
                return True
        return QWidget.eventFilter(self, source, event)

    def editMarque(self):
        self.marqueNote.testMarque(self.xCour)
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.videoID}')

        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            # formGererNote = FormGererNote(self, videoPath, self.videoID, self.marqueNote.marqueCour, False)
            query1 = QSqlQuery()
            query1.exec(f'SELECT cle FROM paragraph WHERE timeNote={self.marqueNote.marqueCour} '
                        f'AND clevideo ={self.videoID}')
            if query1.next():
                paragraphCour = ParagrapheRecord(query1.value('cle'))
                formGererNote.populateNoteModif(paragraphCour)

                # formGererNote.exec_()
                formGererNote.show()

    def allerMarque(self):
        self.marqueNote.testMarque(self.xCour)
        self.mediaPlayer.setPosition(self.marqueNote.marqueCour * 1000)

    def loadVideo(self, videoID):
        self.videoID = videoID
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={videoID}')
        if query.next():
            self.videoPath = mainWindow.racine + query.value('internalPath') + query.value('VideoName')
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
        # if marqueCour != 0:
        query = QSqlQuery()
        tplChamps = ('marquePage', 'DateLastView')
        d = datetime.now().strftime('%d/%m/%Y')
        tplData = (int(self.mediaPlayer.position() // 1000), d)
        bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle = {self.videoID}')
        # self.mediaPlayer.setMuted(True)
        # self.deleteLater()
        # event.accept()

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

    def evt_btnMarqueRetour_clicked(self):
        if self.btnMarque.text() == '--:--:--':
            return
        self.mediaPlayer.setPosition(self.marqueCour * 1000)

    def evt_btnCreerNote_clicked(self):
        if self.btnMarque.text() == '--:--:--':
            return
        boolCreer = True
        self.formCreerNote = FormBlockNote(self, self.videoPath, self.videoID, self.marqueCour, boolCreer)
        # self.formCreerNote = FormGererNote(self, self.videoPath, self.videoID, self.marqueCour, boolCreer)
        self.formCreerNote.show()

    def evt_sldVideo_sliderMoved(self, position):
        self.mediaPlayer.setPosition(position * 1000)

    def evt_btnFermer_clicked(self):
        self.parent.screen.close()
        self.parent.paragraph.close()

    # ****************************************************************************
    # ****************************************************************************
    # ****************************************************************************
    def handleError(self):
        QMessageBox.information(self, 'error', str(self.mediaPlayer.error()))


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************      T A B O B J E C T S C R E E N        ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class TabObjectScreen(QMainWindow):
    def __init__(self, parent, lstVideoOnglet):
        super(TabObjectScreen, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.parent = parent  # -> MainWindow
        self.mainWin = parent
        self.lstVideoOnglet = lstVideoOnglet


        #  S C R E E N
        self.barOnglet = BarOnglet(self, lstVideoOnglet)
        self.setCentralWidget(self.barOnglet)

        #   P A R A G R A P H
        self.docParagraph = QDockWidget('Paragraph', self)
        self.docParagraph.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.docParagraph.setFloating(False)
        # self.docParagraph.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.Wind)

        global mainParagraph
        self.mainParagraph = MainParagraph(self.docParagraph, lstVideoOnglet, self.mainWin)
        mainParagraph = self.mainParagraph
        self.docParagraph.setWidget(self.mainParagraph)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docParagraph)

        self.barOnglet.majCurrentOnglet(lstVideoOnglet[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = TabObjectScreen()
    mainWindow.show()
    sys.exit(app.exec_())
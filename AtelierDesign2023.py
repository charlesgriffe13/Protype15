import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
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
from MetaDataMP4 import GrpBoxMetaData11
import exiftool
import subprocess
import html


# *******************************************************************************************
#  Variables globales
# *******************************************************************************************


# *******************************************************************************************
#  Classes de Widgets Heritage
# *******************************************************************************************

# *********************************************************************************************************************
# ***************         T E X E D I T L I N K         ***************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TextEditLink(QTextEdit):
    def __init__(self, parent):
        super().__init__()

    def undoX(self):
        self.undo()

    def redoX(self):
        self.redo()

    def mouseReleaseEvent(self, e):
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
            QDesktopServices.openUrl(QUrl(self.anchor))
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              B O U T O N I N D E X               ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BoutonIndex(QPushButton):
    def __init__(self, parent=None, timeCode=None, videoID=None):
        super(BoutonIndex, self).__init__(parent)
        self.parent = parent
        self.timeCode = timeCode
        self.videoID = videoID
        # print(videoID, timeCode)

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              B O U T O N O F F O N               ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BoutonOffOn(QGroupBox):
    def __init__(self, parent=None):
        super(BoutonOffOn, self).__init__(parent)
        self.setStyleSheet('background-color: #222222; padding: 0, 0, 0, 0;border: 1px solid gray')
        self.setFixedSize(105, 32)
        self.button = QPushButton(self)
        self.button.setFixedSize(46, 26)
        self.button.move(2, 0)
        self.boolON = True
        self.button.setIconSize(QSize(46, 26))
        self.button.setStyleSheet('border: 1px; border-radius: 4px')
        self.button.clicked.connect(self.move_button)
        self.button.setCursor(Qt.PointingHandCursor)
        self.move_button()

    def initBool(self, boolValue):
        self.boolON = not boolValue
        self.move_button()

    def move_button(self):
        if self.boolON:
            self.boolON = False
            self.button.setIcon(QIcon('ressources/btnOFF.png'))
            self.button.move(55, 3)
        else:
            self.boolON = True
            self.button.setIcon(QIcon('ressources/btnON1.png'))
            self.button.move(4, 3)

    def setPos(self, x, y):
        self.move(x, y)

    def setBackGround(self, color):
        self.setStyleSheet(f'background-color: {color}; padding: 0, 0, 0, 0; ')

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             G R P B O X M E T A D A T A          ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class GrpBoxMetaData(QGroupBox):
    def __init__(self, parent, contenant, videoID, lytMain):
        super().__init__()
        self.setStyleSheet('background-color: #222222; margin: 0px')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(240)

        self.parent = parent
        self.contenant = contenant
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False
        self.indexCour = -1
        self.titreComment = ''
        self.listTag = []
        self.listTagSelect = []

        grpTop = QGroupBox()
        grpTop.setStyleSheet('background: transparent')
        grpTop.setFixedSize(600, 50)
        lytMain.addWidget(grpTop)

        #  Saisie du tag
        self.lneTag = QLineEdit(grpTop)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lneTag.setFont(font)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.lneTag.setStyleSheet('margin: 0px; color: white; background: #333333; border-radius: 6px')
        self.lneTag.setFixedSize(400, 35)
        self.lneTag.move(0, 1)
        # Bouton Plus
        self.btnAdmiPlus = QPushButton(grpTop)
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus.setFixedSize(39, 39)
        self.btnAdmiPlus.setIconSize(QSize(33, 33))
        self.btnAdmiPlus.move(410, 0)
        self.btnAdmiPlus.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus.clicked.connect(self.sauverTag)
        #  Bouton Modif
        self.btnAdmiModif = QPushButton(grpTop)
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif.setFixedSize(39, 39)
        self.btnAdmiModif.setIconSize(QSize(33, 33))
        self.btnAdmiModif.move(450, 0)
        self.btnAdmiModif.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif.clicked.connect(self.modifTag)
        #  Bouton Suppr
        self.btnAdmiSuppr = QPushButton(grpTop)
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr.setFixedSize(39, 39)
        self.btnAdmiSuppr.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr.move(490, 0)
        self.btnAdmiSuppr.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr.clicked.connect(self.effaceTag)

        self.grpBoxAffichTag = QGroupBox(self)
        self.grpBoxAffichTag.setStyleSheet('border: 0px; background: #222222')
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        self.grpBoxAffichTag.setFixedWidth(590)  # 590

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(self.grpBoxAffichTag)
        scroll.setWidgetResizable(True)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        scroll.setStyleSheet(styleQScrollBar)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        self.populateGrpBoxAffichTag()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            source.majEtatSelect()
            if source.boolSelect:
                self.listTagSelect.append(source.text())
            else:
                del self.listTagSelect[self.listTagSelect.index(source.text())]
        return super().eventFilter(source, event)

    def effaceTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = 'Pas de tag sélectionné.'
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.dialog = DialogCustom(self)
        aux = 'Vous êtes en train de supprimer les tags sélectionnés. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            for tagAux in self.listTagSelect:
                del self.listTag[self.listTag.index(tagAux)]
            self.listTagSelect = []
            self.majMetaData()
        else:
            pass


    def modifTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = 'Pas de tag sélectionné.'
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return
        if len(self.listTagSelect) > 1:
            self.dialog = DialogCustom(self, 0, 0)
            aux = "L'opération de modification ne s'applique\nqu'à un tag à la fois."
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.motCour = self.listTagSelect[0]
        self.indexCour = self.listTag.index(self.motCour)
        self.lneTag.setText(self.motCour)
        self.boolModif = True

    def majMetaData(self):
        aux = ''
        for tag in self.listTag:
            aux += tag + ','
        aux = aux[:-1]

        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            video = mainWindow.racine + query.value('internalPath') + query.value('VideoName')
        # with exiftool.ExifTool("exiftool.exe") as et:
        #     et.execute(f'-Comment={aux}', video)
        subprocess.run(["exiftool", f"-Comment={aux}".encode(), video])
        self.populateGrpBoxAffichTag()

    def sauverTag(self):
        mot = self.lneTag.text()
        if mot == '':
            return

        if mot in self.listTag and not self.boolModif:
            QMessageBox.information(self, 'Enregistrement annulé', 'Le tag existe déja pour cette vidéo.')
            return
        if self.boolModif:
            del self.listTagSelect[self.listTagSelect.index(self.listTag[self.indexCour])]
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

        self.listTag = []
        output = subprocess.check_output(["exiftool", "-Comment", video])
        output = str(output)
        try:
            cmt = output.split(':')[1][:-5]
            cmt = cmt.replace(chr(92), '')
            cmt = cmt.replace('xe9', 'é')
            cmt = cmt.replace('xe2', 'â')
            cmt = cmt.replace('xe8', 'è')
            cmt = cmt.replace('xe0', 'à')
            cmt = cmt.replace('xe7', 'ç')
            cmt = cmt.replace('xef', 'ï')
            cmt = cmt.replace('xee', 'î')
            cmt = cmt.replace('xea', 'ê')
            cmt = cmt.replace('xfc', 'ü')
            self.listTag = cmt.lstrip().split(',')
        except:
            pass

        if len(self.listTag) == 0:
            return
        ligne = 0
        # *********************************************************************************************
        # *********************************************************************************************
        i = 0
        continuerLigne = True
        largLigneTag = 0
        largeur = 550
        offSet = 28
        lenList = len(self.listTag)
        grpBox = QGroupBox()
        grpBox.setFixedHeight(1000)
        grpBox.setStyleSheet('border: 0px; background: #222222')
        self.lytAffichTag.addWidget(grpBox)
        nbLigne = 0
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(grpBox, self.listTag[i], '#666666')
                lblTag.installEventFilter(self)
                lblTag.setPosition(largLigneTag, nbLigne*30)
                largLigneTag += lblTag.width + offSet
                if i + 1 == lenList:
                    self.lytAffichTag.addWidget(grpBox)
                    continuerLigne = False
                    continuerColonne = False
                    lblTag.setPosition(largLigneTag-lblTag.width-offSet, nbLigne*30)
                else:
                    if largLigneTag > largeur-lblTag.width-offSet-20:
                        largLigneTag = 0
                        lblTag.close()
                        nbLigne += 1
                        i -= 1
                        continuerColonne = False
                i += 1
        # spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lytAffichTag.addItem(spacerItem)
        self.lneTag.setText('')
        return
        # *********************************************************************************************
        # *********************************************************************************************
        largLigneTag = 0
        largeur = 550
        offSet = 30
        lenList = len(self.listTag)
        grpBox = QGroupBox(self.grpBoxAffichTag)
        grpBox.setFixedSize(570, 750)
        grpBox.setStyleSheet('border: 0px; background: #222222')
        grpBox.move(0, 0)

        for tagAux in self.listTag:
            lblTag = LabelTag(grpBox, tagAux, '#666666')
            largLigneTagTemp = largLigneTag + lblTag.width + offSet
            if largLigneTagTemp < largeur:
                lblTag.setPosition(largLigneTag, ligne * 30 + 5)
                largLigneTag += lblTag.width + offSet
            else:
                ligne += 1
                largLigneTag = 0
                lblTag.setPosition(largLigneTag, ligne * 30 + 5)
                largLigneTag += lblTag.width + offSet

        self.lneTag.setText('')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                F R M P R E C S U I V           ******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FrmPrecSuiv(QFrame):
    def __init__(self, parent=None, listVideo=[]):
        super(FrmPrecSuiv, self).__init__()
        self.pageCour = 1
        self.nbPage = 0
        self.parent = parent
        self.listVideo = listVideo
        self.initUI()

    def initDataTab(self, liste):
        self.listVideo = liste

    def initUI(self):
        self.setFixedSize(QSize(120, 40))
        # self.setStyleSheet('background-color: #444b4b;')
        self.setStyleSheet('background-color: transparent;')
        lytPrecSuiv = QHBoxLayout(self)
        self.btnPrec = QPushButton()
        self.btnPrec.setIcon(QIcon('ressources/flecheGche.png'))
        self.btnPrec.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPrec.clicked.connect(self.evt_btnPrec_clicked)
        lytPrecSuiv.addWidget(self.btnPrec)
        self.lblPage = QLabel('')
        self.lblPage.setFixedSize(QSize(50, 20))
        self.lblPage.move(0, -3)
        # self.lblPage.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        lytPrecSuiv.addWidget(self.lblPage)
        self.btnSuiv = QPushButton()
        self.btnSuiv.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSuiv.setIcon(QIcon('ressources/flecheDte.png'))
        self.btnSuiv.clicked.connect(self.evt_btnSuiv_clicked)
        self.setVisible(False)
        lytPrecSuiv.addWidget(self.btnSuiv)

    def initPages(self, pageCour, nbPages):
        self.lblPage.setText(f'{pageCour}/{nbPages}')
        self.nbPage = nbPages

    def evt_btnPrec_clicked(self):
        self.btnPrec.setCursor(Qt.WaitCursor)
        if self.pageCour == 1:
            return
        else:
            self.pageCour -= 1
            self.parent.fillGridLayout()
        self.btnPrec.setCursor(Qt.PointingHandCursor)

    def evt_btnSuiv_clicked(self):
        self.btnSuiv.setCursor(Qt.WaitCursor)
        if self.pageCour == self.nbPage:
            return
        else:
            self.pageCour += 1
            self.parent.fillGridLayout()
        self.btnSuiv.setCursor(Qt.PointingHandCursor)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           N A V I G F I C H I E R S            ******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NavigFichiers(QMainWindow):
    def __init__(self, repertoire, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: #000000')

        self.resize(400, 600)
        self.setWindowTitle("Navigateur de fichiers")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # crée le modèle
        model = QFileSystemModel()
        model.setRootPath(repertoire)

        # Crée le QTreeView et intégre le modèle
        self.view = QTreeView()
        self.view.setModel(model)
        self.view.setRootIndex(model.index(repertoire))
        f = open('styles/QTreeView.txt', 'r')
        style = f.read()
        styleQTreeView = style
        self.view.setStyleSheet(styleQTreeView)

        # Police de caractères à utiliser
        font = QFont()
        font.setStyleHint(QFont.Monospace)
        self.view.setFont(font)

        # largeur de la colonne 0
        self.view.setColumnWidth(0, 350)

        # place le QTreeView dans la fenêtre
        self.setCentralWidget(QFrame())
        layout = QGridLayout()
        layout.addWidget(self.view, 0, 0)
        self.centralWidget().setLayout(layout)

        # Etablissement lien entre signal et méthode
        self.view.clicked.connect(self.clicligne)

    def clicligne(self):
        pass


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
        for i in range(1, 6):
            btn = QPushButton()
            if self.rating + 1 > i:
                btn.setIcon(QIcon('ressources/orangeStar.png'))
            else:
                btn.setIcon(QIcon('ressources/blackStar.png'))
            btn.setStyleSheet('QPushButton {background-color: transparent; border: 0px} '
                               'QPushButton:hover{background-color: #888888} QToolTip{color: white}')
            # if i == 0:
            #     btn.setFixedSize(12, 25)
            #     btn.setIcon(QIcon(None))
            # else:
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
        if nbStar == 1 and self.rating == 1:
            self.rating = 0
        else:
            self.rating = nbStar
        self.majRatingStar()

    def setBackgound(self, coulor):
        self.setStyleSheet(f'background-color: {coulor}')


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

    def setPosition(self, x, y):
        self.move(x, y)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            L A B E L I N D E X            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelIndex(QLabel):
    def __init__(self, parent, index, picture, ligne, colonne):
        QLabel.__init__(self, parent)
        self.index = index
        self.picture = picture
        self.ligne = ligne
        self.colonne = colonne
        self.boolOnglet = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.boolOnglet:
                self.boolOnglet = False
                self.setStyleSheet('border: 0px')
                # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = False
            else:
                self.boolOnglet = True
                self.setStyleSheet('border: 2px solid red')
                # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = True

    def mousePressEventMethod(self):
        if self.boolOnglet:
            self.boolOnglet = False
            self.setStyleSheet('border: 0px')
            # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = False
        else:
            self.boolOnglet = True
            self.setStyleSheet('border: 2px solid red')
            # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = True

    def mouseDoubleClickEvent(self, evt):
        if self.index == -1:
            return
        lstVideo = [self.index]
        mainWindow.displayTabWindow(lstVideo)

    def mouseDoubleClickMethod(self):
        if self.index == -1:
            return
        lstVideo = [self.index]
        mainWindow.displayTabWindow(lstVideo)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************          B U T T O N G R O U P            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ButtonGroup(QPushButton):
    def __init__(self, indexButton=0, etat=False):
        super(ButtonGroup, self).__init__()
        self.etat = etat
        self.indexButton = indexButton
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def initEtat(self):
        if self.etat:
            self.setStyleSheet("text-align: left; border: 2px solid orange;background-color: transparent; "
                               "margin-left: 8px")
        else:
            self.setStyleSheet("QPushButton { text-align: left; border: 0px solid orange; "
                               "background-color: transparent; margin-left: 8px}")

    def command(self):
        if not self.etat:
            self.etat = not self.etat
            self.setIcon(QIcon('ressources/favoriRouge.png'))
        else:
            self.etat = not self.etat
            self.setIcon(QIcon('ressources/favoriGris.png'))


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************          B U T T O N S W I T C H          ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ButtonSwitch(QPushButton):
    def __init__(self, parent=None, image1=None, image2=None, etat=False):
        super(ButtonSwitch, self).__init__()
        self.etat = etat
        self.image1 = image1
        self.image2 = image2
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.evt_self_clicked)
        self.parent = parent

    def evt_self_clicked(self):
        pass

    def command(self):
        if not self.etat:
            self.etat = not self.etat
            self.setIcon(QIcon('ressources/favoriRouge.png'))
        else:
            self.etat = not self.etat
            self.setIcon(QIcon('ressources/favoriGris.png'))


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           S C R O L L L A B E L           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        try:
            f = open("DarkStyle.txt", 'r')
            contenu = f.read()
            self.setStyleSheet(contenu)
        except:
            pass

        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)

        self.label = QLabel(content)
        # self.label.setStyleSheet('background-color:green')
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        content.setContentsMargins(0, 0, 0, 0)
        lay.setContentsMargins(0, 0, 0, 0)

        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           P A R A G R A P H R E C O R D           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ParagrapheRecord():
    def __init__(self, cle):
        self.cle = cle

        query = QSqlQuery()
        query.exec(f'SELECT * FROM paragraph WHERE cle={cle}')
        if query.next():
            self.timeNote = query.value('timeNote')
            self.indentation = query.value('indentation')
            self.titre = query.value('titre')
            self.picture = query.value('picture')
            self.texte = query.value('texte')
            self.icone = query.value('icone')
            self.cleLien = query.value('cleLien')
            self.cleVideo = query.value('cleVideo')
            self.note = query.value('note')
            self.hauteur = query.value('hauteur')
            self.largeur = query.value('largeur')
            self.icone = query.value('icone')
            self.boolModif = False
            self.lienWeb = query.value('lienWeb')

        # query = QSqlQuery()
        # query.exec(f'SELECT icone FROM paragraph WHERE cle=116')

    def __str__(self):
        aux = f'cle->{self.cle} - timeNote->{self.timeNote} - indentation->{self.indentation} - ' \
              f'titre->{self.titre} - picture->{self.picture} - texte->{self.texte} - ' \
              f'icone->{self.icone} - cleLien->{self.cleLien} - cleVideo->{self.cleVideo} - note->{self.note}'
        return aux


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           V I D E O R E C O R D           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class VideoFileRecord:
    def __init__(self, cle=0):
        self.cle = cle
        query = QSqlQuery()
        query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.cle}')
        self.timeCodeIcone = 0
        self.titreVideo = ''
        self.boolOnglet = False
        if query.next():
            self.cleClasseur = query.value('cleClasseur')
            self.ordreClasseur = query.value('ordreClasseur')
            self.videoName = query.value('videoName')
            self.videoPath = query.value('videoFullPath')
            self.marquePage = query.value('marquePage')
            self.dateLastView = query.value('dateLastView')
            self.statut = query.value('statut')
            self.nomClasseur = ''
            if self.cleClasseur > -1:
                query1 = QSqlQuery()
                query1.exec(f'SELECT nom FROM classeurTab WHERE cle={self.cleClasseur}')
                if query1.next():
                    self.nomClasseur = query1.value('nom')
            else:
                self.nomClasseur = 'Aucun classeur'
            self.nomStatut = ''
            if self.statut > -1:
                query1 = QSqlQuery()
                query1.exec(f'SELECT nom, color FROM statutTab WHERE cle={self.statut}')
                if query1.next():
                    self.nomStatut = query1.value('nom')
                    self.colorStatut = query1.value('color')
                else:
                    self.nomStatut = 'Aucun label'
                    self.colorStatut = ''
            # self.boolTag = boolTag
            self.Favori = query.value('Favori')
            self.internalPath = query.value('internalPath')
            self.cleBiblio = query.value('cleBiblio')
            self.note = query.value('note')
        self.ongletVideo = False

        # recherche présence de la video dans paragraph
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM paragraph WHERE cleVideo={self.cle} AND timeNote=0 AND Titre={True}')
        if query.next():
            self.boolTag = True
            self.titreVideo = query.value('texte')
            #  Recherche de la picture icone
            query1 = QSqlQuery()
            query1.exec(f'SELECT timeNote FROM paragraph WHERE cleVideo={self.cle} AND icone={True}')
            if query1.next():
                self.timeCodeIcone = query1.value('timeNote')
            else:
                self.timeCodeIcone = 10
        else:
            self.boolTag = False

    def __str__(self):
        aux = f'cle->{self.cle} - cleClasseur->{self.cleClasseur} - ordreClasseur->{self.ordreClasseur} - ' \
              f'viodeoName->{self.videoName} - videoPath->{self.videoPath} - marquePage->{self.marquePage} - ' \
              f'dateLastView->{self.dateLastView} - statut->{self.statut} - nomClasseur->{self.nomClasseur}' \
              f' - boolTag->{self.boolTag} - Favori->{self.Favori} - InternalPath->{self.internalPath}' \
              f' - cleBiblio->{self.cleBiblio} - ongletVideo->{self.ongletVideo} - timeCodeIcone->{self.timeCodeIcone}' \
              f' - titreVideo->{self.titreVideo}'
        return aux


# *******************************************************************************************
#  Classes de Modules
# *******************************************************************************************

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            M A I N W I N D O W            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setStyleSheet("QMainWindow::title {background-color: red;}")
        self.setGeometry(100, 60, 1326, 780)
        statusBar = QStatusBar(self)
        self.setStatusBar(statusBar)
        f = open('styles/statuBar.txt', 'r')
        style = f.read()
        styleQStatusBar = style
        statusBar.setStyleSheet(styleQStatusBar)

        lblVersion = QLabel('Version : 12.18')
        statusBar.addWidget(lblVersion)
        global fileAttenteVideo
        fileAttenteVideo = [(-1, -1)]
        self.btnGroupCour = -1
        self.boolSearch = False
        self.searchString = ''
        self.lstGridVideo = []
        self.lstVideo = []
        self.URLCour = None
        self.nbTab = 0
        self.filtreCour = None
        self.NbVideosRecentes = 5
        self.cmbSortIndex = 0

        f = open('styles/QMainWindow.txt', 'r')
        style = f.read()
        styleQMainWindow = style
        self.setStyleSheet(styleQMainWindow)

        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('c:/videoFinder/Atelier_Constructor/data/VideoLearnerX.db')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            # Remplacer les notes (Null) par 0
            query = QSqlQuery()
            query.exec('UPDATE videoFileTab SET note = 0 WHERE note IS NULL')

        #  ***********************************************
        #  Mise en place du menu principal
        #  ***********************************************
        f = open('styles/QMenuBar.txt', 'r')
        style = f.read()
        styleBarMenu = style

        barMenu = self.menuBar()
        barMenu.setStyleSheet(styleBarMenu)
        #
        menuPreferences = barMenu.addMenu("Préférences")

        menuItemAbout = QAction(QIcon('ressources/about.png'), 'About VideoFinder', self)
        menuItemAbout.setStatusTip('All about VideoFinder')
        menuItemAbout.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuPreferences.addAction(menuItemAbout)

        menuItemPreferences = QAction(QIcon('ressources/library.png'), 'Préférences', self)
        menuItemPreferences.setStatusTip('Paramétrer le logiciel')
        menuItemPreferences.triggered.connect(self.evt_actPreferences_clicked)
        menuPreferences.addAction(menuItemPreferences)

        # menuItemLanguage = QAction(QIcon('ressources/language.png'), 'language', self)
        # menuItemLanguage.setStatusTip('Language')
        # menuItemLanguage.triggered.connect(lambda: print("Menu item has been clicked!"))
        # menuPreferences.addAction(menuItemLanguage)
        #
        # menuItemPlayer = QAction(QIcon('ressources/player.png'), 'Players externes', self)
        # menuItemPlayer.setStatusTip('Language')
        # menuItemPlayer.triggered.connect(lambda: print("Menu item has been clicked!"))
        # menuPreferences.addAction(menuItemPlayer)
        #
        menuFile = barMenu.addMenu("File")

        menuAddVideo = QAction(QIcon('ressources/addVideo1.png'), 'Add video', self)
        menuAddVideo.setStatusTip('Add video')
        menuAddVideo.triggered.connect(self.evt_actAddVideo_clicked)
        menuFile.addAction(menuAddVideo)

        menuRankedVideo = QAction(QIcon('ressources/RankedVideo.png'), 'Ranked video', self)
        menuRankedVideo.setStatusTip('Ranked video')
        menuRankedVideo.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuFile.addAction(menuRankedVideo)

        menuStoreVideo = QAction(QIcon('ressources/storedVideo.png'), 'Store video', self)
        menuStoreVideo.setStatusTip('Store video')
        menuStoreVideo.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuFile.addAction(menuStoreVideo)
        #
        menuLabel = barMenu.addMenu("Labels")

        menuCreateLabel = QAction(QIcon('ressources/addVideo1.png'), 'Create Label', self)
        menuCreateLabel.setStatusTip('Create Label')
        menuCreateLabel.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuLabel.addAction(menuCreateLabel)

        menuRankedLabel = QAction(QIcon('ressources/addVideo1.png'), 'Ranked Label', self)
        menuRankedLabel.setStatusTip('Ranked Label')
        menuRankedLabel.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuLabel.addAction(menuRankedLabel)

        menuStoreLabel = QAction(QIcon('ressources/addVideo1.png'), 'Store Label', self)
        menuStoreLabel.setStatusTip('Store Label')
        menuStoreLabel.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuLabel.addAction(menuStoreLabel)
        #
        menuBlinders = barMenu.addMenu("Blinders")

        menuCreateBlinders = QAction(QIcon('ressources/addVideo1.png'), 'Create Blinders', self)
        menuCreateBlinders.setStatusTip('Create Blinders')
        menuCreateBlinders.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuBlinders.addAction(menuCreateBlinders)

        menuRankedBlinders = QAction(QIcon('ressources/addVideo1.png'), 'Ranked Blinders', self)
        menuRankedBlinders.setStatusTip('Ranked Blinders')
        menuRankedBlinders.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuBlinders.addAction(menuRankedBlinders)

        menuStoreBlinders = QAction(QIcon('ressources/addVideo1.png'), 'Store Blinders', self)
        menuStoreBlinders.setStatusTip('Store Blinders')
        menuStoreBlinders.triggered.connect(lambda: print("Menu item has been clicked!"))
        menuBlinders.addAction(menuStoreBlinders)

        #  Vérification de la racinee de la bibliothèque
        self.checkRacine()

    def checkRacine(self):
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM parametersTab')
        if query.next():
            if query.value('cleRacine') != -1:
                self.cleBiblio = query.value('cleRacine')
                query1 = QSqlQuery()
                bOk = query1.exec(f'SELECT * FROM biblioTab WHERE cle = {self.cleBiblio}')
                if query1.next():
                    self.setWindowTitle(f"Bibliothèqie courante : {query1.value('nom')}")
                    self.racine = query1.value('path')
            else:
                rep = QMessageBox.question(self, 'Pas de racine de la bibliothèque enregistrée',
                                           'voulez-vous la saisir maintenant ?')
                if rep == QMessageBox.Yes:
                    # self.evt_actBiblio_clicked()
                    formBiblio = FormBiblio(self)
                    formBiblio.show()
                    formBiblio.exec_()
                else:
                    sys.exit()
        else:
            rep = QMessageBox.question(self, 'Pas de racine de la bibliothèque enregistrée',
                                       'voulez-vous la saisir maintenant ?')
            if rep == QMessageBox.Yes:
                self.evt_actBiblio_clicked()
            else:
                exit()

    def closeEvent(self, event):
        # Suppression des tags avec la clé de Note provisoire (-99)
        query = QSqlQuery()
        bOK = query.exec(f'DELETE FROM tagTab WHERE cleParagraph = -99')
        # maj du champ DateLastView dans la base
        try:
            if formScreen1:
                formScreen1.closeEvent(event)
        except:
            pass

    def evt_actEtudeVideo_clicked(self):
        L1 = [itm for itm in self.gridWindow.lstGridVideo if itm.boolOnglet == True]

        for itm in L1:
            try:
                nbTab = self.tabWidget.count() + 1
                # videoAux = [video for video in self.lstVideo if video.cle == cleVideo][0]
                self.tabObjetScreen = TabObjectScreen(self, itm.cle)
                self.tabWidget.addTab(self.tabObjetScreen, f'{itm.videoName}')
            except:
                # videoAux = [video for video in self.lstVideo if video.cle == cleVideo][0]
                self.tabWidget = QTabWidget()
                self.setCentralWidget(self.tabWidget)
                # f = open('styles/QTabWidget.txt', 'r')
                # style = f.read()
                # styleQTabWidget = style
                # self.tabWidget.setStyleSheet(styleQTabWidget)

                # self.tabWidget.setStyleSheet('QTabBar::tab {width: 125px; height: 25}')
                self.tabWidget.setTabsClosable(True)
                self.tabWidget.tabCloseRequested.connect(self.removeTab)
                nbTab = self.tabWidget.count() + 1
                self.tabObjetScreen = TabObjectScreen(self, itm.cle)
                self.tabWidget.addTab(self.tabObjetScreen, f'{itm.videoName}')
            try:
                if self.btnPlusTab:
                    self.btnPlusTab.close()
            except:
                pass
            self.btnPlusTab = QPushButton(self.tabWidget)
            self.btnPlusTab.setFixedSize(QSize(35, 35))
            self.btnPlusTab.setText('+')
            self.btnPlusTab.move((135*nbTab+3), 0)
            self.btnPlusTab.setFont(QFont('Arial', 15))

            self.btnPlusTab.clicked.connect(self.evt_actGrilleVideo_clicked)

    def evt_actEtudeVideoAnnul_clicked(self):
        mainWindow.actEtudeVideo.setEnabled(False)
        mainWindow.actEtudeVideoAnnul.setEnabled(False)
        # mainWindow.lstOngletVideo = []
        for itm in self.gridWindow.lstVideo:
            itm.ongletVideo = False
        self.gridWindow.fillGridLayout()

    def evt_actStatut_clicked(self):
        formStatut = FormStatut(self)
        formStatut.show()
        formStatut.exec_()

    def evt_actPreferences_clicked(self):
        # formBiblio = FormBiblio(self)
        # formBiblio.show()
        # formBiblio.exec_()
        try:
            self.gridWindow.formEditionVideo.close()
        except:
            pass
        self.formPreferencesVideo = FormPreferencesVideo()
        self.formPreferencesVideo.show()

    def evt_actParametres_clicked(self):
        formParameters = FormParameters(self)
        formParameters.show()
        formParameters.exec_()

    def evt_actClasseurVideo_clicked(self):
        formClasseur = FormClasseur(self)
        formClasseur.show()
        formClasseur.exec_()

    def evt_actGrilleVideo_clicked(self):
        if formScreen1:
            formScreen1.mediaPlayer.stop()
        try:
            if not self.tabObjetScreen:
                pass
        except:
            return
        if self.tabObjetScreen.cleVideo:
            videoID = self.tabObjetScreen.cleVideo
            query = QSqlQuery()
            tplChamps = ('marquePage', 'DateLastView')
            d = datetime.now().strftime('%d/%m/%Y')
            tplData = (0, d)
            bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle = {videoID}')
        try:
            self.tabWidget.close()
            self.displayGridWindow()
        except:
            pass

    def evt_actAddVideo_clicked(self):
        # try:
        #     self.formListVideo.close()
        # except:
        #     pass
        # #  Recherche du classeur par defaut
        # query1 = QSqlQuery()
        # query1.exec(f'SELECT cle from classeurTab WHERE defaut={True}')
        # if query1.next():
        #     cleClasseurDefaut = query1.value('cle')
        # #  Recherche du statut par defaut
        # query1 = QSqlQuery()
        # query1.exec(f'SELECT cle from statutTab WHERE defaut={True}')
        # if query1.next():
        #     cleStatutDefaut = query1.value('cle')

        file, b = QFileDialog.getOpenFileName(self, 'Enregistrer une nouvelle vidéo', self.racine, '*.mp4')
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
                return
            # #  Rechercher le numéro d'ordre suivant dans le classeur par défaut
            # query2 = QSqlQuery()
            # # cleClasseurDefaut = 1
            # bOk = query2.exec(f'SELECT ordreClasseur FROM videoFileTab WHERE '
            #                   f'cleClasseur={cleClasseurDefaut}')
            # maxOrdre = 0
            # while query2.next():
            #     aux = query2.value('ordreClasseur')
            #     if aux > maxOrdre:
            #         maxOrdre = aux
            # maxOrdre += 1
            #  Enregistrer la video dans videoFileTab
            queryCle = QSqlQuery()
            #  Recherche de l'indice suivant pour la primary key
            bOK = queryCle.exec('SELECT MAX(cle) FROM paragraph')
            maxCleParagraph = 1
            try:
                if bOK:
                    while queryCle.next():
                        maxCleParagraph = queryCle.value(0) + 1
            except:
                pass

            tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'ordreClasseur', 'marquePage', 'statut',
                         'internalPath', 'cleBiblio', 'note')
            tplData = (os.path.basename(file), os.path.basename(file), -1, -1, 0, -1,
                       internalPath, mainWindow.cleBiblio, 0)
            query3 = QSqlQuery()
            bOK3 = query3.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')
            #  Recherche de la cle dans videoFileTab de la nouvelle video
            query31 = QSqlQuery()
            bOk31 = query31.exec(f'SELECT MAX(cle) AS cleMax FROM videoFileTab')
            if query31.next():
                cleMax = query31.value('cleMax')
            #  Enregistrement provisoire du Titre de de la vidéo, du timeNote de l'icone (0)
            tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'texte', 'cleVideo', 'icone', 'note', 'cle')
            # Titre principal provisoire
            tplData = (0, 0, True, False, os.path.basename(file), cleMax, False, False, maxCleParagraph)
            bOk2 = query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
            if bOK3 and bOk2:
                QMessageBox.information(self, 'Success!!!', 'Record added successfully.')
            else:
                QMessageBox.critical(self, 'Database Error', f'Database Error \n\n{query.lastError().text()}')
            maxCleParagraph += 1
            # Vignette provisoire
            query4 = QSqlQuery()
            tplData = (10, 0, False, True, '', cleMax, True, False, maxCleParagraph)
            bOk4 = query4.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')

    def displayGridWindow(self, lstVideo):
        self.gridWindow = GridWindow(self, lstVideo)
        self.setCentralWidget(self.gridWindow)

    def displayTabWindow(self, lstVideo):
        lstVideoOnglet = lstVideo
        try:
            self.tabObjetScreen.close()
        except:
            pass
        self.tabObjetScreen = TabObjectScreen(self, lstVideoOnglet)
        self.setCentralWidget(self.tabObjetScreen)

    def evt_btnPlusTab_clicked(self):

        #  vider la video chargée dans mediaPlayer
        formScreen1.mediaPlayer.setMedia(QMediaContent(None))

        self.setCursor(Qt.WaitCursor)
        query = QSqlQuery()
        filtreSQL, listOnglet = self.filtreCour

        filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleBiblio={self.cleBiblio} '
        self.filtreCour = (filtreSQL, listOnglet)
        if mainWindow.cmbSortIndex == 0:  # récents
            query.exec(filtreSQL + f' ORDER BY dateLastView DESC LIMIT {mainWindow.NbVideosRecentes}')

        if mainWindow.cmbSortIndex == 1:  # favoris
            query.exec(filtreSQL + ' AND favori')
        if mainWindow.cmbSortIndex == 2:  # All items
            query.exec(filtreSQL)
        lstVideo = []
        while query.next():
            lstVideo.append(VideoFileRecord(query.value('cle')))

        self.displayGridWindow(lstVideo)
        self.unsetCursor()

    def removeTab(self):
        cleVideo = self.tabObjetScreen.barOnglet.videoTabCle
        lstAux = mainWindow.gridWindow.gridVignette.lstVignette1
        i = 0
        ongletCour = 0
        for onglet in self.tabObjetScreen.barOnglet.lstOnglet:
            if onglet.cleVideo == cleVideo:
                ongletCour = i
        #  supprimer l'onglet concerné
        self.tabObjetScreen.barOnglet.lstOnglet[ongletCour].close()
        #  Vider les mediaPlayer des vidéos chargées
        formScreen1.mediaPlayer.setMedia(QMediaContent(None))
        # Effacer la page paragraph
        mainWindow.tabObjetScreen.mainParagraph.objNote.effacer()
        #  retirer l'élément onglet de la liste
        del self.tabObjetScreen.barOnglet.lstOnglet[ongletCour]
        if len(self.tabObjetScreen.barOnglet.lstOnglet) != 0:
            cleVideo = self.tabObjetScreen.barOnglet.lstOnglet[0].cleVideo
            self.tabObjetScreen.barOnglet.majCurrentOnglet(cleVideo)

    def afficheFiltreCour(self):
        self.setCursor(Qt.WaitCursor)
        self.evt_actGrilleVideo_clicked()
        query = QSqlQuery()
        filtreSQL, listOnglet = self.filtreCour

        query.exec(filtreSQL)
        lstVideo = []
        while query.next():
            lstVideo.append(VideoFileRecord(query.value('cle')))

        mainWindow.displayGridWindow(lstVideo)
        self.unsetCursor()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************    M A I N W I N D O W      C U S T O M      ********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainWindowCustom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Masquer la barre de titre
        self.setGeometry(100, 100, 700, 500)
        f = open('styles/QTextEdit.txt', 'r')
        style = f.read()
        # self.setStyleSheet('background-color: #223333')
        self.setStyleSheet(style)
        self.initUI_sys()


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
        #  Zone de Titre
        self.lblWindowTitle = QLabel(self.gpbTitre)
        self.lblWindowTitle.setStyleSheet('background-color: transparent; color: white')
        self.lblWindowTitle.setFixedWidth(500)
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
        self.lytTitre.addWidget(self.lblWindowTitle)
        self.lytTitre.addStretch()
        self.lytTitre.addWidget(self.btnMini)
        self.lytTitre.addWidget(self.btnMax)
        self.lytTitre.addWidget(self.btnClose)

        # Poignée de redimensionnement
        self.poignee = QLabel(self)
        self.poignee.setStyleSheet('background-color: transparent')
        self.poignee.setPixmap(QPixmap('ressources/poignee.png'))
        self.poignee.setFixedSize(20, 20)
        cursor = QCursor(Qt.SizeFDiagCursor)
        self.poignee.setCursor(cursor)

        #  Bouton fermer (avec sauvegarde des modifications)
        self.btnFermer = QPushButton(self)
        self.btnFermer.setText('Fermer')
        self.btnFermer.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnFermer.setFixedSize(100, 35)
        self.btnFermer.move(600, 520)
        self.btnFermer.clicked.connect(self.closeWindow)

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

    def setTitle(self, aux):
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(False)
        self.lblWindowTitle.setFont(font)
        self.lblWindowTitle.setText(f'   {aux}')

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
        self.btnFermer.setGeometry(w-130, h-50, 100, 35)

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

    def setBtnMax(self, boolAux):
        self.btnMax.setVisible(boolAux)

    def setBtnMini(self, boolAux):
        self.btnMini.setVisible(boolAux)

    def setBtnClose(self, boolAux):
        self.btnClose.setVisible(boolAux)


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************    D I A L O G C U S T O M    **************************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class DialogCustom(QDialog):
    def __init__(self, parent=None, contenant=None, x=100, y=100):
        super(DialogCustom, self).__init__(parent)
        self.x = x
        self.y = y
        self.contenant = contenant

        self.setUpUISystem()

        self.button_ok = QPushButton(self)
        self.button_ok.setFixedSize(100, 35)
        self.button_ok.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.button_ok.setText('Accepter')
        self.button_ok.move(50, 200)

        self.button_annul = QPushButton(self)
        self.button_annul.setFixedSize(100, 35)
        self.button_annul.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.button_annul.setText('Refuser')
        self.button_annul.move(300, 200)

        #  Zone de message
        grpMessage = QGroupBox(self)
        grpMessage.setFixedSize(350, 155)
        grpMessage.setStyleSheet('background-color: #223333; border: 0px;')
        grpMessage.move(50, 35)

        # Label message
        self.lblMessage = QLabel(grpMessage)
        self.lblMessage.setStyleSheet('color: #ffffff; background-color: #223333')
        self.lblMessage.setFixedSize(300, 155)
        self.lblMessage.setWordWrap(True)
        self.lblMessage.setAlignment(Qt.AlignTop)
        self.lblMessage.setWordWrap(True)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(False)
        self.lblMessage.setFont(font)
        self.lblMessage.move(20, 15)
        #  Zone saisie
        self.grpSaisie = QGroupBox(self)
        self.grpSaisie.setFixedSize(350, 75)
        self.grpSaisie.setStyleSheet('background-color: #223333; border: 0px')
        self.grpSaisie.move(50, 115)
        # lineEdit saisie
        self.lneSaisie = QLineEdit(self.grpSaisie)
        self.lneSaisie.setStyleSheet('color: #ffffff; background-color: #666666; border-radius: 6px')
        self.lneSaisie.setFixedSize(350, 35)
        self.lneSaisie.setAlignment(Qt.AlignLeft)
        # self.lblMessage.setWordWrap(True)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(9)
        font.setBold(False)
        self.lneSaisie.setFont(font)
        self.lneSaisie.setVisible(True)
        self.lneSaisie.move(0, 15)

        # Connexion des signaux et des slots
        self.button_ok.clicked.connect(self.accept)
        self.button_annul.clicked.connect(self.reject)

    def setUpUISystem(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Masquer la barre de titre
        self.setGeometry(self.x, self.y, 450, 250)
        self.move(0, 0)
        self.setStyleSheet('background-color: #223333; border: 1px solid gray')

        self.boolMoveWindow = False
        self.mousePressed = False
        self.oldPos = None
        self.resizeCorner = None

        #  Barre de titre
        self.gpbTitre = QGroupBox(self)
        self.gpbTitre.setFixedSize(450, 35)
        self.gpbTitre.setStyleSheet('background-color: #3c3f41; border-left: 1px solid gray; '
                                    'border-top: 1px solid gray; border-right: 1px solid gray; border-bottom: 0px')
        self.gpbTitre.installEventFilter(self)
        self.lytTitre = QHBoxLayout()
        self.gpbTitre.setLayout(self.lytTitre)
        self.lblWindowTitle = QLabel(self.gpbTitre)
        self.lblWindowTitle.setFixedSize(300, 35)
        self.lblWindowTitle.setStyleSheet('background-color: transparent; color: white; border: 0px')
        self.lytTitre.addWidget(self.lblWindowTitle)
        self.lytTitre.setContentsMargins(0, 0, 0, 0)

        #  Bouton close
        self.btnClose = QPushButton(self.gpbTitre)
        self.btnClose.setFixedSize(58, 35)
        self.btnClose.setIcon(QIcon('ressources/titreClose.png'))
        self.btnClose.setIconSize(QSize(58, 35))
        self.btnClose.setStyleSheet('QPushButton{border: 0px} '
                                    'QPushButton:hover {background-color: #e81123; color: white;}')
        self.btnClose.clicked.connect(self.closeWindow)

        self.lytTitre.addStretch()
        self.lytTitre.addWidget(self.btnClose)

    def setMessage(self, aux):
        self.lblMessage.setText(aux)

    def setBouton1(self, aux, boolVisible):
        self.button_ok.setVisible(boolVisible)
        if boolVisible:
            self.button_ok.setText(aux)

    def setBouton2(self, aux, boolVisible):
        self.button_annul.setVisible(boolVisible)
        if boolVisible:
            self.button_annul.setText(aux)

    def setSaisie(self, aux, boolVisible):
        self.grpSaisie.setVisible(boolVisible)
        if boolVisible:
            self.lneSaisie.setPlaceholderText(aux)

    def setPosition(self, x, y):
        self.move(x, y)

    def closeWindow(self):
        self.close()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            if source == self.gpbTitre:
                self.boolMoveWindow = True
        return QWidget.eventFilter(self, source, event)

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
                self.setGeometry(self.x(), self.y() + delta.y(), self.width() + delta.x(),
                                 self.height() - delta.y())
            elif self.resizeCorner == Qt.BottomLeftCorner:
                self.setGeometry(self.x() + delta.x(), self.y(), self.width() - delta.x(),
                                 self.height() + delta.y())
            elif self.resizeCorner == Qt.BottomRightCorner:
                self.setGeometry(self.x(), self.y(), self.width() + delta.x(), self.height() + delta.y())
            self.oldPos = event.globalPos()

    def setBtnClose(self, boolAux):
        self.btnClose.setVisible(boolAux)

#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************   P A S T I L L E   S I M P L E  ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class PastilleSimple(QLabel):
    def __init__(self, parent=None, radius=5, color=None):
        super(PastilleSimple, self).__init__(parent)
        self.radius =  radius
        self.color = color
        self.setStyleSheet('background-color: transparent')
        self.setFixedSize(2*self.radius+3, 2*self.radius+3)


    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(QColor(self.color))
        painter.setPen(pen)
        brush = QBrush(QColor(self.color))
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawEllipse(1, 1, 2*self.radius, 2*self.radius)

    def setPosition(self, x, y):
        self.move(x, y)

#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************   P A S T I L L E   I C O N E    ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class PastilleIcone(QPixmap):
    def __init__(self, parent=None, radius=5, color=None):
        super(PastilleIcone, self).__init__(parent)
        self.radius =  radius
        self.color = color
        # self.setStyleSheet('background-color: transparent')
        # self.setFixedSize(2*self.radius+3, 2*self.radius+3)
        self = self.scaled(2*self.radius+3, 2*self.radius+3)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(QColor(self.color))
        painter.setPen(pen)
        brush = QBrush(QColor(self.color))
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawEllipse(1, 1, 2*self.radius, 2*self.radius)

    def setPosition(self, x, y):
        self.move(x, y)

#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************  F O R M P R E F E R E C E S V I D E O ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class FormPreferencesVideo(MainWindowCustom):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 910, 580)
        self.setBtnMax(False)
        self.setBtnMini(False)
        self.colorLabel = ''
        self.cleBiBlioCour = -1
        self.nomBiblioCour = ''

        # Titre
        # Titre
        lblPreferences = QLabel(self)
        lblPreferences.setText('Préférences')
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

        #  Menu Bibliotthèque
        self.btnBiblio = QPushButton(self)
        self.btnBiblio.setText('Bibliothèques')
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnBiblio.setFont(font1)
        self.btnBiblio.setStyleSheet(self.styleDesabled)
        self.btnBiblio.setFixedSize(250, 35)
        self.btnBiblio.move(20, 100)
        self.btnBiblio.clicked.connect(self.evt_btnBiblio_clicked)
        self.lstMenu.append(self.btnBiblio)

        #  Menu Langues
        self.btnLangues = QPushButton(self)
        self.btnLangues.setText('Langues')
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
        self.btnParametres.setText('Paramètres vidéo')
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
        self.btnThemes.setText('Thèmes')
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

        #  Construire infoGeneUI
        self.biblioUI()
        #  Construire choix des langues
        self.languesUI()
        #  Construire parametres Vidéo
        self.parametresUI()
        #  Construire Thèmes
        self.themesUI()
        #  Construire Classeurs
        # self.labelUI()

    def evt_btnBiblio_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Bibliothèques':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreBiblio.setVisible(True)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(False)

    def evt_btnLangues_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Langues':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(True)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(False)

    def evt_btnParametres_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Paramètres vidéo':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(True)
        self.cadreThemes.setVisible(False)

    def evt_btnThemes_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Thèmes':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreBiblio.setVisible(False)
        self.cadreLangues.setVisible(False)
        self.cadreParametres.setVisible(False)
        self.cadreThemes.setVisible(True)

    def biblioUI(self):
        self.cadreBiblio = QGroupBox(self)
        self.cadreBiblio.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreBiblio.setFixedSize(640, 440)
        self.cadreBiblio.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreBiblio)
        lblTitre.setText('Gestion des bibliothèques')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 15)

        # Bibliothèque courante
        self.lblBiblioCourant = QLabel(self.cadreBiblio)
        query = QSqlQuery()
        query.exec(f'SELECT cleRacine FROM parametersTab WHERE cle={1}')
        if query.next():
            if query.value('cleRacine') == -1:
                QMessageBox.information(self, 'Pas de bibliothèques crées', 'Pour utiliser le ligiciel, il faut'
                                                            'au préalable saisir au moins une bibliothèque!')
                # --> renvoyer sur l'initialisation de la première bibliothèque
            else:
                self.cleBiBlioCour = query.value('cleRacine')
        query = QSqlQuery()
        query.exec(f'SELECT nom FROM biblioTab WHERE cle={self.cleBiBlioCour}')
        aux = ''
        if query.next():
            aux = query.value('nom')

        self.lblBiblioCourant.setText(aux)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        self.lblBiblioCourant.setStyleSheet('color: #f05a24')
        font.setBold(True)
        self.lblBiblioCourant.setFixedWidth(250)
        self.lblBiblioCourant.setFont(font)
        self.lblBiblioCourant.move(20, 50)

        #  Bouton d'administration des classeurs
        self.btnAdmiValid = QPushButton(self.cadreBiblio)
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiValid.setFixedSize(39, 39)
        self.btnAdmiValid.setIconSize(QSize(33, 33))
        self.btnAdmiValid.move(10, 80)
        self.btnAdmiValid.setCursor(Qt.PointingHandCursor)
        self.btnAdmiValid.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiValid.clicked.connect(self.evt_btnAdmiValid_clicked)
        #
        self.btnAdmiPlus = QPushButton(self.cadreBiblio)
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus.setFixedSize(39, 39)
        self.btnAdmiPlus.setIconSize(QSize(33, 33))
        self.btnAdmiPlus.move(55, 80)
        self.btnAdmiPlus.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus.clicked.connect(self.evt_btnAdmiPlus_clicked)
        #
        self.btnAdmiModif = QPushButton(self.cadreBiblio)
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif.setFixedSize(39, 39)
        self.btnAdmiModif.setIconSize(QSize(33, 33))
        self.btnAdmiModif.move(100, 80)
        self.btnAdmiModif.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif.clicked.connect(self.evt_btnAdmiModif_clicked)
        #
        self.btnAdmiSuppr = QPushButton(self.cadreBiblio)
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr.setFixedSize(39, 39)
        self.btnAdmiSuppr.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr.move(145, 80)
        self.btnAdmiSuppr.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr.clicked.connect(self.evt_btnAdmiSuppr_clicked)

        #  GroupBox des Bibliothèques
        grpLstBiblio = QGroupBox(self.cadreBiblio)
        grpLstBiblio.setFixedSize(260, 300)
        grpLstBiblio.move(10, 130)
        grpLstBiblio.setStyleSheet('background-color: #222222; border: 0px')
        # grpLstBiblio.
        lyt = QVBoxLayout()
        grpLstBiblio.setLayout(lyt)
        # Liste des bibliothèques
        self.lstBiblio = QListWidget()
        self.lstBiblio.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lstBiblioIndex = -1
        self.cleBiblioTemp = -1
        self.nomBiblioTemp = ''
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lstBiblio.setFont(font)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.lstBiblio.setStyleSheet(style)
        lyt.addWidget(self.lstBiblio)
        self.lstBiblio.itemClicked.connect(self.evt_lstBiblio_currentItemChanged)
        self.populateLstBiblio()

        # *********************************************************************************************
        #  Cadre Aide
        # *********************************************************************************************
        self.grpCadreAide = QGroupBox(self.cadreBiblio)
        self.grpCadreAide.setFixedSize(340, 400)
        self.grpCadreAide.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadreAide.move(280, 20)
        #  Titre Aide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        lblAide = QLabel(self.grpCadreAide)
        lblAide.setFont(font)
        lblAide.setText('Aide')
        lblAide.setStyleSheet('color: #F05A24; border: 0px')
        lblAide.move(20, 25)
        # textAide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        lblTextAide = QLabel(self.grpCadreAide)
        lblTextAide.setWordWrap(True)
        lblTextAide.setFixedSize(300, 75)
        lblTextAide.setStyleSheet('background-color: #222222; color: #777777; border: 0px')
        aux = 'Les bibliothèques constitue le classement le plus élevé. ' \
              'Ils comportent des classeurs qui contiennent les vidéos.'
        lblTextAide.setText(aux)
        lblTextAide.setFont(font)
        lblTextAide.move(20, 60)

        #  Aide icones
        #  Valid
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        lblValid = QLabel(self.grpCadreAide)
        lblValid.setFixedSize(39, 39)
        lblValid.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiValid2')
        img = img.scaled(33, 33)
        lblValid.setPixmap(img)
        lblValid.move(20, 160)
        lblAideValid = QLabel(self.grpCadreAide)
        lblAideValid.setStyleSheet('border: 0px; color: #777777')
        lblAideValid.setFont(font)
        lblAideValid.setText('Sélectionne la bibliothèque cpurante')
        lblAideValid.move(70, 170)

        #  Plus
        lblPlus = QLabel(self.grpCadreAide)
        lblPlus.setFixedSize(39, 39)
        lblPlus.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiPlus2')
        img = img.scaled(33, 33)
        lblPlus.setPixmap(img)
        lblPlus.move(20, 210)
        lblAidePlus = QLabel(self.grpCadreAide)
        lblAidePlus.setStyleSheet('border: 0px; color: #777777')
        lblAidePlus.setFont(font)
        lblAidePlus.setText('Ajouter une nouvelle bibliothèque')
        lblAidePlus.move(70, 220)
        #  Modif
        lblModif = QLabel(self.grpCadreAide)
        lblModif.setFixedSize(39, 39)
        lblModif.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiModif2')
        img = img.scaled(33, 33)
        lblModif.setPixmap(img)
        lblModif.move(20, 260)
        lblAideModif = QLabel(self.grpCadreAide)
        lblAideModif.setStyleSheet('border: 0px; color: #777777')
        lblAideModif.setFont(font)
        lblAideModif.setText('Editer la bibliothèque sélectionnée')
        lblAideModif.move(70, 270)
        #  Supprimer
        lblSuppr = QLabel(self.grpCadreAide)
        lblSuppr.setFixedSize(39, 39)
        lblSuppr.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiSuppr2')
        img = img.scaled(33, 33)
        lblSuppr.setPixmap(img)
        lblSuppr.move(20, 310)
        lblAideSuppr = QLabel(self.grpCadreAide)
        lblAideSuppr.setStyleSheet('border: 0px; color: #777777')
        lblAideSuppr.setFont(font)
        lblAideSuppr.setText('Supprimer la bibliothèque sélectionnée')
        lblAideSuppr.move(70, 320)

        # *********************************************************************************************
        #  Cadre Plus
        # *********************************************************************************************
        self.grpCadrePlusBiblio = QGroupBox(self.cadreBiblio)
        self.grpCadrePlusBiblio.setFixedSize(340, 450)
        self.grpCadrePlusBiblio.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadrePlusBiblio.move(280, 20)
        #  Titre Plus
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.lblPlusBiblio = QLabel(self.grpCadrePlusBiblio)
        self.lblPlusBiblio.setFont(font)
        self.lblPlusBiblio.setText('Créer une nouvelle bibliothèque')
        self.lblPlusBiblio.setStyleSheet('color: white; border: 0px')
        self.lblPlusBiblio.move(20, 25)
        self.grpCadrePlusBiblio.setVisible(False)

        #  Titre parcourir
        self.lblTitrePlusBiblio = QLabel(self.grpCadrePlusBiblio)
        self.lblTitrePlusBiblio.setStyleSheet('background: transparent; color: white')
        self.lblTitrePlusBiblio.setText('Ajouter une bibliothèque')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lblTitrePlusBiblio.setFont(font)
        self.lblTitrePlusBiblio.move(20, 75)

        #  btn Parcourir
        self.btnPacourir = QPushButton(self.grpCadrePlusBiblio)
        self.btnPacourir.setText('Parcourir')
        self.btnPacourir.setFixedSize(100, 35)
        self.btnPacourir.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnPacourir.move(20, 105)
        self.btnPacourir.clicked.connect(self.evt_btnParcourir_clicked)
        #  lbl chemin biblio
        lblTitreChemin  = QLabel(self.grpCadrePlusBiblio)
        lblTitreChemin.setStyleSheet('background: transparent; color: white')
        lblTitreChemin.setText('Chemin')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitreChemin.setFont(font)
        lblTitreChemin.move(20, 175)
        #
        self.lblChemin = QLabel(self.grpCadrePlusBiblio)
        self.lblChemin.setStyleSheet('color: gray')
        self.lblChemin.setFixedSize(300, 30)
        self.lblChemin.move(20, 200)
        #  Saisie du nom de la bibliothèque
        lblTitreNom = QLabel(self.grpCadrePlusBiblio)
        lblTitreNom.setStyleSheet('background: transparent; color: white')
        lblTitreNom.setText('Nom de la bibliothèque')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitreNom.setFont(font)
        lblTitreNom.move(20, 250)
        #
        self.lneNom = QLineEdit(self.grpCadrePlusBiblio)
        self.lneNom.setPlaceholderText('Saisir le nom de la nouvelle bibliothèque')
        self.lneNom.setStyleSheet('border: 1px solid gray')
        self.lneNom.setFixedSize(300, 30)
        self.lneNom.move(20, 275)
        # Boutons Enregistrer Annuler
        self.btnSauverBiblio = QPushButton(self.grpCadrePlusBiblio)
        self.btnSauverBiblio.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                             'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSauverBiblio.setFixedSize(100, 35)
        self.btnSauverBiblio.setText('Enregistrer')
        self.btnSauverBiblio.move(20, 350)
        self.btnSauverBiblio.clicked.connect(self.evt_btnSauverBiblio_clicked)
        #
        self.btnAnnulerBiblio = QPushButton(self.grpCadrePlusBiblio)
        self.btnAnnulerBiblio.setStyleSheet(
            'QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
            'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnAnnulerBiblio.setFixedSize(100, 35)
        self.btnAnnulerBiblio.setText('Annuler')
        self.btnAnnulerBiblio.move(140, 350)
        self.btnAnnulerBiblio.clicked.connect(self.evt_btnAnnulerBiblio_clicked)

        # self.populateLstClasseur()
        self.cadreBiblio.setVisible(False)

    def languesUI(self):
        self.cadreLangues = QGroupBox(self)
        self.cadreLangues.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreLangues.setFixedSize(640, 440)
        self.cadreLangues.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreLangues)
        lblTitre.setText('Choix de la langue')
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

        # *********************************************************************************************
        #  Cadre Aide
        # *********************************************************************************************
        self.grpCadreAide1 = QGroupBox(self.cadreLangues)
        self.grpCadreAide.setFixedSize(340, 400)
        self.grpCadreAide.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadreAide1.move(280, 20)
        #  Titre Aide1
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        lblAide1 = QLabel(self.grpCadreAide1)
        lblAide1.setFont(font)
        lblAide1.setText('Aide')
        lblAide1.setStyleSheet('color: #F05A24; border: 0px')
        lblAide1.move(20, 25)
        # textAide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        lblTextAide1 = QLabel(self.grpCadreAide1)
        lblTextAide1.setWordWrap(True)
        lblTextAide1.setFixedSize(300, 75)
        lblTextAide1.setStyleSheet('background-color: #222222; color: #777777; border: 0px')
        aux = "Le choix d'une nouvelle langue permet de traduire l'application. "
        lblTextAide1.setText(aux)
        lblTextAide1.setFont(font)
        lblTextAide1.move(20, 60)

        self.cadreLangues.setVisible(False)

    def parametresUI(self):
        self.cadreParametres = QGroupBox(self)
        self.cadreParametres.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreParametres.setFixedSize(640, 440)
        self.cadreParametres.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreParametres)
        lblTitre.setText('Paramètres de la vidéo')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 5)

        # Lecture vidéo
        self.lblLectureVideo = QLabel(self.cadreParametres)
        self.lblLectureVideo.setText('Lecture vidéo')
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
        lblLecture.setText('La video démarre automatiquement au lancement')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        lblLecture.setFont(font)
        lblLecture.setWordWrap(True)
        lblLecture.move(330, 45)
        # Son
        self.lblLectureSon = QLabel(self.cadreParametres)
        self.lblLectureSon.setText('Son')
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
        lblTitre.setText('Thèmes')
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

    def evt_btnAdmiValid_clicked(self):
        self.grpCadreAide.setVisible(True)
        if self.cleBiblioTemp == -1:
            return
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid1.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de sélectionner une nouvelle bibliothèque. \nEtes-vous certain de votre choix ?'
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
        self.grpCadreAide.setVisible(True)
        if self.cleLanguesTemp == -1:
            return
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid1.png'))
        # self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        # self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        # self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de sélectionner une nouvelle langue. \nEtes-vous certain de votre choix ?'
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
        aux = 'Vous êtes en train de sélectionner un nouveau thème. \nEtes-vous certain de votre choix ?'
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
            # print(query.value("nom"))
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
            # self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
            self.cleLanguesTemp = current.data(Qt.UserRole)
            self.nomLanguesCour = current.text()
        except:
            pass

    def evt_lstThemes_currentItemChanged(self, current):
        try:
            self.btnAdmiValid2.setIcon(QIcon('ressources/admiValid.png'))
            # self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
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


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************  F O R M E D I T I O N V I D E O ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************

class FormEditionVideo(MainWindowCustom):
    def __init__(self, videoCour):
        super().__init__()
        self.setGeometry(200, 100, 910, 580)
        self.videoCour = videoCour
        self.videoRecordCour = VideoFileRecord(self.videoCour)
        self.setBtnMax(False)
        self.setBtnMini(False)
        self.colorLabel = ''
        # Titre
        lblClassement = QLabel(self)
        lblClassement.setText('Classement')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(20)
        font.setBold(True)
        lblClassement.setFont(font)
        lblClassement.setStyleSheet('background-color: transparent; color: #f05a24')
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
        self.lstMenu.append(self.btnMatieres)

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
        self.font1.setPointSize(12)
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
        #  Construire Classeurs
        self.classeurUI()
        #  Construire Classeurs
        self.labelUI()

    def evt_btnInfoGene_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Informations générales':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreInfoGene.setVisible(True)
        self.cadreTableMatiere.setVisible(False)
        self.cadreClasseur.setVisible(False)
        self.cadreTag.setVisible(False)
        self.cadreLabel.setVisible(False)


    def evt_btnMatieres_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Table des matières':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(True)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(False)
        self.cadreClasseur.setVisible(False)
        self.cadreLabel.setVisible(False)

    def evt_btnTags_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Tags':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(False)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(True)
        self.cadreClasseur.setVisible(False)
        self.cadreLabel.setVisible(False)

    def evt_btnClasseurs_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Classeurs':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
            self.cadreTableMatiere.setVisible(False)
            self.cadreInfoGene.setVisible(False)
            self.cadreTag.setVisible(False)
            self.cadreClasseur.setVisible(True)
            self.cadreLabel.setVisible(False)

    def evt_btnLabels_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == 'Labels':
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
            self.cadreTableMatiere.setVisible(False)
            self.cadreInfoGene.setVisible(False)
            self.cadreTag.setVisible(False)
            self.cadreClasseur.setVisible(False)
            self.cadreLabel.setVisible(True)


    def infoGeneUI(self):
        self.cadreInfoGene = QGroupBox(self)
        self.cadreInfoGene.setStyleSheet('background-color: #333333; color: white; border: 0px')
        self.cadreInfoGene.setFixedSize(600, 430)
        self.cadreInfoGene.move(300, 55)
        # titre
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setText('Informations générales')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(200, 45)
        # lblNote
        lblNote = QLabel(self.cadreInfoGene)
        lblNote.setAlignment(Qt.AlignRight)
        lblNote.setStyleSheet('color: #ffffff; background-color: transparent')
        lblNote.setFixedWidth(180)
        lblNote.setText('Note')
        lblNote.setFont(self.font1)
        lblNote.move(2, 100)
        #  lbl Note vidéo
        self.grpRating = QGroupBox(self.cadreInfoGene)
        self.lblNoteVideo = StarRating(self.videoRecordCour.note)
        self.grpRating.setFixedSize(250, 43)
        self.grpRating.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpRating.move(200, 77)
        lytRating = QVBoxLayout()
        lytRating.setSpacing(0)
        lytRating.addWidget(self.lblNoteVideo)
        self.grpRating.setLayout(lytRating)
        # lblFavori
        lblFavori = QLabel(self.cadreInfoGene)
        lblFavori.setAlignment(Qt.AlignRight)
        lblFavori.setStyleSheet('color: #ffffff; background-color: transparent')
        lblFavori.setFixedWidth(180)
        lblFavori.setText('Favori')
        lblFavori.setFont(self.font1)
        lblFavori.move(2, 144)
        #  lbl Favori vidéo
        self.grpFavori = QGroupBox(self.cadreInfoGene)
        self.lblFavoriVideo = WidgetFavori(boolFavori=self.videoRecordCour.Favori)
        self.grpFavori.setFixedSize(40, 40)
        self.grpFavori.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpFavori.move(209, 133)
        lytFavori = QVBoxLayout()
        lytFavori.setSpacing(0)
        lytFavori.addWidget(self.lblFavoriVideo)
        self.grpFavori.setLayout(lytFavori)
        #  lblTitre de la video
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setAlignment(Qt.AlignRight)
        lblTitre.setStyleSheet('color: #eeeeee; background-color: #333333')
        lblTitre.setFixedWidth(180)
        lblTitre.setText('Titre de la vidéo')
        lblTitre.setFont(self.font1)
        lblTitre.move(2, 188)
        #  lblTitre vidéo
        self.lblTitreVideo = QLabel(self.cadreInfoGene)
        self.lblTitreVideo.setText('titre de la vidéo')
        # style = "color: white; background-color: #666666; border: 1px solid #455364; border-radius: 4px;"
        # styleQLabel = style
        self.lblTitreVideo.setStyleSheet('color: #888888')
        self.lblTitreVideo.setFixedSize(310, 30)
        self.lblTitreVideo.move(210, 184)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        font2.setBold(True)
        self.lblTitreVideo.setFont(font2)
        if self.videoRecordCour.titreVideo == '':
            self.lblTitreVideo.setText(self.videoRecordCour.videoName)
        else:
            self.lblTitreVideo.setText(self.videoRecordCour.titreVideo)
        # lblNom
        lblNom = QLabel(self.cadreInfoGene)
        lblNom.setAlignment(Qt.AlignRight)
        lblNom.setStyleSheet('color: #ffffff; background-color: transparent')
        lblNom.setFixedWidth(180)
        lblNom.setText('Nom du fichier')
        lblNom.setFont(self.font1)
        lblNom.move(2, 232)
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
        self.lblNomVideo.move(210, 228)
        #  lblChemin
        lblChemin = QLabel(self.cadreInfoGene)
        lblChemin.setAlignment(Qt.AlignRight)
        lblChemin.setStyleSheet('color: #ffffff; background-color: transparent')
        lblChemin.setFixedWidth(180)
        lblChemin.setText('Chemin')
        lblChemin.setFont(self.font1)
        lblChemin.move(2, 276)
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
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblCheminVideo.setFont(font2)
        self.lblCheminVideo.setStyleSheet('color: #888888')
        self.lblCheminVideo.move(210, 272)
        # lblDurée
        lblDuree = QLabel(self.cadreInfoGene)
        lblDuree.setAlignment(Qt.AlignRight)
        lblDuree.setStyleSheet('color: #ffffff; background-color: transparent')
        lblDuree.setFixedWidth(180)
        lblDuree.setText('Durée')
        lblDuree.setFont(self.font1)
        lblDuree.move(2, 320)
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
        self.lblDureeVideo.move(210, 318)
        # Label titre
        lblStatut = QLabel(self.cadreInfoGene)
        lblStatut.setAlignment(Qt.AlignRight)
        lblStatut.setStyleSheet('color: #ffffff; background-color: #333333')
        lblStatut.setFixedWidth(180)
        lblStatut.setText('Label de la vidéo')
        lblStatut.setFont(self.font1)
        lblStatut.move(2, 364)
        #  Label video
        self.lblLabelVideo = QLabel(self.cadreInfoGene)
        self.lblLabelVideo.setFixedSize(310, 30)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(8)
        font2.setItalic(True)
        self.lblLabelVideo.setFont(font2)
        self.lblLabelVideo.setStyleSheet('color: #888888')
        try:
            color = self.videoRecordCour.colorStatut
            nomLabel = self.videoRecordCour.nomStatut
        except:
            color = '#ffffff'
            nomLabel = 'Aucun label'
        self.lblLabelVideo.setText('         ' + nomLabel)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblLabelVideo.setFont(font2)
        self.lblPastilleInfo = QLabel(self.lblLabelVideo)
        self.lblPastilleInfo.setFixedSize(19, 19)
        self.lblPastilleInfo.setStyleSheet('background: transparent')
        self.lblPastilleInfo.move(3, 4)
        if self.videoRecordCour.statut == -1:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, ''))
        else:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, color))
        self.lblLabelVideo.move(205, 364)
        #  lbl Classeur
        lblClasseur = QLabel(self.cadreInfoGene)
        lblClasseur.setAlignment(Qt.AlignRight)
        lblClasseur.setStyleSheet('color: #ffffff; background-color: #333333')
        lblClasseur.setFixedWidth(180)
        lblClasseur.setText('Classeur de la vidéo')
        lblClasseur.setFont(self.font1)
        lblClasseur.move(2, 408)
        #  Classeur vidéo
        self.lblClasseurVideo = QLabel(self.cadreInfoGene)
        self.lblClasseurVideo.setFixedSize(310, 30)
        self.lblClasseurVideo.setText( self.videoRecordCour.nomClasseur)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblClasseurVideo.setFont(font2)
        self.lblClasseurVideo.setStyleSheet('color: #888888')
        self.lblClasseurVideo.move(210, 405)

        self.cadreInfoGene.setVisible(False)
        # self.cmbStatut.currentIndexChanged.connect(self.evt_cmbStatut_currentIndexChanged)

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
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)

        #  Mise en place du ScrollArea
        scrollArea = QScrollArea()
        widget = QWidget(self.cadreTableMatiere)
        widget.setStyleSheet('background-color: #333333;')
        widget.setFixedSize(480, 1000)
        widget.move(150, 100)
        self.lytTableMatiere = QVBoxLayout()
        #  Ajouter le contenu
        self.populateTableMatiere()
        #
        widget.setLayout(self.lytTableMatiere)
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

    def populateTableMatiere(self):
        while self.lytTableMatiere.count():
            widget = self.lytTableMatiere.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        query = QSqlQuery()
        query.exec(f'SELECT * FROM paragraph WHERE cleVideo={self.videoCour} AND titre ORDER BY timeNote')
        i = 0
        while query.next():
            # print(query.value('cle'), query.value('texte'))
            texte = query.value('texte')
            texte = texte.replace('$$', chr(32))
            texte = texte.replace(')|', chr(34))
            texte = texte.replace('µµ', chr(9))
            lbl = LabelIndex(self.cadreTableMatiere, query.value('timeNote'), None, None, None)
            lbl.setText(texte[:50] + '...')
            lbl.setFixedSize(500, 40)
            lbl.setStyleSheet(
                'background: #222222')  # ; border-top: 5px solid #333333; border-bottom: 5px solid #333333
            font2 = QFont()
            font2.setFamily('Arial')
            font2.setPointSize(10)
            font2.setBold(False)
            lbl.setFont(font2)
            # lbl.move(0, i*50)
            # btnAdmiModif2
            self.btnAdmiModif2 = QPushButton(lbl)
            self.btnAdmiModif2.setIcon(QIcon('ressources/admiModif.png'))
            self.btnAdmiModif2.setFixedSize(39, 39)
            self.btnAdmiModif2.setIconSize(QSize(33, 33))
            self.btnAdmiModif2.move(390, 0)
            self.btnAdmiModif2.setCursor(Qt.PointingHandCursor)
            self.btnAdmiModif2.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
            self.btnAdmiModif2.clicked.connect(self.evt_btnAdmiModif2_clicked)
            # btnAdmiSuppr2
            self.btnAdmiSuppr2 = QPushButton(lbl)
            self.btnAdmiSuppr2.setIcon(QIcon('ressources/admiSuppr.png'))
            self.btnAdmiSuppr2.setFixedSize(39, 39)
            self.btnAdmiSuppr2.setIconSize(QSize(33, 33))
            self.btnAdmiSuppr2.move(430, 0)
            self.btnAdmiSuppr2.setCursor(Qt.PointingHandCursor)
            self.btnAdmiSuppr2.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
            self.btnAdmiSuppr2.clicked.connect(self.evt_btnAdmiSuppr2_clicked)
            #
            i += 1
            self.lytTableMatiere.addWidget(lbl)
            self.lytTableMatiere.setSpacing(10)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lytTableMatiere.addItem(spacerItem)

    def evt_btnAdmiModif2_clicked(self):
        lbl = self.sender().parent()
        timeNote = lbl.index
        query = QSqlQuery()
        query.exec(f'SELECT * from Paragraph where timeNote={timeNote}')
        if query.next():
            videoPath = self.videoRecordCour.videoPath
            videoId = self.videoRecordCour.cle
            marqueCour = query.value('TimeNote')
            boolCreer = False
            videoFullPath = mainWindow.racine + self.videoRecordCour.internalPath + videoPath
            formGererNote = FormBlockNote(self, videoFullPath, videoId, marqueCour, boolCreer)
            # formGererNote = FormGererNote(self, videoFullPath, videoId, marqueCour, boolCreer)
            formGererNote.show()

    def evt_btnAdmiSuppr2_clicked(self):
        lbl = self.sender().parent()
        clePagraph = lbl.index
        self.dialog = DialogCustom(self, 200, 200)
        aux = 'Vous êtes en train de supprimer une note. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM paragraph WHERE cle = {clePagraph}')
        else:
            pass

        self.populateTableMatiere()

    def tagUI(self):
        self.cadreTag = QGroupBox(self)
        self.cadreTag.setStyleSheet('background-color: #222222; border: 0px')
        self.cadreTag.setFixedSize(600, 400)
        self.cadreTag.move(250, 55)

        self.cadreTitre = QGroupBox(self.cadreTag)
        self.cadreTitre.setFixedSize(600, 45)
        self.cadreTitre.setStyleSheet('background-color: #222222; border: 0px')
        self.cadreTitre.move(0, 0)

        # titre
        lblTitre = QLabel(self.cadreTitre)
        lblTitre.setStyleSheet('color: white')
        lblTitre.setText('Tags globaux')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(15, 4)

        # Cadre affiche tags
        self.cadreAffichTitre = QGroupBox(self.cadreTag)
        self.cadreAffichTitre.setFixedSize(550, 500)
        self.cadreAffichTitre.setStyleSheet('background-color: #222222; border: 0px')
        self.cadreAffichTitre.move(0, 45)

        #  Installation de GrpBoxMetaData
        lytTag = QVBoxLayout()
        self.cadreAffichTitre.setLayout(lytTag)
        grpBoxTag = GrpBoxMetaData(self, self, self.videoCour, lytTag)
        lytTag.addWidget(grpBoxTag)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lytTag.addItem(spacer)

        self.cadreTag.setVisible(False)

    def classeurUI(self):
        self.cadreClasseur = QGroupBox(self)
        self.cadreClasseur.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreClasseur.setFixedSize(640, 440)
        self.cadreClasseur.move(250, 55)
        # titre
        lblTitre = QLabel(self.cadreClasseur)
        lblTitre.setText('Gestion des classeurs')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 15)
        # Classeur courant
        self.lblClasseurCourant = QLabel(self.cadreClasseur)
        aux = self.videoRecordCour.nomClasseur
        if aux != '':
            self.lblClasseurCourant.setText(aux)
        else:
            self.lblClasseurCourant.setText('Pas de classeur sélectionné')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        self.lblClasseurCourant.setStyleSheet('color: #f05a24')
        font.setBold(True)
        self.lblClasseurCourant.setFixedWidth(250)
        self.lblClasseurCourant.setFont(font)
        self.lblClasseurCourant.move(20, 50)
        #  Bouton d'administration des classeurs
        self.btnAdmiValid = QPushButton(self.cadreClasseur)
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiValid.setFixedSize(39, 39)
        self.btnAdmiValid.setIconSize(QSize(33, 33))
        self.btnAdmiValid.move(10, 80)
        self.btnAdmiValid.setCursor(Qt.PointingHandCursor)
        self.btnAdmiValid.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiValid.clicked.connect(self.evt_btnAdmiValid_clicked)
        #
        self.btnAdmiPlus = QPushButton(self.cadreClasseur)
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus.setFixedSize(39, 39)
        self.btnAdmiPlus.setIconSize(QSize(33, 33))
        self.btnAdmiPlus.move(55, 80)
        self.btnAdmiPlus.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus.clicked.connect(self.evt_btnAdmiPlus_clicked)
        #
        self.btnAdmiModif = QPushButton(self.cadreClasseur)
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif.setFixedSize(39, 39)
        self.btnAdmiModif.setIconSize(QSize(33, 33))
        self.btnAdmiModif.move(100, 80)
        self.btnAdmiModif.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif.clicked.connect(self.evt_btnAdmiModif_clicked)
        #
        self.btnAdmiSuppr = QPushButton(self.cadreClasseur)
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr.setFixedSize(39, 39)
        self.btnAdmiSuppr.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr.move(145, 80)
        self.btnAdmiSuppr.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr.clicked.connect(self.evt_btnAdmiSuppr_clicked)
        #  GroupBox des classeurs
        grpLstClasseur = QGroupBox(self.cadreClasseur)
        grpLstClasseur.setFixedSize(260, 300)
        grpLstClasseur.move(10, 130)
        grpLstClasseur.setStyleSheet('background-color: #222222; border: 0px')
        # grpLstClasseur.
        lyt = QVBoxLayout()
        grpLstClasseur.setLayout(lyt)
        # Liste des classeurs
        self.lstClasseur = QListWidget()
        self.lstClasseur.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lstClasseurIndex = -1
        self.cleClasseurTemp = -1
        self.nomClasseurTemp = ''
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lstClasseur.setFont(font)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.lstClasseur.setStyleSheet(style)
        lyt.addWidget(self.lstClasseur)
        self.lstClasseur.itemClicked.connect(self.evt_lstClasseur_currentItemChanged)
        # *********************************************************************************************
        #  Cadre Aide
        # *********************************************************************************************
        self.grpCadreAide = QGroupBox(self.cadreClasseur)
        self.grpCadreAide.setFixedSize(340, 400)
        self.grpCadreAide.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadreAide.move(280, 20)
        #  Titre Aide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        lblAide = QLabel(self.grpCadreAide)
        lblAide.setFont(font)
        lblAide.setText('Aide')
        lblAide.setStyleSheet('color: white; border: 0px')
        lblAide.move(20, 25)
        # textAide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        lblTextAide = QLabel(self.grpCadreAide)
        lblTextAide.setWordWrap(True)
        lblTextAide.setFixedSize(300, 75)
        lblTextAide.setStyleSheet('background-color: #222222; color: #777777; border: 0px')
        aux = 'Les classeurs sont des dossiers qui vous permettent de classer vos vidéos'
        lblTextAide.setText(aux)
        lblTextAide.setFont(font)
        lblTextAide.move(20, 60)
        #  Aide icones
        #  Valid
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        lblValid = QLabel(self.grpCadreAide)
        lblValid.setFixedSize(39, 39)
        lblValid.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiValid2')
        img = img.scaled(33, 33)
        lblValid.setPixmap(img)
        lblValid.move(20, 160)
        lblAideValid = QLabel(self.grpCadreAide)
        lblAideValid.setStyleSheet('border: 0px; color: #777777')
        lblAideValid.setFont(font)
        lblAideValid.setText('Sélectionne le classeur de votre vidéo')
        lblAideValid.move(70, 170)
        #  Plus
        lblPlus = QLabel(self.grpCadreAide)
        lblPlus.setFixedSize(39, 39)
        lblPlus.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiPlus2')
        img = img.scaled(33, 33)
        lblPlus.setPixmap(img)
        lblPlus.move(20, 210)
        lblAidePlus = QLabel(self.grpCadreAide)
        lblAidePlus.setStyleSheet('border: 0px; color: #777777')
        lblAidePlus.setFont(font)
        lblAidePlus.setText('Ajouter un nouveau classeur')
        lblAidePlus.move(70, 220)
        #  Modif
        lblModif = QLabel(self.grpCadreAide)
        lblModif.setFixedSize(39, 39)
        lblModif.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiModif2')
        img = img.scaled(33, 33)
        lblModif.setPixmap(img)
        lblModif.move(20, 260)
        lblAideModif = QLabel(self.grpCadreAide)
        lblAideModif.setStyleSheet('border: 0px; color: #777777')
        lblAideModif.setFont(font)
        lblAideModif.setText('Editer le classeur sélectionné')
        lblAideModif.move(70, 270)
        #  Supprimer
        lblSuppr = QLabel(self.grpCadreAide)
        lblSuppr.setFixedSize(39, 39)
        lblSuppr.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiSuppr2')
        img = img.scaled(33, 33)
        lblSuppr.setPixmap(img)
        lblSuppr.move(20, 310)
        lblAideSuppr = QLabel(self.grpCadreAide)
        lblAideSuppr.setStyleSheet('border: 0px; color: #777777')
        lblAideSuppr.setFont(font)
        lblAideSuppr.setText('Supprimer le classeur sélectionnée')
        lblAideSuppr.move(70, 320)
        # *********************************************************************************************
        #  Cadre Plus
        # *********************************************************************************************
        self.grpCadrePlusClasseur = QGroupBox(self.cadreClasseur)
        self.grpCadrePlusClasseur.setFixedSize(340, 450)
        self.grpCadrePlusClasseur.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadrePlusClasseur.move(280, 20)
        #  Titre Plus
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.lblPlusClasseur = QLabel(self.grpCadrePlusClasseur)
        self.lblPlusClasseur.setFont(font)
        self.lblPlusClasseur.setText('Créer un nouveau classeur')
        self.lblPlusClasseur.setStyleSheet('color: white; border: 0px')
        self.lblPlusClasseur.move(20, 25)
        self.grpCadrePlusClasseur.setVisible(False)
        #  Titre plus Nom
        lblTitrePlusClasseur = QLabel(self.grpCadrePlusClasseur)
        lblTitrePlusClasseur.setStyleSheet('background: transparent; color: white')
        lblTitrePlusClasseur.setText('Nom du classeur')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitrePlusClasseur.setFont(font)
        lblTitrePlusClasseur.move(20, 75)
        #  Saisie Plus Nom
        self.lnePlusClasseurNom = QLineEdit(self.grpCadrePlusClasseur)
        self.lnePlusClasseurNom.setStyleSheet('background: #666666; border-radius: 5px; color: white')
        self.lnePlusClasseurNom.setFixedSize(300, 25)
        self.lnePlusClasseurNom.move(20, 105)
        #  Titre plus commentaire
        lblTitrePlusClasseur1 = QLabel(self.grpCadrePlusClasseur)
        lblTitrePlusClasseur1.setStyleSheet('background: transparent; color: white')
        lblTitrePlusClasseur1.setText('Note du classeur')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitrePlusClasseur1.setFont(font)
        lblTitrePlusClasseur1.move(20, 155)
        #  Saisie Plus Note
        self.lnePlusClasseurNote = QTextEdit(self.grpCadrePlusClasseur)
        self.lnePlusClasseurNote.setStyleSheet('background: #666666; border-radius: 5px; color: white')
        self.lnePlusClasseurNote.setFixedSize(300, 140)
        self.lnePlusClasseurNote.move(20, 185)
        # Boutons Enregistrer Annuler
        self.btnSauverClasseur = QPushButton(self.grpCadrePlusClasseur)
        self.btnSauverClasseur.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSauverClasseur.setFixedSize(100, 35)
        self.btnSauverClasseur.setText('Enregistrer')
        self.btnSauverClasseur.move(20, 380)
        self.btnSauverClasseur.clicked.connect(self.evt_btnSauverClasseur_clicked)
        #
        self.btnAnnulerClasseur = QPushButton(self.grpCadrePlusClasseur)
        self.btnAnnulerClasseur.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                        'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnAnnulerClasseur.setFixedSize(100, 35)
        self.btnAnnulerClasseur.setText('Annuler')
        self.btnAnnulerClasseur.move(140, 380)
        self.btnAnnulerClasseur.clicked.connect(self.evt_btnAnnulerClasseur_clicked)

        self.populateLstClasseur()
        self.cadreClasseur.setVisible(False)

    def evt_btnSauverClasseur_clicked(self):
        if self.lnePlusClasseurNom.text() == '':
            self.dialog = DialogCustom(self, 100, 100)
            aux = 'Saisie du nom du classeur obligatoire.'
            self.dialog.setMessage(aux)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return

        if self.boolModif:
            query = QSqlQuery()
            tptData = (self.lnePlusClasseurNom.text(),
                       self.lnePlusClasseurNote.toPlainText(), False)

            tplChamps = ('Nom', 'Commentaire', 'defaut')
            bOk = query.exec(f'UPDATE classeurTab SET {tplChamps} = {tptData} '
                             f'WHERE cle={self.cleClasseurTemp}')
        else:
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) FROM classeurTab')
            try:
                if query.next():
                    maxCle = query.value(0) + 1
            except:
                maxCle = 1
            query = QSqlQuery()
            tplChamps = ('cle', 'nom', 'commentaire', 'defaut')
            tplData = (maxCle, self.lnePlusClasseurNom.text(), self.lnePlusClasseurNote.toPlainText(),
                       False)
            query.exec(f'INSERT INTO classeurTab {tplChamps} VALUES {tplData}')
        self.sauveModifVideo()
        self.populateLstClasseur()
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide.setVisible(True)
        self.grpCadrePlusClasseur.setVisible(False)
        self.lnePlusClasseurNom.setText('')
        self.lnePlusClasseurNote.setText('')
        self.grpCadrePlusClasseur.setVisible(False)
        self.cleClasseurTemp = -1

    def evt_btnSauverLabel_clicked(self):
        if self.lnePlusLabelNom.text() == '':
            self.dialog = DialogCustom(self, 100, 100)
            aux = 'Saisie du nom du label obligatoire.'
            self.dialog.setMessage(aux)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return

        if self.boolModif:
            query = QSqlQuery()
            tptData = (self.lnePlusLabelNom.text(), self.lnePlusLabelNote.toPlainText(),
                       False, self.colorLabel)
            tplChamps = ('Nom', 'Commentaire', 'defaut', 'color')
            bOk = query.exec(f'UPDATE statutTab SET {tplChamps} = {tptData} '
                             f'WHERE cle={self.cleLabelTemp}')
        else:
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) FROM statutTab')
            try:
                if query.next():
                    maxCle = query.value(0) + 1
            except:
                maxCle = 1
            query = QSqlQuery()
            tplChamps = ('cle', 'nom', 'commentaire', 'defaut', 'color')
            tplData = (maxCle, self.lnePlusLabelNom.text(), self.lnePlusLabelNote.toPlainText(),
                       False, self.colorLabel)
            query.exec(f'INSERT INTO statutTab {tplChamps} VALUES {tplData}')
        self.sauveModifVideo()
        self.populateLstLabel()
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide1.setVisible(True)
        self.grpCadrePlusLabel.setVisible(False)
        self.lnePlusLabelNom.setText('')
        self.lnePlusLabelNote.setText('')
        self.grpCadrePlusLabel.setVisible(False)
        self.cleLabelTemp = -1

    def evt_btnAnnulerClasseur_clicked(self):
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide.setVisible(True)
        self.grpCadrePlusClasseur.setVisible(False)
        self.lnePlusClasseurNom.setText('')
        self.lnePlusClasseurNote.setText('')
        self.grpCadrePlusClasseur.setVisible(False)
        self.cleClasseurTemp = -1
        self.grpCadreAide.setVisible(True)

    def evt_btnAnnulerLabel_clicked(self):
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.grpCadreAide1.setVisible(True)
        self.grpCadrePlusLabel.setVisible(False)
        self.lnePlusLabelNom.setText('')
        self.lnePlusLabelNote.setText('')
        self.grpCadrePlusLabel.setVisible(False)
        self.cleLabelTemp = -1

    def labelUI(self):
        self.cadreLabel = QGroupBox(self)
        self.cadreLabel.setStyleSheet('background-color: #222222; color: white; border: 0px')
        self.cadreLabel.setFixedSize(640, 440)
        self.cadreLabel.move(250, 55)

        # titre
        lblTitre = QLabel(self.cadreLabel)
        lblTitre.setText('Gestion des labels')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(20, 15)

        # Label courant
        self.lblPastille = QLabel(self.cadreLabel)
        self.lblPastille.setFixedSize(19, 19)
        self.lblPastille.setStyleSheet('background: transparent')
        self.lblPastille.move(20, 54)
        self.lblLabelCourant = QLabel(self.cadreLabel)

        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        self.lblLabelCourant.setStyleSheet('color: #f05a24')
        self.lblLabelCourant.setFixedWidth(250)
        font.setBold(True)
        self.lblLabelCourant.setFont(font)
        self.lblLabelCourant.move(50, 53)

        #  Bouton d'administration des labels
        self.btnAdmiValid1 = QPushButton(self.cadreLabel)
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiValid1.setFixedSize(39, 39)
        self.btnAdmiValid1.setIconSize(QSize(33, 33))
        self.btnAdmiValid1.move(10, 80)
        self.btnAdmiValid1.setCursor(Qt.PointingHandCursor)
        self.btnAdmiValid1.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiValid1.clicked.connect(self.evt_btnAdmiValid1_clicked)

        #
        self.btnAdmiPlus1 = QPushButton(self.cadreLabel)
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus1.setFixedSize(39, 39)
        self.btnAdmiPlus1.setIconSize(QSize(33, 33))
        self.btnAdmiPlus1.move(55, 80)
        self.btnAdmiPlus1.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus1.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus1.clicked.connect(self.evt_btnAdmiPlus1_clicked)
        #
        self.btnAdmiModif1 = QPushButton(self.cadreLabel)
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif1.setFixedSize(39, 39)
        self.btnAdmiModif1.setIconSize(QSize(33, 33))
        self.btnAdmiModif1.move(100, 80)
        self.btnAdmiModif1.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif1.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif1.clicked.connect(self.evt_btnAdmiModif1_clicked)
        #
        self.btnAdmiSuppr1 = QPushButton(self.cadreLabel)
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr1.setFixedSize(39, 39)
        self.btnAdmiSuppr1.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr1.move(145, 80)
        self.btnAdmiSuppr1.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr1.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr1.clicked.connect(self.evt_btnAdmiSuppr1_clicked)

        #  GroupBox des labels
        grpLstLabel = QGroupBox(self.cadreLabel)
        grpLstLabel.setFixedSize(260, 300)
        grpLstLabel.move(10, 130)
        grpLstLabel.setStyleSheet('background-color: #222222; border: 0px')
        # grpLstClasseur.
        lyt = QVBoxLayout()
        grpLstLabel.setLayout(lyt)
        # Liste des labels
        self.lstLabel = QListWidget()
        self.lstLabel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lstLabelIndex = -1
        self.cleLabelTemp = -1
        self.nomLabelTemp = ''
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lstLabel.setFont(font)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.lstLabel.setStyleSheet(style)
        lyt.addWidget(self.lstLabel)
        self.lstLabel.itemClicked.connect(self.evt_lstLabel_currentItemChanged)
        # *********************************************************************************************
        #  Cadre Aide
        # *********************************************************************************************
        self.grpCadreAide1 = QGroupBox(self.cadreLabel)
        self.grpCadreAide1.setFixedSize(340, 400)
        self.grpCadreAide1.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadreAide1.move(280, 20)
        #  Titre Aide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        lblAide = QLabel(self.grpCadreAide1)
        lblAide.setFont(font)
        lblAide.setText('Aide')
        lblAide.setStyleSheet('color: white; border: 0px')
        lblAide.move(20, 25)
        # textAide
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        lblTextAide = QLabel(self.grpCadreAide1)
        lblTextAide.setWordWrap(True)
        lblTextAide.setFixedSize(300, 75)
        lblTextAide.setStyleSheet('background-color: #222222; color: #777777; border: 0px')
        aux = 'Sélectionne le label de la vidéo'
        lblTextAide.setText(aux)
        lblTextAide.setFont(font)
        lblTextAide.move(20, 60)
        #  Aide icones
        #  Valid
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        lblValid = QLabel(self.grpCadreAide1)
        lblValid.setFixedSize(39, 39)
        lblValid.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiValid2')
        img = img.scaled(33, 33)
        lblValid.setPixmap(img)
        lblValid.move(20, 160)
        lblAideValid = QLabel(self.grpCadreAide1)
        lblAideValid.setStyleSheet('border: 0px; color: #777777')
        lblAideValid.setFont(font)
        lblAideValid.setText('Sélectionne le label de votre vidéo')
        lblAideValid.move(70, 170)
        #  Plus
        lblPlus = QLabel(self.grpCadreAide1)
        lblPlus.setFixedSize(39, 39)
        lblPlus.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiPlus2')
        img = img.scaled(33, 33)
        lblPlus.setPixmap(img)
        lblPlus.move(20, 210)
        lblAidePlus = QLabel(self.grpCadreAide1)
        lblAidePlus.setStyleSheet('border: 0px; color: #777777')
        lblAidePlus.setFont(font)
        lblAidePlus.setText('Ajouter un nouveau label.')
        lblAidePlus.move(70, 220)
        #  Modif
        lblModif = QLabel(self.grpCadreAide1)
        lblModif.setFixedSize(39, 39)
        lblModif.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiModif2')
        img = img.scaled(33, 33)
        lblModif.setPixmap(img)
        lblModif.move(20, 260)
        lblAideModif = QLabel(self.grpCadreAide1)
        lblAideModif.setStyleSheet('border: 0px; color: #777777')
        lblAideModif.setFont(font)
        lblAideModif.setText('Editer le label sélectionné')
        lblAideModif.move(70, 270)
        #  Supprimer
        lblSuppr = QLabel(self.grpCadreAide1)
        lblSuppr.setFixedSize(39, 39)
        lblSuppr.setStyleSheet('border: 0px')
        img = QPixmap('ressources/admiSuppr2')
        img = img.scaled(33, 33)
        lblSuppr.setPixmap(img)
        lblSuppr.move(20, 310)
        lblAideSuppr = QLabel(self.grpCadreAide1)
        lblAideSuppr.setStyleSheet('border: 0px; color: #777777')
        lblAideSuppr.setFont(font)
        lblAideSuppr.setText('Supprimer le label sélectionnée')
        lblAideSuppr.move(70, 320)
        # *********************************************************************************************
        #  Cadre Plus
        # *********************************************************************************************
        self.grpCadrePlusLabel = QGroupBox(self.cadreLabel)
        self.grpCadrePlusLabel.setFixedSize(340, 450)
        self.grpCadrePlusLabel.setStyleSheet('background-color: #222222; border-left: 1px solid #444444;')
        self.grpCadrePlusLabel.move(280, 20)
        #  Titre Plus
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.lblPlusLabel = QLabel(self.grpCadrePlusLabel)
        self.lblPlusLabel.setFont(font)
        self.lblPlusLabel.setText('Créer un nouveau label')
        self.lblPlusLabel.setStyleSheet('color: white; border: 0px')
        self.lblPlusLabel.move(20, 25)
        self.grpCadrePlusLabel.setVisible(False)
        #  Titre plus Nom
        lblTitrePlusLabel = QLabel(self.grpCadrePlusLabel)
        lblTitrePlusLabel.setStyleSheet('QPushButton {background: transparent; color: white}')
        lblTitrePlusLabel.setText('Nom et couleur du label')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitrePlusLabel.setFont(font)
        lblTitrePlusLabel.move(20, 75)
        #  Saisie Pastille couleur
        pixmap = self.drawPastille(8, '#ffffff')
        self.btnColor = QPushButton(self.grpCadrePlusLabel)
        self.btnColor.setCursor(Qt.PointingHandCursor)
        self.btnColor.setStyleSheet('QPushButton {background: transparent}')
        self.btnColor.setIcon(QIcon(pixmap))
        self.btnColor.setFixedSize(18, 18)
        self.btnColor.move(20, 107)
        self.btnColor.clicked.connect(self.showColorDialog)
        #  Saisie Plus Nom
        self.lnePlusLabelNom = QLineEdit(self.grpCadrePlusLabel)
        self.lnePlusLabelNom.setStyleSheet('background: #666666; border-radius: 5px; color: white')
        self.lnePlusLabelNom.setFixedSize(260, 25)
        self.lnePlusLabelNom.move(60, 105)
        #  Titre plus commentaire
        lblTitrePlusLabel1 = QLabel(self.grpCadrePlusLabel)
        lblTitrePlusLabel1.setStyleSheet('background: transparent; color: white')
        lblTitrePlusLabel1.setText('Note du label')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitrePlusLabel1.setFont(font)
        lblTitrePlusLabel1.move(20, 155)
        #  Saisie Plus Note
        self.lnePlusLabelNote = QTextEdit(self.grpCadrePlusLabel)
        self.lnePlusLabelNote.setStyleSheet('background: #666666; border-radius: 5px; color: white')
        self.lnePlusLabelNote.setFixedSize(300, 140)
        self.lnePlusLabelNote.move(20, 185)
        # Boutons Enregistrer Annuler
        self.btnSauverLabel = QPushButton(self.grpCadrePlusLabel)
        self.btnSauverLabel.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSauverLabel.setFixedSize(100, 35)
        self.btnSauverLabel.setText('Enregistrer')
        self.btnSauverLabel.move(20, 380)
        self.btnSauverLabel.clicked.connect(self.evt_btnSauverLabel_clicked)
        #
        self.btnAnnulerLabel = QPushButton(self.grpCadrePlusLabel)
        self.btnAnnulerLabel.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                        'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnAnnulerLabel.setFixedSize(100, 35)
        self.btnAnnulerLabel.setText('Annuler')
        self.btnAnnulerLabel.move(140, 380)
        self.btnAnnulerLabel.clicked.connect(self.evt_btnAnnulerLabel_clicked)

        self.populateLstLabel()
        self.cadreLabel.setVisible(False)

    def drawPastille(self, radius, color):
        if color == '':
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor('#ffffff'))
            painter.setPen(pen)
            brush = QBrush(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            pen = QPen(QColor('#ff0000'), 2, Qt.SolidLine)
            painter.setPen(pen)
            brush = QBrush(QColor('#ff0000'))
            painter.setBrush(brush)
            painter.drawLine(1, radius + 2, radius * 2 + 4, radius + 2)
            del painter
        else:
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor(color))
            painter.setPen(pen)
            brush = QBrush(QColor(color))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2*radius, 2*radius)
            del painter
        return pixmap


    def evt_btnAdmiValid_clicked(self):
        self.grpCadreAide.setVisible(True)
        if self.cleClasseurTemp == -1:
            return
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid1.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de sélectionner un nouveau classeur. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte du nouveau classeur
            indexCour = self.lstClasseur.currentItem().data(Qt.UserRole)
            nom = self.lstClasseur.currentItem().text()
            self.lblClasseurCourant.setText(nom)
            self.videoRecordCour.nomClasseur = nom
            self.videoRecordCour.cleClasseur = indexCour
        else:
            pass
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.cleClasseurTemp = -1

    def evt_btnAdmiValid1_clicked(self):
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid1.png'))
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        if self.cleLabelTemp == -1:
            return
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid1.png'))

        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de sélectionner un nouveau label. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte du nouveau label
            query = QSqlQuery()
            query.exec(f'SELECT * FROM statutTab WHERE cle={self.cleLabelTemp}')
            color = ''
            if query.next():
                color = query.value('color')
            self.lblPastille.setPixmap(self.drawPastille(8, color))
            indexCour = self.lstLabel.currentItem().data(Qt.UserRole)
            nom = self.lstLabel.currentItem().text()
            self.lblLabelCourant.setText(nom.strip())
            self.videoRecordCour.nomStatut = nom
            self.videoRecordCour.statut = indexCour
            # MaJ dans informations générales
            self.lblLabelVideo.setText('         ' + nom)
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, color))
        else:
            #  On garde l'ancien classeur
            pass
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.cleLabelTemp = -1

    def closeEvent(self, event):
        self.sauveModifVideo()

    def sauveModifVideo(self):
        #  enregistrement des données qui ont été modifiées dans videoFileTab
        query = QSqlQuery()
        self.videoRecordCour.note = self.lblNoteVideo.rating
        self.videoRecordCour.Favori = self.lblFavoriVideo.boolFavori
        tptData =(self.videoRecordCour.statut, self.videoRecordCour.note, self.videoRecordCour.Favori,
                  self.videoRecordCour.cleClasseur)
        tplChamps = ('statut', 'Note', 'Favori', 'cleClasseur')
        bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tptData} WHERE cle={self.videoRecordCour.cle}')

    def evt_btnAdmiPlus_clicked(self):
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus1.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.lnePlusClasseurNom.setText('')
        self.lnePlusClasseurNote.setText('')
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusClasseur.setVisible(True)
        self.lblPlusClasseur.setText('Créer un  classeur')
        self.boolModif = False

    def evt_btnAdmiPlus1_clicked(self):
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus1.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.lblPlusLabel.setText('Créer un nouveau label')
        self.lnePlusLabelNom.setText('')
        self.lnePlusLabelNote.setText('')
        self.grpCadreAide1.setVisible(False)
        self.grpCadrePlusLabel.setVisible(True)
        self.boolModif = False

    def evt_btnAdmiModif_clicked(self):
        if self.cleClasseurTemp == -1:
            return
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusClasseur.setVisible(True)
        self.lblPlusClasseur.setText('Modifier un classeur')
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif1.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM classeurTab WHERE cle={self.cleClasseurTemp}')
        if query.next():
            self.lnePlusClasseurNom.setText(query.value('nom'))
            self.lnePlusClasseurNote.setText(query.value('commentaire'))

    def evt_btnAdmiModif1_clicked(self):
        self.grpCadreAide1.setVisible(False)
        self.grpCadrePlusLabel.setVisible(True)
        self.lblPlusLabel.setText('Modifier un label')
        if self.cleLabelTemp == -1:
            return
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif1.png'))
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab WHERE cle={self.cleLabelTemp}')
        if query.next():
            self.lnePlusLabelNom.setText(query.value('nom'))
            self.lnePlusLabelNote.setText(query.value('commentaire'))
            if self.is_color_valid(query.value('color')):
                self.colorLabel = query.value('color')
            else:
                self.colorLabel = '#ffffff'
            self.btnColor.setIcon(QIcon(self.drawPastille(8, self.colorLabel)))

    def showColorDialog(self):
        colorDialog = QColorDialog()

        color = colorDialog.getColor(QColor('red'), self.grpCadrePlusLabel)
        self.colorLabel = ''
        if self.is_color_valid(color.name()):
            self.colorLabel = color.name()
            self.btnColor.setIcon(QIcon(self.drawPastille(8, color.name())))

    def is_color_valid(self, color_string):
        color = QColor(color_string)
        return color.isValid()

    def evt_btnAdmiSuppr1_clicked(self):
        if self.cleLabelTemp == -1:
            return
        self.lblPlusLabel.setText('Supprimer un label')
        self.grpCadreAide1.setVisible(False)
        self.grpCadrePlusLabel.setVisible(True)
        self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus1.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr1.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab WHERE cle={self.cleLabelTemp}')
        if query.next():
            self.lnePlusLabelNom.setText(query.value('nom'))
            self.lnePlusLabelNote.setText(query.value('commentaire'))
        self.btnSauverLabel.setVisible(False)
        self.btnAnnulerLabel.setVisible(False)

        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de supprimer un label. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte du nouveau classeur
            indexCour = self.lstLabel.currentItem().data(Qt.UserRole)
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM statutTab WHERE cle = {indexCour}')
        else:
            pass
        self.btnSauverLabel.setVisible(True)
        self.btnAnnulerLabel.setVisible(True)
        self.btnAdmiSuppr1.setIcon(QIcon('ressources/admiSuppr.png'))
        self.lnePlusLabelNom.setText('')
        self.lnePlusLabelNote.setText('')
        self.grpCadrePlusLabel.setVisible(False)
        self.grpCadreAide1.setVisible(False)
        self.populateLstLabel()
        self.cleLabelTemp = -1

    def evt_btnAdmiSuppr_clicked(self):
        if self.cleClasseurTemp == -1:
            return
        self.grpCadreAide.setVisible(False)
        self.grpCadrePlusClasseur.setVisible(True)
        self.lblPlusLabel.setText('Supprimer un classeur')
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr1.png'))
        self.boolModif = True
        query = QSqlQuery()
        query.exec(f'SELECT * FROM classeurTab WHERE cle={self.cleClasseurTemp}')
        if query.next():
            self.lnePlusClasseurNom.setText(query.value('nom'))
            self.lnePlusClasseurNote.setText(query.value('commentaire'))
        self.btnSauverClasseur.setVisible(False)
        self.btnAnnulerClasseur.setVisible(False)

        self.dialog = DialogCustom(self, 100, 100)
        aux = 'Vous êtes en train de supprimer un classeur. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Prise en compte du nouveau classeur
            indexCour = self.lstClasseur.currentItem().data(Qt.UserRole)
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM classeurTab WHERE cle = {indexCour}')
        else:
            pass
        self.btnSauverClasseur.setVisible(True)
        self.btnAnnulerClasseur.setVisible(True)
        self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.lnePlusClasseurNom.setText('')
        self.lnePlusClasseurNote.setText('')
        self.grpCadrePlusClasseur.setVisible(False)
        self.grpCadreAide.setVisible(True)
        self.populateLstClasseur()
        self.cleClasseurTemp = -1

    def evt_cmbStatut_currentIndexChanged(self, index):
        self.videoRecordCour.statut = self.cmbStatut.currentData()

    def evt_lstClasseur_currentItemChanged(self, current):
        try:
            self.btnAdmiValid.setIcon(QIcon('ressources/admiValid.png'))
            self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
            self.cleClasseurTemp = current.data(Qt.UserRole)
            self.nomClasseurTemp = current.text()
        except:
            pass

    def evt_lstLabel_currentItemChanged(self, current):
        try:
            self.btnAdmiValid1.setIcon(QIcon('ressources/admiValid.png'))
            self.btnAdmiModif1.setIcon(QIcon('ressources/admiModif.png'))
            self.cleLabelTemp = current.data(Qt.UserRole)
            self.nomLabelTemp = current.text()
        except:
            pass

    def populateLstClasseur(self):
        self.lstClasseur.clear()
        query = QSqlQuery()
        query.exec(f'SELECT * FROM classeurTab ORDER BY nom')
        while query.next():
            lbl = QLabel()
            lbl.setFixedSize(QSize(20, 17))
            lbl.setPixmap(QPixmap('ressources/dossier.png'))
            itemN = QListWidgetItem(self.lstClasseur)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(f'{query.value("nom")}')
            itemN.setData(Qt.UserRole, query.value('cle'))
            self.lstClasseur.addItem(itemN)
            # self.lstClasseur.setItemWidget(itemN, lbl)
        self.lstClasseur.setSpacing(4)
        #  Mise à jour du label courant
        self.videoRecordCour = VideoFileRecord(self.videoCour)
        aux = self.videoRecordCour.nomClasseur
        if aux != '':
            self.lblClasseurCourant.setText(aux)
        else:
            self.lblClasseurCourant.setText('Pas de classeur sélectionné')

    def populateLstLabel(self):
        self.lstLabel.clear()
        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab ORDER BY NOM')
        while query.next():
            lbl = PastilleSimple(None, 8, query.value("color"))
            itemN = QListWidgetItem(self.lstLabel)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(f'     {query.value("nom")}')
            itemN.setData(Qt.UserRole, query.value('cle'))
            self.lstLabel.addItem(itemN)
            self.lstLabel.setItemWidget(itemN, lbl)
        self.lstLabel.setSpacing(7)
        #  Mise à jour du label courant
        self.videoRecordCour = VideoFileRecord(self.videoCour)
        aux = self.videoRecordCour.nomStatut

        if self.videoRecordCour.statut == -1:
            self.lblLabelCourant.setText('Aucun label')
            self.lblPastille.setPixmap(self.drawPastille(8, ''))
        else:
            self.lblLabelCourant.setText(aux)
            self.lblPastille.setPixmap(self.drawPastille(8, self.videoRecordCour.colorStatut))

    def populateCmbStatut(self):
        statutCour = self.videoRecordCour.statut
        self.cmbStatut.clear()
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM statutTab ORDER BY nom')
        i = 0
        indexCour = 0
        while query.next():
            icon = QIcon(self.drawPastille(8, QColor(query.value('color'))))
            self.cmbStatut.addItem(icon, query.value('nom'), query.value('cle'))

        self.cmbStatut.setCurrentIndex(indexCour)

        # self.cmbStatut.setStyleSheet('QComboBox::item { height: 40px;}')

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

        #  ***************************************************************************
        #  Top Zone
        #  ***************************************************************************
        btnSize = QSize(32, 20)
        btnSizea = QSize(70, 20)
        btnSize1 = QSize(80, 20)
        btnSize2 = QSize(100, 25)
        #
        self.btnMarquePage = QPushButton('Marque Page', self)
        self.btnMarquePage.setIcon(QIcon('ressources/marquePage.png'))
        self.btnMarquePage.setFixedSize(btnSize2)
        self.btnMarquePage.move(10, 10)
        self.btnMarquePage.setStyleSheet('color: white')
        self.lytTop.addWidget(self.btnMarquePage)
        self.lytTop.addSpacing(50)
        #
        self.btnRetour = QPushButton('Retour', self)
        self.btnRetour.move(80, 10)
        self.btnRetour.setVisible(False)
        self.lytTop.addWidget(self.btnRetour)
        self.lytTop.addSpacing(50)
        #
        self.chkImage = QCheckBox('Images', self)
        self.chkImage.setStyleSheet('color: white')
        self.chkImage.move(140, 10)
        self.chkImage.setChecked(True)
        self.chkImage.repaint()
        self.lytTop.addWidget(self.chkImage)
        #
        # self.chkLien = QCheckBox('Liens', self)
        # self.chkLien.setStyleSheet('color: white')
        # self.chkLien.setChecked(True)
        # self.chkLien.move(220, 10)
        # self.lytTop.addWidget(self.chkLien)
        #
        self.chkNote = QCheckBox('Notes', self)
        self.chkNote.move(300, 10)
        self.chkNote.setChecked(True)
        self.chkNote.setStyleSheet('color: white')
        self.lytTop.addWidget(self.chkNote)
        #
        self.chkTitre = QCheckBox('Titres', self)
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
        #  Ancienne méthode
        # self.objNote = ObjNote1(self, self.videoID)
        #  Nouvelle méthode
        self.objNote = AtelierParagraph(self, self.videoID)

        self.lytNote.addWidget(self.objNote)
        self.repaint()
        self.unsetCursor()

    def majChkNote(self):
        try:
            mainXX = mainWindow.tabObjetScreen.docParagraph.widget()
            mainXX.objNote.initChkNote(self.chkImage.isChecked(), self.chkNote.isChecked(), self.chkTitre.isChecked())
            mainXX.objNote.populateParagraph(self.videoID)
        except:
            pass

    def loadNotes(self):
        # return
        # self.objNote.effacer()
        self.objNote.populateParagraph(formScreen1.videoID)
        # self.objNote.populateObjNote(formScreen1.videoID)

    def evt_btnMarquePage_clicked(self):
        # self.objNote.effacer()
        # self.objNote.populateObjNote()
        print(self.videoID)

    def evt_btnRetour_clicked(self):
        fileAttenteVideo.pop()
        cleVideo, cleLien = fileAttenteVideo[len(fileAttenteVideo) - 1]
        if len(fileAttenteVideo) == 1:
            self.btnRetour.setVisible(False)
        self.parent.videoID = cleVideo
        formScreen1.loadVideo(cleVideo)
        self.videoID = cleVideo
        self.loadNotes()
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
        self.setWindowTitle('Module Paragraph')
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
                grpBouton.setFixedSize(425, 30)
                self.layout.addWidget(grpBouton)
                self.icon = QIcon('ressources/modif.png')
                # aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModifTitre0 = BoutonIndex(grpBouton, timeNote, self.videoID)
                # print(timeNote, self.videoID)
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
                self.btnPlayNoteTitre0.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
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
                # documentSize = tedNote.document().size()
                # tedNote.setFixedHeight(int(documentSize.height() + 10))
                tedNote.setStyleSheet('background: #111111; color: white; border: 0px')
                # tedNote.move(50, int(self.top))
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
                    self.btnModifTitre1.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
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
                    self.btnPlayNoteTitre1.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
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
            # mainXX = mainWindow.tabObjetScreen
            if imageAux != None and self.chkImage:
                #  Récupération du cemin complet de la video pour extraction
                query1 =QSqlQuery()
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
                img = extractPicture(videoPath, 423, 249, timeNote)
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
                    self.btnModifPicture.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
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
                    self.btnPlayNotePicture.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
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

    def evt_fullScreen_clicked(self):
        dlgFullScreen = QDialog(self)
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
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            img = extractPicture(videoPath, 700, 500, timeCode)
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
            # print(self, videoPath, self.videoID, self.timeNoteCour, False)
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
# ***************                O B J N O T E  1           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ObjNote1(QMainWindow):
    def __init__(self, parent, videoID):
        super().__init__()
        self.parent = parent
        self.setFixedWidth(520)
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 200
        self.setWindowIcon(QIcon("icon.png"))
        self.videoID = videoID
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.videoPath = ''

        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        self.scrollArea.setStyleSheet(styleQScrollBar)

        self.populateObjNote(videoID)

    def populateObjNote(self, cleVideo):
        self.effacer()
        listTimeNote = []
        self.listWidget = []
        i = 0
        #  Génération des Notes
        query = QSqlQuery()
        bOk = query.exec(f'SELECT DISTINCT timeNote FROM paragraph WHERE cleVideo = {cleVideo} ORDER BY timenote')
        while query.next():
            listTimeNote.append(query.value('timeNote'))
        for timeNote in listTimeNote:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM paragraph WHERE cleVideo={cleVideo} AND timeNote={timeNote}')
            titreAux = None
            imageAux = None
            texteAux = None
            lienWebAux = None
            boolModif = True
            while query.next():
                aux = ParagrapheRecord(query.value('cle'))
                if aux.titre:
                    titreAux = aux
                if aux.picture:
                    imageAux = aux
                if aux.note:
                    texteAux = aux
                if aux.lienWeb:
                    lienWebAux = aux
            if titreAux != None:
                if self.parent.chkTitre.isChecked():
                    boolModif = True
                    noteTitre = NoteTitre(self, titreAux.cle, boolModif)
                    self.vbox.addWidget(noteTitre)
                    self.listWidget.append(noteTitre)
                boolModif = False
            if imageAux != None:
                if self.parent.chkImage.isChecked():
                    query1 = QSqlQuery()
                    query1.exec(f'SELECT * FROM videoFileTab WHERE cle={cleVideo}')
                    if query1.next():
                        videoPath = self.parent.mainWin.racine + query1.value('internalPath') + \
                                    query1.value('videoName')
                    notePicture = NotePicture(self, timeNote=imageAux.timeNote, picture=imageAux.picture,
                                              texte=imageAux.texte, cle=imageAux.cle, videoPath=videoPath,
                                              videoID=cleVideo, icone=imageAux.icone, indentation=imageAux.indentation,
                                              boolModif=boolModif)
                    self.vbox.addWidget(notePicture)
                    self.listWidget.append(notePicture)
                boolModif = False
            if texteAux != None:
                if self.parent.chkNote.isChecked():
                    noteTexte = NoteTitre(self, texteAux.cle, boolModif)
                    self.vbox.addWidget(noteTexte)
                    self.listWidget.append(noteTexte)
            if lienWebAux != None:
                if self.parent.chkLien.isChecked():
                    noteLienWeb = NoteLienWeb(self, lienWebAux.cle, boolModif)
                    self.vbox.addWidget(noteLienWeb)
                    self.listWidget.append(noteLienWeb)

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)
        vsb = self.scrollArea.verticalScrollBar()

        formScreen1.marqueNote.populateMarqueNote()

    def effacer(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().deleteLater()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             N O T E T I T R E             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NoteTitre(QTextEdit):
    def __init__(self, parent, paragraphID, boolModif):
        super(NoteTitre, self).__init__()
        self.parent = parent
        self.paragraphID = paragraphID
        self.setFixedSize(480, 200)
        self.videoID = formScreen1.videoID
        self.adjustSize()
        # self.setWordWrap(True)
        cursorPlay = QCursor(QPixmap('ressources/playCursor.png'))
        # self.setCursor(QCursor(cursorPlay))
        self.searchString = formScreen1.searchString
        self.boolModif = boolModif
        self.marqueCour = 0
        self.viewport().installEventFilter(self)
        self.textChanged.connect(self.evt_textChanged)
        self.setupUI()

    def setupUI(self):
        self.paragraphCour = ParagrapheRecord(self.paragraphID)
        self.texte = self.paragraphCour.texte
        self.marqueCour = self.paragraphCour.timeNote

        self.lstFontSize = [16, 12, 10, 8, 7]

        if self.paragraphCour.titre:  # texte de type titre
            if self.paragraphCour.indentation == 0 and self.paragraphCour.timeNote == 0:  # Titre global de la vidéo
                self.setText(self.paragraphCour.texte)
                self.setAlignment(Qt.AlignCenter)
                texte = self.paragraphCour.texte.replace('$$', chr(10))
                texte = texte.replace(')|', chr(34))
                texte = texte.replace('µµ', chr(9))
                texteTag = self.majTag(texte)
                # texteTag = texteTag.replace(chr(10), '\n')
                self.setText("<p><br>" + str(texteTag) + "</p>")
                self.setStyleSheet(f'font-size: 20pt; border: 1px solid white++;'
                                   f'font-family: Arial; font-weight: normal; margin-bottom: 40px; color: white; ')
                #
                self.icon = QIcon('ressources/modif.png')
                #
                aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModif = QPushButton(aux, self)
                self.btnModif.setIcon(self.icon)
                self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                            'border-style: solid; border-color: gray; border-width: 0px;'
                                            'background-color: #201F1F')
                self.btnModif.setFixedSize(25, 25)
                #
                self.icon = QIcon('ressources/playNote.png')
                self.btnPlayNote = QPushButton(aux, self)
                self.btnPlayNote.setIcon(self.icon)
                self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                            'border-style: solid; border-color: gray; border-width: 0px;'
                                            'background-color: #201F1F')
                self.btnPlayNote.setFixedSize(25, 25)

                if self.paragraphCour.indentation == 0 and self.paragraphCour.titre:
                    self.btnModif.move(5, 5)
                    self.btnPlayNote.move(35, 5)
                if self.paragraphCour.indentation == 0 and self.paragraphCour.note:
                    self.btnModif.move(0, -20)
                self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnPlayNote.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnPlayNote.clicked.connect(self.evt_btnPlayNote_clicked)
                self.btnModif.clicked.connect(self.evt_btnModif_clicked)
                self.btnModif.setVisible(self.boolModif)
                self.btnPlayNote.setVisible(self.boolModif)

            else:  # titre de pararagraphe
                if not self.parent.parent.chkTitre.isChecked():
                    return
                offset = 0
                texte = self.paragraphCour.texte.replace('$$', chr(10))
                texte = texte.replace(')|', chr(34))
                texte = texte.replace('µµ', chr(9))
                # texteTag = self.majTag(texte)
                texteTag = self.majTag(texte)
                self.setText("<p>" + str(texteTag) + "</p>")
                self.setStyleSheet(
                    f'font-size: 14pt; font-family: Arial; '
                    f'margin-left: {offset}px; font-weight: normal; margin-top: 0px; margin-bottom: 0px;'
                    f'; color: white;')
                self.setMinimumHeight(95)
                # ***************************************************************************************
                #
                self.icon = QIcon('ressources/modif.png')
                aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModif = QPushButton(aux, self)
                self.btnModif.setIcon(self.icon)
                self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                            'border-style: solid; border-color: gray; border-width: 0px;'
                                            'background-color: #201F1F')
                self.btnModif.setFixedSize(25, 25)
                self.btnModif.move(5, 5)
                self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                #
                self.icon = QIcon('ressources/playNote.png')
                self.btnPlayNote2 = QPushButton(aux, self)
                self.btnPlayNote2.setIcon(self.icon)
                self.btnPlayNote2.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                               'border-style: solid; border-color: gray; border-width: 0px;'
                                               'background-color: #201F1F')
                self.btnPlayNote2.setFixedSize(25, 25)
                self.btnPlayNote2.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnPlayNote2.move(35, 5)

                self.btnModif.clicked.connect(self.evt_btnModif_clicked)
                self.btnPlayNote2.clicked.connect(self.evt_btnPlayNote_clicked)
                self.btnModif.setVisible(self.boolModif)
                self.btnPlayNote2.setVisible(self.boolModif)

        else:
            if self.paragraphCour.note:  # texte de type Note
                if not self.parent.parent.chkTitre.isChecked():
                    return
                self.setStyleSheet(f'font-size: 9pt; font-family: Arial; margin-left: 0px; font-weight: normal; '
                                   f'margin-top: 10px; color: white;')
                # self.setFixedHeight(100)
                query1 = QSqlQuery()
                ok = query1.exec(f'SELECT mot, URL FROM linkTab WHERE timecode={self.marqueCour} AND cleVideo={self.videoID}')
                self.listTpl = []
                while query1.next():
                    self.listTpl.append((query1.value('mot'), query1.value('URL')))

                aux = self.paragraphCour.texte
                aux = aux.replace("²", "'")
                aux = aux.replace('<br>', '')
                aux = aux.replace("&#09", "\t")
                self.setText('<br>' + aux)

                self.icon = QIcon('ressources/modif.png')
                aux = strTime(self.paragraphCour.timeNote)
                aux = ''
                self.btnModif = QPushButton(aux, self)
                self.btnModif.setIcon(self.icon)
                self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                            'border-style: solid; border-color: gray; border-width: 0px;'
                                            'background-color: #201F1F')
                self.btnModif.setFixedSize(25, 25)
                self.btnModif.move(5, 5)
                #
                self.icon = QIcon('ressources/playNote.png')
                self.btnPlayNote3 = QPushButton(aux, self)
                self.btnPlayNote3.setIcon(self.icon)
                self.btnPlayNote3.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                                'border-style: solid; border-color: gray; border-width: 0px;'
                                                'background-color: #201F1F')
                self.btnPlayNote3.setFixedSize(25, 25)
                self.btnPlayNote3.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnPlayNote3.move(35, 5)

                self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
                self.btnModif.clicked.connect(self.evt_btnModif_clicked)
                self.btnPlayNote3.clicked.connect(self.evt_btnPlayNote_clicked)
                self.btnModif.setVisible(self.boolModif)
                self.btnPlayNote3.setVisible(self.boolModif)

    # def updateSize(self):
    #     content_height = self.document().size().height()
    #     scroll_height = self.verticalScrollBar().pageStep()
    #     new_height = content_height + scroll_height
    #     self.setFixedHeight(int(new_height))

    def evt_textChanged(self):
        self.update()
        documentSize = self.document().size()
        # print(documentSize.height())
        # self.setFixedHeight(int(documentSize.height() + 10))
        # self.setFixedHeight(162)

    def eventFilter(self, source, event):
        try:
            if source is self.viewport() and event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    cursor = self.cursorForPosition(event.pos())
                    cursor.select(QTextCursor.WordUnderCursor)
                    selected_text = cursor.selectedText()
                    format = cursor.charFormat()
                    if format.fontWeight() == QFont.Bold and format.fontUnderline():
                        for tpl in self.listTpl:
                            lien, URL = tpl
                            if selected_text in lien:
                                QDesktopServices.openUrl(QUrl(URL))
                    else:
                        pass
        except:
            pass
        return super().eventFilter(source, event)

    def evt_btnModif_clicked(self):
        query = QSqlQuery()
        bOk = query.exec(
            f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.paragraphCour.cleVideo}')

        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.paragraphCour.cleVideo,
                                          self.marqueCour, False)
            formGererNote.populateNoteModif()
            formGererNote.show()

    # def mousePressEvent(self, e):
    def evt_btnPlayNote_clicked(self):
        # if e.button() == Qt.LeftButton:  # lecture de la vidéo à partir du timeNote de l'image
        formScreen1.mediaPlayer.setPosition(self.paragraphCour.timeNote * 1000)
        formScreen1.marqueNote.testMarque(-self.paragraphCour.timeNote + 5)
        if formScreen1.mediaPlayer.state() == QMediaPlayer.PlayingState:
            formScreen1.mediaPlayer.pause()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            formScreen1.mediaPlayer.setPlaybackRate(formScreen1.vitesseCour)
            formScreen1.mediaPlayer.play()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def majusculeSansAccent(self, chaine):
        txt = chaine.upper()
        chnorm = normalize('NFKD', txt)
        return "".join([c for c in chnorm if not combining(c)])

    def majTag(self, texte):
        #  Initialiser startHTML et end HTML
        texte = texte.replace(chr(10), '<br>')
        startHTML = "<font color= \'#66cccc\'>"
        endHTML = "</font>"
        lenStart = len("<font color= \'#66cccc\'>")
        lenEnd = len("</font>")
        #  Charger la liste des tags de la vidéos
        lstTags = []
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM tagTab WHERE cleVideo = {self.paragraphCour.cleVideo}')
        if bOk:
            while query.next():
                lstTags.append(query.value('mot'))
        lenTexte = len(texte) - 1
        #
        # for tag in lstTags:
        #     ret = 0
        #     index = 0
        #     while ret != -1:
        #         ret = texte.find(tag, index)
        #         if ret != -1:
        #             texte = texte[:ret] + startHTML + texte[ret:]
        #             index = ret + len(tag) + lenStart
        #             texte = texte[:index] + endHTML + texte[index:]
        #             index += lenEnd
        return texte


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            N O T E P I C T U R E          ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NotePicture(QGroupBox):
    def __init__(self, parent, timeNote=None, picture=None, cle=None, videoPath=None, videoID=None, icone=None,
                 contenant=None, texte=None, indentation=None, boolModif=False, pointeur=None):
        QGroupBox.__init__(self, parent)
        self.parent = parent
        self.timeNote = timeNote
        self.picture = picture
        self.cle = cle
        self.videoPath = videoPath
        self.videoID = videoID
        self.icone = icone
        self.texte = texte
        self.largeur = 423
        self.hauteur = 249
        self.indentation = indentation
        self.imageIni = None
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.originQpoint = QPoint()
        self.boolZoom = False
        self.boolModif = boolModif
        self.setStyleSheet('border:1px;')
        cursorPlay = QCursor(QPixmap('ressources/playCursor.png'))

        self.paragraphCour = ParagrapheRecord(cle)
        # , timeNote, 0, False, True, texte, icone, None, videoID, False)

        # self.setFixedSize(QSize(637, 329))
        self.setFixedSize(QSize(637, 260))
        grpBoxBtn = QGroupBox(self)
        grpBoxBtn.setStyleSheet('background-color: #111111')
        grpBoxBtn.setFixedSize(637, 30)
        grpBoxBtn.move(0, 0)
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        self.lblPicture = QLabel(self)
        self.lblPicture.setFixedSize(QSize(self.largeur, self.hauteur))
        self.lblPicture.move(0, 0)
        self.lblPicture.setStyleSheet('border-width:1px; border-color: gray; border-style: solid; border-radius:4px;'
                                      ' margin-top:0')
        img = extractPicture(videoPath, self.hauteur, self.largeur, timeNote)
        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.pixmap01 = QPixmap.fromImage(qimg)
        self.lblPicture.setPixmap(self.pixmap01.scaled(self.largeur, self.hauteur, Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation))
        self.imageIni = self.pixmap01.scaled(self.largeur, self.hauteur, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if texte != '':
            lblCommentaire = QLabel(self)
            lblCommentaire.setStyleSheet('background: #111111; color: #aaaaaa')
            lblCommentaire.setText(texte)
            lblCommentaire.move(0, 235)

        # bt modif
        # self.icon = QIcon('ressources/modif.png')
        # self.btnModif = QPushButton(grpBoxBtn)
        # self.btnModif.setIcon(self.icon)
        # self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
        #                             'border-style: solid; border-color: gray; border-width: 0px;'
        #                             'background-color: transparent')
        # self.btnModif.setFixedSize(25, 25)
        # self.btnModif.move(5, 5)
        # self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btnModif.setVisible(self.boolModif)
        # #
        # self.icon = QIcon('ressources/playNote.png')
        # self.btnPlayNote = QPushButton(self)
        # self.btnPlayNote.setIcon(self.icon)
        # self.btnPlayNote.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
        #                                'border-style: solid; border-color: gray; border-width: 0px;'
        #                                'background-color: #201F1F')
        # self.btnPlayNote.setFixedSize(25, 25)
        # self.btnPlayNote.move(35, 5)
        # self.btnPlayNote.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btnPlayNote.setVisible(self.boolModif)


        #  bt zoom
        self.btnZoom = QPushButton('1:1', self)
        self.btnZoom.setFixedSize(QSize(25, 25))
        # self.btnZoom.move(580, 224)
        self.btnZoom.move(56, 15)
        self.btnZoom.setVisible(False)

        # self.btnModif.clicked.connect(self.evt_btnModif_clicked)
        self.btnZoom.clicked.connect(self.evt_btnZoom_clicked)
        # self.btnPlayNote.clicked.connect(self.evt_btnPlayNote_clicked)

    def evt_btnModif_clicked(self):
        query = QSqlQuery()
        bOk = query.exec(
            f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE cle={self.paragraphCour.cleVideo}')
        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formCreerNote = FormBlockNote(self, videoPath, self.paragraphCour.cleVideo,
                                          self.timeNote, False)
            # formCreerNote = FormGererNote(self, videoPath, self.paragraphCour.cleVideo,
            #                               self.timeNote, False)
            formCreerNote.populateNoteModif()
            formCreerNote.show()

    def evt_btnZoom_clicked(self, e):
        self.lblPicture.setPixmap(self.imageIni)
        self.btnZoom.setVisible(False)
        self.boolZoom = False

    def evt_btnPlayNote_clicked(self):
        formScreen1.mediaPlayer.setPosition(self.timeNote * 1000)
        formScreen1.marqueNote.testMarque(-self.paragraphCour.timeNote + 5)
        if formScreen1.mediaPlayer.state() == QMediaPlayer.PlayingState:
            formScreen1.mediaPlayer.pause()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            formScreen1.mediaPlayer.setPlaybackRate(formScreen1.vitesseCour)
            # mediaPlayer.setPlaybackRate(self.parent.parent.formScreen1.vitesseCour)
            formScreen1.mediaPlayer.play()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        # if e.button() == Qt.RightButton:  # demande de zoom
        #     # vérification que la souris est sur l'image
        #     if self.boolZoom:
        #         return
        #     if 54 < e.x() < 600:
        #         self.originQpoint = e.pos()
        #         self.currentQRubberBand.setGeometry(QRect(self.originQpoint, QSize()))
        #         self.currentQRubberBand.show()

    def mouseMoveEvent(self, e):
        if self.boolZoom:
            return
        if e.button() == Qt.LeftButton:
            return
        self.currentQRubberBand.setGeometry(QRect(self.originQpoint, e.pos()).normalized())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            return
        if not (3 < e.x() < 600):
            return
        if self.boolZoom:
            return
        self.boolZoom = True
        self.btnZoom.setVisible(True)
        self.currentQRubberBand.hide()
        currentRect = self.currentQRubberBand.geometry()
        y, x = currentRect.top() - 40, currentRect.left()  # - 200
        w, h = currentRect.width(), currentRect.height()  # rectangle initial à la souris
        h0 = h

        h1 = int(w / 1.7)
        if (w + x > self.largeur) or (h1 + y > self.hauteur):
            w = int(h * 1.7)
        else:
            h = h1
        h = h0
        # (w, h) dimensions rectifiées au ration 1.7
        try:
            fct = self.largeur / w  # calcul du facteur d'agrandissement
        except:
            return
        wGrd, hGrd = int(self.largeur * fct), int(self.hauteur * fct)
        imgGrd = self.pixmap01.scaled(wGrd, hGrd, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #  calcul du pt haut/gauche du rectangle dans l'image agrandie
        x, y = int(x * fct), int(y * fct)
        #  rectangle du crop
        pt = QPoint(x, y)
        dim = QSize(self.largeur, self.hauteur)
        dim = QSize(self.largeur, self.hauteur - 13)
        currentRect = QRect(pt, dim)
        imgCrop = imgGrd.copy(currentRect)
        self.lblPicture.setPixmap(imgCrop)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              N O T E L I E N W E B           ********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NoteLienWeb(QLabel):
    def __init__(self, parent, paragraphID, boolModif):
        super(NoteLienWeb, self).__init__()
        self.parent = parent
        self.paragraphID = paragraphID
        self.setFixedWidth(480)
        self.setFixedHeight(100)
        self.adjustSize()
        cursorPlay = QCursor(QPixmap('ressources/playCursor.png'))
        # self.setStyleSheet(f'background-color: orange')
        self.setCursor(QCursor(cursorPlay))
        self.boolModif = boolModif
        self.setupUI()

    def setupUI(self):
        self.paragraphCour = ParagrapheRecord(self.paragraphID)
        lytMain = QVBoxLayout()
        self.setLayout(lytMain)
        #  Bouton Modif
        self.icon = QIcon('ressources/modif.png')
        self.btnModif = QPushButton(self)
        self.btnModif.setIcon(self.icon)
        self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
                                    'border-style: solid; border-color: gray; border-width: 0px;'
                                    'background-color: #201F1F')
        lytMain.addWidget(self.btnModif)
        #  Note du lien
        lytNote = QHBoxLayout()
        lytMain.addLayout(lytNote)
        self.paragraphcour = ParagrapheRecord(self.paragraphID)
        self.texe = self.paragraphcour.texte
        self.marqueCour = self.paragraphcour.timeNote
        pixmap = QIcon('ressources/lienWeb.png')
        self.lblLienWeb = QPushButton()
        self.lblLienWeb.setIcon(pixmap)
        self.lblLienWeb.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet('QPushButton::Hover {background-color: gray} QPushButton {background-color: transparent}')
        lytNote.addWidget(self.lblLienWeb)
        self.lblURL = QLabel(self)
        self.lblURL.setText(self.paragraphcour.texte)
        lytNote.addWidget(self.lblURL)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytNote.addItem(spacerItem)

        self.btnModif.setFixedSize(25, 25)
        self.btnModif.move(0, 0)
        self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnModif.setVisible(self.boolModif)
        self.btnModif.clicked.connect(self.evt_btnModif_clicked)
        self.lblLienWeb.clicked.connect(self.evt_lblLienWeb_clicked)

    def evt_lblLienWeb_clicked(self):
        mainWindow.URLCour = self.lblURL.text()
        win = FormWebBrowser(self)
        win.resize(QSize(600, 500))
        win.show()

    def evt_btnModif_clicked(self):
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath, internalPath FROM videoFileTab WHERE'
                         f' cle={self.paragraphCour.cleVideo}')

        if query.next():
            videoPath = mainWindow.racine + query.value('internalPath') + query.value('videoFullPath')
            formGererNote = FormBlockNote(self, videoPath, self.paragraphCour.cleVideo,
                                          self.marqueCour, False)
            # formGererNote = FormGererNote(self, videoPath, self.paragraphCour.cleVideo,
            #                               self.marqueCour, False)
            # formCreerNote.show()
            formGererNote.populateNoteModif(self.paragraphCour)
            # formGererNote.exec_()
            formGererNote.show()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              N O T E L I E N              ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NoteLien(QGroupBox):
    def __init__(self, parent, timeNote, indentation, titre, picture, hauteur, largeur, texte, cle, videoPath,
                 videoID, icone, note, lien, contenant):
        QLabel.__init__(self, parent)

        self.parent = contenant
        self.timeNote = timeNote
        self.indentation = indentation
        self.titre = titre
        self.picture = picture
        self.note = note
        self.videoPath = videoPath
        self.hauteur = 249
        self.largeur = 423
        self.videoID = videoID
        self.icone = icone
        self.texte = texte
        self.cle = cle
        self.cleLien = lien
        self.setStyleSheet('line-height: 2')

        self.setFixedSize(QSize(423, 100))
        # layout = QHBoxLayout()
        btnLien = QPushButton(self)
        btnLien.setFixedSize(QSize(30, 30))
        # btnLien.setStyleSheet('background-color: transparent; border-width: 1px;')
        iconLien = QIcon('ressources/lienGrd.png')
        btnLien.setIcon(iconLien)
        btnLien.move(4, 10)
        # layout.setContentsMargins(0, 0, 0, 0)
        #  timeNote du lien
        self.timeNoteLien = ''
        query = QSqlQuery()
        bOk = query.exec(f'SELECT timeNote FROM  paragraph WHERE cle={lien}')
        if query.next():
            self.timeNoteLien = strTime(query.value('timeNote'))
            self.timeNoteLienInt = query.value('timeNote')

        texte = self.miseEnForme(self.texte)
        scrollLabel = ScrollLabel(self)
        scrollLabel.setFixedSize(QSize(328, 80))
        scrollLabel.setText("<p>" + str(texte) + "</p>")
        scrollLabel.move(90, 10)
        #
        self.icon = QIcon('ressources/corbeille.png')
        aux = strTime(self.timeNote)
        aux = ''
        self.btnModif = QPushButton(aux, self)
        self.btnModif.setIcon(self.icon)
        # self.btnModif.setStyleSheet('font-size: 7pt; font-family: Arial; margin-top:0; margin-bottom:0;'
        #                             'border-style: solid; border-color: gray; border-width: 0px;'
        #                             'background-color: transparent')
        self.btnModif.setFixedSize(30, 30)
        self.btnModif.move(4, 62)
        self.btnModif.setCursor(QCursor(Qt.PointingHandCursor))

        self.btnModif.clicked.connect(self.evt_btnModif_clicked)
        btnLien.clicked.connect(self.evt_btnLien_clicked)

    def miseEnForme(self, texte):
        #  Initialiser startHTML et end HTML
        texte = texte.replace('$$', chr(10))
        texte = texte.replace(')|', chr(34))
        texte = texte.replace('µµ', chr(9))
        txtDecoupe = texte.split(chr(10))
        textTitre = f'<span style="font-size:9pt; font-weight:600>>{txtDecoupe[0]}<br></span>'
        del txtDecoupe[0]
        txtLien = ''
        for item in txtDecoupe:
            txtLien += item
        lstTxtLien = txtLien.split(':')

        txtLien = f'<span style=" color:#888888;">{lstTxtLien[0]} : <b>{lstTxtLien[1]}</b>'
        texte = textTitre + txtLien + '<br>' + 'TimeNote : ' + '<b>' + self.timeNoteLien
        return texte

    def evt_btnModif_clicked(self):
        rep = QMessageBox.question(self, "Supprimer le lien", "Confirmez-vous la suppression ?")
        if rep == QMessageBox.Yes:
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cle}')
            objNote.populateObjNote(self.videoID)

    def evt_btnLien_clicked(self):
        # fileAttenteVideo.append((self.videoID, self.cleLien))
        query = QSqlQuery()
        bOk = query.exec(f'SELECT cleVideo FROM paragraph WHERE cle={self.cleLien}')
        if query.next():
            fileAttenteVideo.append((query.value('cleVideo'), self.cleLien))
        self.parent.parent.videoID = query.value('cleVideo')
        objNote.populateObjNote(query.value('cleVideo'))
        objNote.parent.videoID = query.value('cleVideo')
        formScreen1.loadVideo(query.value('cleVideo'))
        mainParagraph.btnRetour.setVisible(True)
        self.setLienTimeNote()

    def setLienTimeNote(self):
        # if e.button() == Qt.LeftButton:  # lecture de la vidéo à partir du timeNote de l'image
        formScreen1.mediaPlayer.setPosition(int(self.timeNoteLienInt) * 1000)
        if formScreen1.mediaPlayer.state() == QMediaPlayer.PlayingState:
            formScreen1.mediaPlayer.pause()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            formScreen1.mediaPlayer.setPlaybackRate(self.parent.parent.formScreen.vitesseCour)
            formScreen1.mediaPlayer.play()
            formScreen1.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))


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

    def evt_mediaPlayer_changeDuration(self, duration):
        self.durationCour = duration
        self.lblDuration.setText(strTime(duration // 1000))
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
        self.lblPosition.setText(strTime(position // 1000))

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
        self.btnMarque.setText(strTime(self.mediaPlayer.position() // 1000))
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
# ***************        F O R M T A G I N T E R N E      *************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormTagInterne(QGroupBox):
    def __init__(self, parent, contenant, videoID, lytMain, marqueCour):
        super().__init__()
        self.setStyleSheet('background-color: #333333; margin: 0px')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(100)

        self.parent = parent
        self.contenant = contenant
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False
        self.indexCour = -1
        self.titreComment = ''
        self.listTag = []
        self.listTagSelect = []
        self.marqueCour = marqueCour

        grpTop = QGroupBox()
        grpTop.setStyleSheet('background: transparent')
        grpTop.setFixedSize(600, 50)
        lytMain.addWidget(grpTop)

        #  Saisie du tag
        self.lneTag = QLineEdit(grpTop)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lneTag.setFont(font)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.lneTag.setStyleSheet('margin: 0px; color: white; background: #666666; border-radius: 6px')
        self.lneTag.setFixedSize(400, 35)
        self.lneTag.move(0, 1)
        # Bouton Plus
        self.btnAdmiPlus = QPushButton(grpTop)
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus.setFixedSize(39, 39)
        self.btnAdmiPlus.setIconSize(QSize(33, 33))
        self.btnAdmiPlus.move(410, 0)
        self.btnAdmiPlus.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus.clicked.connect(self.sauverTag)
        #  Bouton Modif
        self.btnAdmiModif = QPushButton(grpTop)
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif.setFixedSize(39, 39)
        self.btnAdmiModif.setIconSize(QSize(33, 33))
        self.btnAdmiModif.move(450, 0)
        self.btnAdmiModif.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif.clicked.connect(self.modifTag)
        #  Bouton Suppr
        self.btnAdmiSuppr = QPushButton(grpTop)
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr.setFixedSize(39, 39)
        self.btnAdmiSuppr.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr.move(490, 0)
        self.btnAdmiSuppr.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr.clicked.connect(self.effaceTag)

        self.grpBoxAffichTag = QGroupBox(self)
        self.grpBoxAffichTag.setStyleSheet('border: 0px; background: #333333')
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        self.grpBoxAffichTag.setFixedSize(590, 120)  # 590

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(self.grpBoxAffichTag)
        scroll.setWidgetResizable(True)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        scroll.setStyleSheet(styleQScrollBar)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        self.populateGrpBoxAffichTag()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            source.majEtatSelect()
            if source.boolSelect:
                self.listTagSelect.append(source.text())
            else:
                del self.listTagSelect[self.listTagSelect.index(source.text())]
        return super().eventFilter(source, event)

    def effaceTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = 'Pas de tag sélectionné.'
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return
        #  la cle correspodant au tag concerné
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.listTagSelect[0]}"')
        if query.next():
            cle = query.value('cle')
        self.dialog = DialogCustom()
        aux = 'Vous êtes en train de supprimer les tags sélectionnés. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            query = QSqlQuery()
            bOK = query.exec(f'DELETE FROM tagTab WHERE cle = {cle}')
        self.populateGrpBoxAffichTag()

    def modifTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = 'Pas de tag sélectionné.'
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return
        if len(self.listTagSelect) > 1:
            self.dialog = DialogCustom()
            aux = "L'opération de modification ne s'applique\nqu'à un tag à la fois."
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Fermer', False)
            self.dialog.setBouton2('Fermer', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.motCour = self.listTagSelect[0]
        self.lneTag.setText(self.motCour)
        # #  la cle correspodant au tag concerné
        # query = QSqlQuery()
        # query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
        # if query.next():
        #     cle = query.value('cle')
        self.indexCour = self.listTag.index(self.motCour)
        self.boolModif = True

    def sauverTag(self):
        #  Vérifier l'existence du tag en doublon
        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))
        mot = self.lneTag.text()

        if mot in self.listTag:
            QMessageBox.information(self, 'Enregistrement annulé', 'Le tag existe déja pour cette vidéo.')
        else:
            if self.boolModif:
                #  la cle correspodant au tag concerné
                query = QSqlQuery()
                query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
                if query.next():
                    cle = query.value('cle')
                query = QSqlQuery()
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                tplData = (cle, self.marqueCour, self.lneTag.text(), self.videoID)
                bOk = query.exec(f'UPDATE tagTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
                self.populateGrpBoxAffichTag()
            else:
                #  Recherche de l'index suivant
                cleMax = 1
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) AS cleMax FROM tagTab')
                try:
                    if query.next():
                        cleMax = query.value('cleMax') + 1
                except:
                    pass
                tplData = (cleMax, self.marqueCour, mot, self.videoID)
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                query1 = QSqlQuery()
                query1.exec(f'INSERT INTO tagTab {tplChamps} VALUES {tplData}')
                self.listTag.append(mot)
        self.lneTag.setText('')
        self.boolModif = False
        self.populateGrpBoxAffichTag()

    def populateGrpBoxAffichTag(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            # Remplacer les notes (Null) par 0
            query = QSqlQuery()
            query.exec('UPDATE videoFileTab SET note = 0 WHERE note IS NULL')
        query = QSqlQuery()
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
        query = QSqlQuery()
        ok = query.exec(f'SELECT * FROM tagTab where timeCode={self.marqueCour} AND cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))

        if len(self.listTag) == 0:
            return
        ligne = 0
        # *********************************************************************************************
        # *********************************************************************************************
        i = 0
        continuerLigne = True
        largLigneTag = 0
        largeur = 550
        offSet = 28
        lenList = len(self.listTag)
        grpBox = QGroupBox()
        grpBox.setFixedHeight(1000)
        grpBox.setStyleSheet('border: 0px; background: #333333')
        self.lytAffichTag.addWidget(grpBox)
        self.lytAffichTag.setSpacing(0)
        nbLigne = 0
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(grpBox, self.listTag[i], '#666666')
                lblTag.installEventFilter(self)
                lblTag.setPosition(largLigneTag, nbLigne*30)
                largLigneTag += lblTag.width + offSet
                if i + 1 == lenList:
                    self.lytAffichTag.addWidget(grpBox)
                    continuerLigne = False
                    continuerColonne = False
                    lblTag.setPosition(largLigneTag-lblTag.width-offSet, nbLigne*30)
                else:
                    if largLigneTag > largeur-lblTag.width-offSet-20:
                        largLigneTag = 0
                        lblTag.close()
                        nbLigne += 1
                        i -= 1
                        continuerColonne = False
                i += 1
        # spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lytAffichTag.addItem(spacerItem)
        self.lneTag.setText('')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        F O R M B L O C K N O T E      ***************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class FormBlockNote(MainWindowCustom):
    def __init__(self, parent, videoPath, videoID, marqueCour, boolCreer):
        super().__init__()
        self.setGeometry(100, 100, 1210, 768)
        self.setTitle('Ceci est un exemple de titre')
        self.setStyleSheet('background-color: #262626')
        self.videoPath = 'C:/VideoFinder/Protype11/video/notion-to-do-list.mp4'
        #***** ARGUMENTS  ***************
        self.parent = parent
        videoPath = videoPath
        self.videoID = videoID
        self.marqueCour = marqueCour
        self.boolCreer = boolCreer
        #********************************
        self.cleNoteCour = -1
        self.cleSnapShotCour = -1
        self.cleTitreCour = -1
        self.listTpl = []

        self.setUpUI()

        if not self.boolCreer:
            self.populateNoteModif()

    def setUpUI(self):
        # **************************************************************
        # lne saisie titre ou paragraphe
        # **************************************************************
        self.lneTitreParagraph = QLineEdit(self)
        self.lneTitreParagraph.setFixedSize(513, 35)
        self.lneTitreParagraph.setPlaceholderText('Saisir le titre de la vidéo ou du paragraphe')
        self.lneTitreParagraph.setStyleSheet('background-color: #666666; color: white; border: 0px;'
                                             'border-radius: 6px')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lneTitreParagraph.setFont(font)
        self.lneTitreParagraph.move(20, 60)
        self.lneTitreParagraph.textChanged.connect(self.evt_lneTitreParagraph_textChanged)
        # **************************************************************
        #  Bouton ValideTitre
        # **************************************************************
        self.btnValideTitre = BoutonOffOn(self)
        aux = self.lneTitreParagraph.text()
        if aux == '':
            self.btnValideTitre.initBool(False)
        else:
            self.btnValideTitre.initBool(True)
        self.btnValideTitre.move(563, 60)
        # **************************************************************
        #  Liste des fonts disponibles
        # **************************************************************
        font_db = QFontDatabase()
        font_families = font_db.families()
        self.cmbFontWidget = QComboBox(self)
        # self.cmbFontWidget.setStyleSheet('QComboBox {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeeeee, stop:1 #aaaaaa);'
        #                                  ' color: black; border: 0px;}')
        f = open('styles/QComboBoxDegrade.txt', 'r')
        style = f.read()
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(True)
        self.cmbFontWidget.setStyleSheet(style)
        self.cmbFontWidget.setFont(font)
        self.cmbFontWidget.setFixedSize(180, 30)
        self.cmbFontWidget.setWindowTitle('Polices disponibles')
        # Ajouter chaque police à QListWidget
        i = 0
        for font_family in font_families:
            # list_item = QListWidgetItem(font_family)
            self.cmbFontWidget.addItem(font_family, 1)
            i += 1
        self.cmbFontWidget.setCurrentIndex(3)
        self.cmbFontWidget.move(20, 140)
        self.cmbFontWidget.currentIndexChanged.connect(self.changeFontNote)
        # **************************************************************
        #  Liste des tailles de font
        # **************************************************************
        self.spnTaillePolice = QSpinBox(self)
        self.spnTaillePolice.setRange(8, 72)
        self.spnTaillePolice.setFixedSize(60, 30)
        self.spnTaillePolice.setFont(font)
        self.spnTaillePolice.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                           'stop:0 #aaaaaa, stop:1 #eeeeee); color: black; border: 0px;'
                                           'border-radius: 4px; border: 1px solid #262626')
        self.spnTaillePolice.move(207, 140)
        self.spnTaillePolice.valueChanged.connect(self.evt_spnTaillePolice_changed)
        # **************************************************************
        #  Bouton Gras
        # **************************************************************
        self.btnGras = QPushButton(self)
        self.btnGras.setFixedSize(30, 30)
        self.btnGras.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                           'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                           'border-radius: 4px; border: 1px solid #262626')
        font = QFont()
        font.setFamily('Arial Black')
        font.setPointSize(10)
        font.setBold(True)
        self.btnGras.setFont(font)
        self.btnGras.setText('T')
        # self.btnGras.move(280, 140)
        # **************************************************************
        #  Bouton Souligné
        # **************************************************************
        # self.btnSouligne = QPushButton(self)
        # self.btnSouligne.setFixedSize(30, 30)
        # self.btnSouligne.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
        #                            'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
        #                            'border-radius: 4px; border: 1px solid #262626')
        # font = QFont()
        # font.setFamily('Arial')
        # font.setPointSize(10)
        # font.setUnderline(True)
        # font.setBold(True)
        # self.btnSouligne.setFont(font)
        # self.btnSouligne.setText('T')
        # self.btnSouligne.move(317, 140)
        # **************************************************************
        #  Bouton Italic
        # **************************************************************
        self.btnItalic = QPushButton(self)
        self.btnItalic.setFixedSize(30, 30)
        self.btnItalic.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                       'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                       'border-radius: 4px; border: 1px solid #262626')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setUnderline(False)
        font.setItalic(True)
        self.btnItalic.setFont(font)
        self.btnItalic.setText('T')
        # self.btnItalic.move(317, 140)
        # **************************************************************
        #  Bouton undo
        # **************************************************************
        self.btnUndo = QPushButton(self)
        self.btnUndo.setFixedSize(30, 30)
        self.btnUndo.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                     'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                     'border-radius: 4px; border: 1px solid #262626')
        self.btnUndo.setIcon(QIcon('ressources/undo.png'))
        self.btnUndo.move(405, 140)
        # **************************************************************
        #  Bouton redo
        # **************************************************************
        self.btnRedo = QPushButton(self)
        self.btnRedo.setFixedSize(30, 30)
        self.btnRedo.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626')
        self.btnRedo.setIcon(QIcon('ressources/redo.png'))
        self.btnRedo.move(440, 140)
        # **************************************************************
        #  Bouton link
        # **************************************************************
        self.btnLink = QPushButton(self)
        self.btnLink.setFixedSize(30, 30)
        self.btnLink.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626')
        self.btnLink.setIcon(QIcon('ressources/link.png'))
        self.btnLink.move(490, 140)
        self.btnLink.clicked.connect(self.creerLink)
        # **************************************************************
        #  Bouton suppr link
        # **************************************************************
        self.btnLinkSuppr = QPushButton(self)
        self.btnLinkSuppr.setFixedSize(30, 30)
        self.btnLinkSuppr.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626')
        self.btnLinkSuppr.setIcon(QIcon('ressources/linkSuppr.png'))
        self.btnLinkSuppr.move(525, 140)
        self.btnLinkSuppr.clicked.connect(self.supprLink)
        # **************************************************************
        #  textEditNote
        # **************************************************************
        self.grpNote = QGroupBox(self)
        self.grpNote.setFixedSize(650, 300)
        self.grpNote.setStyleSheet('background-color: #222222; border-radius: 6px; color: white')
        self.grpNote.move(20, 178)
        lytGrpNote = QVBoxLayout()
        self.grpNote.setLayout(lytGrpNote)

        self.textEditNote = QTextEdit(self.grpNote)
        # self.textEditNote = TextEditLink(self.grpNote)
        self.textEditNote.setFixedSize(630, 280)
        f = open('styles/QTextEdit.txt', 'r')
        style = f.read()
        lytGrpNote.addWidget(self.textEditNote)
        self.textEditNote.viewport().installEventFilter(self)

        # self.textEditNote.setStyleSheet('background-color: #333333; border-radius: 6px; color: white')
        self.textEditNote.setPlaceholderText('Saisir une note...')
        self.textEditNote.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.textEditNote.setStyleSheet(style)
        self.textEditNote.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.textEditNote.setFont(font)
        self.textEditNote.textChanged.connect(self.evt_textEditNote_textChanged)
        self.btnUndo.clicked.connect(self.textEditNote.undo)
        self.btnRedo.clicked.connect(self.textEditNote.redo)

        #  grpSupprLink
        self.grpSupprLink = QGroupBox(self.textEditNote)
        self.grpSupprLink.setFixedSize(200, 250)
        self.grpSupprLink.setStyleSheet('background-color: #333333; border: 1px solid white')
        self.grpSupprLink.setVisible(False)
        self.grpSupprLink.move(300, 0)
        lblSupptLink = QLabel(self.grpSupprLink)
        lblSupptLink.setText('Supprimer un lien')
        lblSupptLink.setStyleSheet('border: 0px')
        lblSupptLink.move(40, 5)
        #
        self.listSupprLink = QListWidget(self.grpSupprLink)
        self.listSupprLink.setFixedSize(180, 170)
        self.listSupprLink.move(10, 30)
        #
        boutonEffaceLink = QPushButton(self.grpSupprLink)
        boutonEffaceLink.setText('Supprimer')
        boutonEffaceLink.move(20, 220)
        boutonEffaceLink.clicked.connect(self.evt_boutonEffaceLink_clicked)
        boutonFermeLink = QPushButton(self.grpSupprLink)
        boutonFermeLink.setText('Fermer')
        boutonFermeLink.move(140, 220)
        boutonFermeLink.clicked.connect(self.evt_boutonFermeLink_clicked)

        # **************************************************************
        #  Bouton ValideNote
        # **************************************************************
        self.btnValideNote = BoutonOffOn(self)
        aux = self.textEditNote.toPlainText()
        if aux == '':
            self.btnValideNote.initBool(False)
        else:
            self.btnValideNote.initBool(True)
        self.btnValideNote.move(563, 140)
        # **************************************************************
        # Gestion des tags internes
        # **************************************************************
        self.cadreWidgetTag = QGroupBox(self)
        self.cadreWidgetTag.setFixedSize(650, 220)
        self.cadreWidgetTag.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreWidgetTag.move(20, 520)
        #  Installation de GrpBoxMetaData
        lytTag = QVBoxLayout()
        self.cadreWidgetTag.setLayout(lytTag)
        grpBoxTag = FormTagInterne(self, self, 11, lytTag, self.marqueCour)
        lytTag.addWidget(grpBoxTag)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lytTag.addItem(spacer)
        # **************************************************************
        # SnapShot + legende
        # **************************************************************
        self.cadreSnapShot = QGroupBox(self)
        self.cadreSnapShot.setFixedSize(500, 270)
        self.cadreSnapShot.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreSnapShot.move(690, 60)
        #  lblSnapShot
        self.lblSnapShot = QLabel(self.cadreSnapShot)
        self.lblSnapShot.setStyleSheet('background-color: #222222;')
        self.lblSnapShot.setFixedSize(340, 180)
        self.lblSnapShot.move(15, 10)
        self.populateSnapShot()
        #  lblLegende
        self.lneLegende = QLineEdit(self.cadreSnapShot)
        self.lneLegende.setStyleSheet('background-color: #333333; color: white')
        self.lneLegende.setPlaceholderText("Saisir la légende de l'image...")
        self.lneLegende.setFixedSize(450, 60)
        self.lneLegende.move(15, 200)
        #  checkBoxIcone
        self.chkIcone = QCheckBox(self.cadreSnapShot)
        self.chkIcone.setStyleSheet('color: white')
        self.chkIcone.setText('Vignette')
        self.chkIcone.move(360, 70)
        #  Bouton valide
        self.btnValideSnapShot = BoutonOffOn(self.cadreSnapShot)
        if aux == '':
            self.btnValideSnapShot.initBool(False)
        else:
            self.btnValideSnapShot.initBool(True)
        self.btnValideSnapShot.move(360, 10)
        # **************************************************************
        #  cadre Info Générale
        # **************************************************************
        videoCour = VideoFileRecord(self.videoID)
        self.cadreInfoGene = QGroupBox(self)
        self.cadreInfoGene.setFixedSize(500, 350)
        self.cadreInfoGene.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreInfoGene.move(690, 350)
        #  Titre info générales
        self.lblInfoGene = QLabel(self.cadreInfoGene)
        self.lblInfoGene.setStyleSheet('background-color: transparent; color: #cccccc')
        self.lblInfoGene.setText('Informations générales')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.lblInfoGene.setFont(font)
        self.lblInfoGene.move(20, 10)
        #  Titre vidéo
        lblLibelTitre = QLabel(self.cadreInfoGene)
        lblLibelTitre.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelTitre.setText('Titre :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelTitre.setFont(font)
        lblLibelTitre.move(30, 45)
        #
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblTitre.setText(videoCour.titreVideo)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(130, 45)
        #  Titre favori
        lblLibelFavori = QLabel(self.cadreInfoGene)
        lblLibelFavori.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelFavori.setText('Favori :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelFavori.setFont(font)
        lblLibelFavori.move(30, 80)
        #
        cadreFavori = QGroupBox(self.cadreInfoGene)
        cadreFavori.setFixedSize(40, 40)
        lytFavori = QVBoxLayout()
        cadreFavori.setLayout(lytFavori)
        cadreFavori.move(125, 65)
        self.lblFavoriVideo = WidgetFavori(boolFavori=videoCour.Favori)
        lytFavori.addWidget(self.lblFavoriVideo)
        #  Titre durée
        lblLibelDuree = QLabel(self.cadreInfoGene)
        lblLibelDuree.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelDuree.setText('Durée :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelDuree.setFont(font)
        lblLibelDuree.move(30, 115)
        #
        self.lblDureeVideo = QLabel(self.cadreInfoGene)
        query = QSqlQuery()
        ok = query.exec(f'SELECT path FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        if query.next():
            racineCour = query.value('path')
        #  extraction de la vignette
        video = racineCour + videoCour.internalPath + videoCour.videoName
        self.lblDureeVideo.setText(str(self.videoDuration(video)))
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblDureeVideo.setFont(font2)
        self.lblDureeVideo.setStyleSheet('color: #bbbbbb')
        self.lblDureeVideo.move(130, 115)
        #  Titre Note
        lblLibelNote = QLabel(self.cadreInfoGene)
        lblLibelNote.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelNote.setText('Note :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelNote.setFont(font)
        lblLibelNote.move(30, 150)
        #
        self.grpRating = QGroupBox(self.cadreInfoGene)
        self.lblNoteVideo = StarRating(videoCour.note)
        self.lblNoteVideo.setBackgound('transparent')
        self.grpRating.setFixedSize(250, 43)
        self.grpRating.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpRating.move(105, 125)
        lytRating = QVBoxLayout()
        lytRating.setSpacing(0)
        lytRating.addWidget(self.lblNoteVideo)
        self.grpRating.setLayout(lytRating)
        #  Titre Bibliothèque
        lblLibelBiblio = QLabel(self.cadreInfoGene)
        lblLibelBiblio.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelBiblio.setText('Bibliothèque :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelBiblio.setFont(font)
        lblLibelBiblio.move(30, 190)
        #
        lblBiblio = QLabel(self.cadreInfoGene)
        lblBiblio.setStyleSheet('background-color: transparent; color: #bbbbbb')
        query = QSqlQuery()
        query.exec(f'SELECT nom FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        aux = ''
        if query.next():
            aux = query.value('nom')
        lblBiblio.setText(aux)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblBiblio.setFont(font)
        lblBiblio.move(135, 190)
        #  Titre Timecodee
        lblLibelTimeCode = QLabel(self.cadreInfoGene)
        lblLibelTimeCode.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelTimeCode.setText('Timecode :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelTimeCode.setFont(font)
        lblLibelTimeCode.move(30, 230)
        #
        lblTimeCode = QLabel(self.cadreInfoGene)
        lblTimeCode.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblTimeCode.setText(self.strTime(self.marqueCour))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTimeCode.setFont(font)
        lblTimeCode.move(135, 230)
        #  Titre Classeur
        lblLibelClasseur = QLabel(self.cadreInfoGene)
        lblLibelClasseur.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelClasseur.setText('Classeur :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelClasseur.setFont(font)
        lblLibelClasseur.move(30, 270)
        #
        lblClasseur = QLabel(self.cadreInfoGene)
        lblClasseur.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblClasseur.setText(videoCour.nomClasseur)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblClasseur.setFont(font)
        lblClasseur.move(135, 270)
        #  Titre Label
        self.lblLabelVideo = QLabel(self.cadreInfoGene)
        # self.lblLabelVideo.setFixedSize(310, 30)
        lblLibelLabel = QLabel(self.cadreInfoGene)
        lblLibelLabel.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelLabel.setText('Label :')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelLabel.setFont(font)
        lblLibelLabel.move(30, 310)
        #
        self.lblLabelVideo = QLabel(self.cadreInfoGene)
        self.lblLabelVideo.setStyleSheet('color: #888888')
        try:
            color = videoCour.colorStatut
            nomLabel = videoCour.nomStatut
        except:
            color = '#ffffff'
            nomLabel = 'Aucun label'
        self.lblLabelVideo.setText('         ' + nomLabel)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblLabelVideo.setFont(font2)
        self.lblPastilleInfo = QLabel(self.lblLabelVideo)
        self.lblPastilleInfo.setFixedSize(19, 19)
        self.lblPastilleInfo.setStyleSheet('background: transparent')
        self.lblPastilleInfo.move(3, 4)
        if videoCour.statut == -1:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, ''))
        else:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, color))
        self.lblLabelVideo.move(135, 310)

        # Bouton sauver
        self.btnSauver = QPushButton(self)
        self.btnSauver.setFixedSize(100, 35)
        self.btnSauver.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSauver.setText('Sauver')
        self.btnSauver.move(960, 718)
        self.btnSauver.clicked.connect(self.sauverBlockNote)

    def evt_lneTitreParagraph_textChanged(self):
        if self.lneTitreParagraph.text() == '':
            self.btnValideTitre.initBool(False)
        else:
            self.btnValideTitre.initBool(True)

    def evt_textEditNote_textChanged(self):
        if self.textEditNote.toPlainText() == '':
            self.btnValideNote.initBool(False)
        else:
            self.btnValideNote.initBool(True)

    def changeFontNote(self):
        cursor = self.textEditNote.textCursor()
        text_selected = cursor.selectedText()
        if text_selected == '':
            return
        aux = self.cmbFontWidget.currentText()
        self.textEditNote.setCurrentFont(QFont(aux))

    def evt_spnTaillePolice_changed(self):
        cursor = self.textEditNote.textCursor()
        text_selected = cursor.selectedText()
        if text_selected == '':
            return
        font = self.textEditNote.currentFont()
        font.setPointSize(self.spnTaillePolice.value())
        self.textEditNote.setCurrentFont(font)

    def supprLink(self):
        self.grpSupprLink.setVisible(True)
        self.listSupprLink.clear()
        for tpl in self.listTpl:
            lien, URL = tpl
            self.listSupprLink.addItem(lien)

    def evt_boutonFermeLink_clicked(self):
        self.grpSupprLink.setVisible(False)

    def eventFilter(self, source, event):
        try:
            if source is self.textEditNote.viewport() and event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    cursor = self.textEditNote.cursorForPosition(event.pos())
                    cursor.select(QTextCursor.WordUnderCursor)
                    selected_text = cursor.selectedText()
                    format = cursor.charFormat()
                    if format.fontWeight() == QFont.Bold and format.fontUnderline():
                        for tpl in self.listTpl:
                            lien, URL = tpl
                            if selected_text in lien:
                                QDesktopServices.openUrl(QUrl(URL))
                    else:
                        pass
        except:
            pass
        return super().eventFilter(source, event)

    def evt_boutonEffaceLink_clicked(self):
        itm = self.listSupprLink.currentItem()
        lienAux = itm.text()
        self.listSupprLink.takeItem(self.listSupprLink.row(itm))
        i = 0
        lien = ''
        URL = ''
        for tpl in self.listTpl:
            lien, URL = tpl
            if lien == lienAux:
                del self.listTpl[i]
            i += 1
        # MaJ de textEditNote
        cursor = self.textEditNote.textCursor()
        format = QTextCharFormat()
        format.setFontWeight(not QFont.Bold)
        format.setForeground(QBrush(QColor("#ffffff")))
        format.setFontUnderline(False)
        while True:
            cursor = self.textEditNote.document().find(lienAux, cursor)
            format1 = cursor.charFormat()
            if format1.fontWeight() == QFont.Bold and format1.fontUnderline() and not cursor.isNull():
                cursor.mergeCharFormat(format)
            else:
                break
        #  MaJ de la base de données
        query = QSqlQuery()
        query.exec(f'DELETE FROM linkTab WHERE timeCode={self.marqueCour} AND cleVideo={self.videoID} AND mot={lien}')

    def populateNoteModif(self):
        self.btnValideTitre.initBool(False)
        self.btnValideNote.initBool(False)
        self.btnValideSnapShot.initBool(False)
        query = QSqlQuery()
        query.exec(f'SELECT * FROM Paragraph WHERE cleVideo={self.videoID}  AND timeNote={self.marqueCour}')
        while query.next():
            if query.value('titre'):
                self.lneTitreParagraph.setText(query.value('texte'))
                self.btnValideTitre.initBool(True)
                self.cleTitreCour = query.value('cle')
            if query.value('picture'):
                self.lneLegende.setText(query.value('texte'))
                self.btnValideSnapShot.initBool(True)
                if query.value('icone'):
                    self.chkIcone.setChecked(True)
                self.cleSnapShotCour = query.value('cle')
            if query.value('Note'):
                aux = query.value('texte')
                cleAux = query.value('cle')
                #  Récupération des éventuels liens URL
                query1 = QSqlQuery()
                ok = query1.exec(f'SELECT mot, URL FROM linkTab WHERE timecode={self.marqueCour} AND cleVideo={self.videoID}')
                self.listTpl = []
                while query1.next():
                    self.listTpl.append((query1.value('mot'), query1.value('URL')))

                # if len(self.listTpl) > 0:
                #     for tpl in self.listTpl:
                #         lien, URL = tpl
                #         auxHtml = f'<a href={URL} target="_blank">{lien}</a>'
                #         aux = aux.replace(lien, auxHtml)
                #         aux = aux.replace('$$', chr(10))
                # else:
                #     aux = aux.replace('$$', chr(10))

                #  Récupération du texte brut
                aux = aux.replace("²", "'")
                aux = aux.replace('<br>', '')
                aux = aux.replace("&#09", "\t")
                self.textEditNote.setText(aux)
                self.btnValideNote.initBool(True)
                self.cleNoteCour = cleAux
            # if query.value('Note'):
            #     aux = query.value('texte')
            #     cleAux = query.value('cle')
            #     query1 = QSqlQuery()
            #     ok = query1.exec(f'SELECT mot, URL FROM linkTab WHERE timecode={self.marqueCour} AND cleVideo={self.videoID}')
            #     self.listTpl = []
            #     while query1.next():
            #         self.listTpl.append((query1.value('mot'), query1.value('URL')))
            #     if len(self.listTpl) > 0:
            #         for tpl in self.listTpl:
            #             lien, URL = tpl
            #             auxHtml = f'<a href={URL} target="_blank">{lien}</a>'
            #             aux = aux.replace(lien, auxHtml)
            #             aux = aux.replace('$$', chr(10))
            #     else:
            #         aux = aux.replace('$$', chr(10))
            #
            #     self.textEditNote.setText(aux)
            #     self.btnValideNote.initBool(True)
            #     self.cleNoteCour = cleAux

    def sauverBlockNote(self):
        msg = ''
        if not self.btnValideSnapShot.boolON:
            if msg == '':
                msg += "l'image et sa légende"
            else:
                msg += ", l'image et sa légende"
        if not self.btnValideTitre.boolON:
            if msg == '':
                msg += "le titre"
            else:
                msg += ", le titre"
        if not self.btnValideNote.boolON:
            if msg == '':
                msg += "la note"
            else:
                msg += ", la note"
        msg1 = ''
        if msg != '':
            msg1 = "Les éléments suivants ne seront pas sauvegardés: " + msg + " . \n" \
                  "S'ils ont déja été créés, ils seront effacés."
        else:
            msg1 = "Confirmez-vous l'enregeristrement de la note ?"

        self.dialog = DialogCustom(self, 0, 0)
        self.dialog.lblWindowTitle.setText("Sauvegarde de la note")
        self.dialog.setMessage(msg1)
        self.dialog.setPosition(0, 0)
        self.dialog.setBouton1('Accepter', True)
        self.dialog.setBouton2('Annuler', True)
        self.dialog.setSaisie('', False)
        if self.dialog.exec_() != DialogCustom.Accepted:
            return
        # Sauvegarde du titre
        if self.cleTitreCour == -1:
            if self.btnValideTitre.boolON:
            # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'titre', 'texte', 'cleVideo')
                tplData = (maxCle, self.marqueCour, True, self.lneTitreParagraph.text(), self.videoID)
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideTitre.boolON:
                query = QSqlQuery()
                tplChamps = ('timeNote', 'titre', 'texte', 'cleVideo')
                tplData = (self.marqueCour, True, self.lneTitreParagraph.text(), self.videoID)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleTitreCour}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleTitreCour}')
        # Sauvegarde de la note
        if self.cleNoteCour == -1:
            if self.btnValideNote.boolON:
                # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                aux = self.textEditNote.toHtml()
                aux = aux.replace("'", "²")
                aux = aux.replace("\n", "<br>")
                aux = aux.replace("\t", "&#09")

                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'note', 'texte', 'cleVideo')
                tplData = (maxCle, self.marqueCour, True, aux, self.videoID)
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                #  sauvegarde des liens/URL
                for tpl in self.listTpl:
                    lien, URL = tpl
                    # recherche de la clé suivante
                    query = QSqlQuery()
                    query.exec(f'SELECT MAX(cle) FROM linkTab')
                    maxCle1 = 0
                    try:
                        if query.next():
                            maxCle1 = query.value(0) + 1
                    except:
                        maxCle1 = 1
                    query = QSqlQuery()
                    tplChamps = ('cle', 'timeCode', 'mot', 'URL', 'cleVideo')
                    tplData = (maxCle1, self.marqueCour, lien, URL, self.videoID)
                    query.exec(f'INSERT INTO linkTab {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideNote.boolON:
                #  Suppression des entrées dans linkTab correspondant àla note courante
                query = QSqlQuery()
                query.exec(f'DELETE FROM linkTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
                #  enregistrement du texte de la note
                query = QSqlQuery()
                aux = self.textEditNote.toHtml()
                aux = aux.replace("'", "²")
                aux = aux.replace("\n", "<br>")
                aux = aux.replace("\t", "&#09")
                tplChamps = ('timeNote', 'Note', 'texte', 'cleVideo', 'titre')
                tplData = (self.marqueCour, True, aux, self.videoID, False)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleNoteCour}')
                # sauvegarde des liens/URL
                for tpl in self.listTpl:
                    lien, URL = tpl
                    #  recherche de la clé suivante
                    query = QSqlQuery()
                    query.exec(f'SELECT max(cle) FROM linkTab')
                    maxCle1 = 0
                    try:
                        if query.next():
                            maxCle1 = query.value(0) + 1
                    except:
                        maxCle1 = 1
                    query = QSqlQuery()
                    tplChamps = ('cle', 'timeCode', 'mot', 'URL', 'cleVideo')
                    tplData = (maxCle1, self.marqueCour, lien, URL, self.videoID)
                    query.exec(f'INSERT INTO linkTab {tplChamps} VALUES {tplData}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleNoteCour}')
                #  Suppression des entrées dans linkTab correspondant àla note courante
                query = QSqlQuery()
                query.exec(f'DELETE FROM linkTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
        # Sauvegarde de l'image
        if self.chkIcone.isChecked():
            #  Supprimer l'ancienne image icone
            query = QSqlQuery()
            query.exec(f'SELECT * FROM paragraph where cleVideo={self.videoID} AND icone={True}')
            if query.next():
                cleAux = query.value('cle')
                query = QSqlQuery()
                tplChamps = ('icone')
                tplData = (False)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={cleAux}')
        if self.cleSnapShotCour == -1:
            if self.btnValideSnapShot.boolON:
                # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'picture', 'texte', 'cleVideo', 'icone')
                tplData = (maxCle, self.marqueCour, True, self.lneLegende.text(), self.videoID,
                           self.chkIcone.isChecked())
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideSnapShot.boolON:
                query = QSqlQuery()
                tplChamps = ('timeNote', 'picture', 'texte', 'cleVideo', 'icone')
                tplData = (self.marqueCour, True, self.lneLegende.text(), self.videoID, self.chkIcone.isChecked())
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleSnapShotCour}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleSnapShotCour}')

        # en cas de suppression totale supprimer les tags internes
        query = QSqlQuery()
        query.exec(f'DELETE FROM tagTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
        #
        try:
            mainXX = mainWindow.tabObjetScreen.docParagraph.widget()
            mainXX.objNote.populateParagraph(self.videoID)
        except:
            pass

        self.close()

    def creerLink(self):
        cursor = self.textEditNote.textCursor()
        lien = cursor.selectedText()

        if len(lien) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            self.dialog.lblWindowTitle.setText("Création d'un lien Web")
            aux = "Pas d'expression sélectionnée."
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1('Accepter', False)
            self.dialog.setBouton2('Annuler', True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return
        #  Formatage en gras souligné
        format = QTextCharFormat()
        format.setFontWeight(QFont.Bold)
        format.setForeground(QBrush(QColor("#ef6634")))
        format.setFontUnderline(True)
        cursor.mergeCharFormat(format)
        self.textEditNote.mergeCurrentCharFormat(format)

        #  Saisie de l'URL
        self.dialog = DialogCustom(self, 0, 0)
        self.dialog.lblWindowTitle.setText("Création d'un lien Web")
        aux = "Saisir une URL..."
        self.dialog.setMessage(aux)
        self.dialog.setPosition(0, 0)
        self.dialog.setBouton1('Accepter', True)
        self.dialog.setBouton2('Annuler', True)
        self.dialog.setSaisie('Saisir une URL...', True)
        address = ''
        if self.dialog.exec_() == DialogCustom.Accepted:
            address = self.dialog.lneSaisie.text()
            self.dialog.close()
        else:
            self.dialog.close()
            return
        self.listTpl.append((lien, address))
        # format = QTextCharFormat()
        # format.setFontWeight(QFont.Bold)
        # format.setFontUnderline(True)
        # cursor.mergeCharFormat(format)
        # self.textEditNote.mergeCurrentCharFormat(format)

        # cursor = self.textEditNote.textCursor()
        # lien = cursor.selectedText()
        #
        # if len(lien) == 0:
        #     self.dialog = DialogCustom(self, 0, 0)
        #     self.dialog.lblWindowTitle.setText("Création d'un lien Web")
        #     aux = "Pas d'expression sélectionnée."
        #     self.dialog.setMessage(aux)
        #     self.dialog.setPosition(0, 0)
        #     self.dialog.setBouton1('Accepter', False)
        #     self.dialog.setBouton2('Annuler', True)
        #     self.dialog.setSaisie('', False)
        #     if self.dialog.exec_() == DialogCustom.Accepted:
        #         return
        #     return
        # #  Saisie de l'URL
        # self.dialog = DialogCustom(self, 0, 0)
        # self.dialog.lblWindowTitle.setText("Création d'un lien Web")
        # aux = "Saisir une URL..."
        # self.dialog.setMessage(aux)
        # self.dialog.setPosition(0, 0)
        # self.dialog.setBouton1('Accepter', True)
        # self.dialog.setBouton2('Annuler', True)
        # self.dialog.setSaisie('Saisir une URL...', True)
        # address = ''
        # if self.dialog.exec_() == DialogCustom.Accepted:
        #     address = self.dialog.lneSaisie.text()
        #     self.dialog.close()
        # else:
        #     self.dialog.close()
        #     return
        # self.listTpl.append((lien, address))
        # aux = self.textEditNote.toPlainText()
        # for tpl in self.listTpl:
        #     lien, address = tpl
        #     auxHtml = f'<a href="{address}" target="_blank">{lien}</a> '
        #     aux = aux.replace(lien, auxHtml)
        #     aux = aux.replace(chr(10), '<br>')
        # self.textEditNote.setText(aux)

    def drawPastille(self, radius, color):
        if color == '':
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor('#ffffff'))
            painter.setPen(pen)
            brush = QBrush(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            pen = QPen(QColor('#ff0000'), 2, Qt.SolidLine)
            painter.setPen(pen)
            brush = QBrush(QColor('#ff0000'))
            painter.setBrush(brush)
            painter.drawLine(1, radius + 2, radius * 2 + 4, radius + 2)
            del painter
        else:
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor(color))
            painter.setPen(pen)
            brush = QBrush(QColor(color))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2*radius, 2*radius)
            del painter
        return pixmap

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

    def populateSnapShot(self):
        videoCour = VideoFileRecord(self.videoID)
        query = QSqlQuery()
        ok = query.exec(f'SELECT path FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        if query.next():
            racineCour = query.value('path')
        #  extraction de la vignette
        video = racineCour + videoCour.internalPath + videoCour.videoName
        vidcap = cv2.VideoCapture(video)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, self.marqueCour * 1000)
        success, image = vidcap.read()
        if success:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(image)
        self.lblSnapShot.setPixmap(pixmap01.scaled(330, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def textEditNote_undo(self):
        print('ok')
        self.textEditNote.undo()

    def textEditNote_redo(self):
        self.textEditNote.redo()
# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        F O R M C R E E R N O T E      ***************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class FormGererNote(QDialog):
    def __init__(self, parent, videoPath, videoID, marqueCour, boolCreer):
        super(FormGererNote, self).__init__()
        QDialog.__init__(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.parent = parent
        self.videoPath = videoPath
        self.videoID = videoID
        self.marqueCour = marqueCour
        self.lienCour = -1
        self.setWindowTitle('Gestion des notes')

        self.setGeometry(100, 100, 640, 700)
        # self.setFixedHeight(820)

        self.setupUI()

        self.boolCreer = True

        self.boolCreerTitre = boolCreer
        self.boolCreerImage = boolCreer
        self.boolCreerTexte = boolCreer
        self.boolCreerWeb = boolCreer

        self.boolCadreRougeTitre = True
        self.boolCadreRougeImage = True
        self.boolCadreRougeTexte = True
        self.boolCadreRougeURL = True

        self.cleTitreCour = 0
        self.cleImageCour = 0
        self.cleTexteCour = 0
        self.cleWebCour = 0

        # img = self.extractPicture(self.videoPath, 266, 431, self.marqueCour)
        # qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

    def setupUI(self):
        # **************************************************************
        #  Layout Principal
        # **************************************************************
        self.lytMain = QVBoxLayout()
        self.setLayout(self.lytMain)
        #  Entete
        lytEntete = QHBoxLayout()
        self.lytMain.addLayout(lytEntete)
        query = QSqlQuery()
        query.exec(f'SELECT texte FROM paragraph where clevideo={self.videoID} AND titre={True} AND timeNote={0}')
        if query.next():
            lblEntete = QLabel(query.value('texte'))
            lblEntete.setFont(QFont('Arial', 12))
            lblEntete.setFixedHeight(50)
            lblEntete.setStyleSheet('color: gray')
            lytEntete.addWidget(lblEntete)
            spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            lytEntete.addItem(spacerItem)
            lblTimeCode = QLabel()
            lblTimeCode.setFixedHeight(50)
            lblTimeCode.setText(f'Timecode : {strTime(self.marqueCour)}')
            lytEntete.addWidget(lblTimeCode)
        # **************************************************************
        #  Titre
        # **************************************************************
        lytTitre = QVBoxLayout()
        self.lytMain.addLayout(lytTitre)
        self.tedTitre = QTextEdit()
        self.tedTitre.setPlaceholderText('Saisir ou modifier le titre de la vidéo')
        self.tedTitre.setStyleSheet('border: 1px solid red')
        self.tedTitre.setFixedHeight(55)
        self.tedTitre.setFont(QFont('Arial', 12))
        lytTitre.addWidget(self.tedTitre)
        # **************************************************************
        #  Note
        # **************************************************************
        self.listLien = []
        lytTexte = QVBoxLayout()
        self.lytMain.addLayout(lytTexte)
        self.btnTexte = QPushButton(self)
        self.btnTexte.setText('Mode HTML')
        self.btnTexte.clicked.connect(self.modeTexte)
        lytTexte.addWidget(self.btnTexte)

        self.tedTexte = QTextBrowser()
        self.tedTexte.setFont(QFont('Arial', 10))
        self.tedTexte.setReadOnly(False)
        self.tedTexte.setStyleSheet('border: 1px solid red')
        self.tedTexte.setFixedHeight(150)
        self.tedTexte.setPlaceholderText("Saisir ou modifier la note de la vidéo.\nPour créer un tag, "
                                         "sélectionner le mot et taper Ctrl+T. "
                                         "\nPour ajouter un lien URL sélectionner le mot et taper Ctrl+L.")
        lytTexte.addWidget(self.tedTexte)

        # **************************************************************
        #  Image
        # **************************************************************
        lytImage = QVBoxLayout()
        self.lytMain.addLayout(lytImage)
        self.grpBoxImage = QGroupBox()
        self.grpBoxImage.setStyleSheet('QGroupBox{border: 1px solid red}')
        self.grpBoxImage.setFixedHeight(200)
        lytSubImage = QVBoxLayout(self.grpBoxImage)
        lytImage.addWidget(self.grpBoxImage)
        self.lblImage = QLabel()
        self.lblImage.setStyleSheet('border-radius: 10px; border: 1px solid gray; margin-left: 180px')
        lytSubImage.addWidget(self.lblImage)

        img = self.extractPicture(self.videoPath, 266, 431, self.marqueCour)
        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(qimg)
        self.lblImage.setPixmap(pixmap01.scaled(215, 133, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblImage.setFixedSize(QSize(400, 133))
        lytImage.addWidget(self.grpBoxImage)
        lytBottomImage = QHBoxLayout()
        lytSubImage.addLayout(lytBottomImage)
        self.lneLegende = QLineEdit()
        lytBottomImage.addWidget(self.lneLegende)
        self.lneLegende.setPlaceholderText("Saisir la légende de l'image")
        self.chkIcone = QCheckBox('Vignette')
        lytBottomImage.addWidget(self.chkIcone)
        self.chkIgnorer = QCheckBox("Ignorer l'image")

        lytBottomImage.addWidget(self.chkIgnorer)

        self.chkIgnorer.setChecked(True)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lytMain.addItem(spacerItem)
        # **************************************************************
        #  Tag
        # **************************************************************
        self.grpBoxTag = GrpBoxTag(self, self.videoID, self.lytMain)
        self.lytMain.addWidget(self.grpBoxTag)
        # **************************************************************
        #  Boutons
        # **************************************************************
        lytBouton = QHBoxLayout()
        self.lytMain.addLayout(lytBouton)
        self.btnSauver = QPushButton('Sauver')
        self.btnSauver.setFixedSize(QSize(90, 30))
        lytBouton.addWidget(self.btnSauver)
        self.btnAnnuler = QPushButton('Annuler')
        self.btnAnnuler.setFixedSize(QSize(90, 30))
        lytBouton.addWidget(self.btnAnnuler)
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytBouton.addItem(spacerItem)

        self.btnSauver.clicked.connect(self.evt_btnSauver_clicked)
        # self.btnLienWeb.clicked.connect(self.evt_btnLienWeb_clicked)
        self.btnAnnuler.clicked.connect(self.close)
        self.tedTitre.textChanged.connect(self.evt_tedTitre_textChanged)
        self.tedTexte.textChanged.connect(self.evt_tedTexte_textChanged)
        # self.lneURL.textChanged.connect(self.evt_lneURL_textChanged)
        self.chkIgnorer.stateChanged.connect(self.evt_chkIgnorer_stateChanged)

        self.shortcutTag = QShortcut(QKeySequence('Ctrl+T'), self)
        self.shortcutLien = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcutTag.activated.connect(self.creerTag)
        self.shortcutLien.activated.connect(self.creerLien)

    def populateLien(self):
        self.tedTexte.setReadOnly(True)
        # cursor = self.tedTexte.textCursor()
        # lien = cursor.selectedText()
        auxText = self.tedTexte.toPlainText()

        self.listLien = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM linkTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
        while query.next():
            self.listLien.append((query.value('mot'), query.value('url')))

        for tpl in self.listLien:

            mot, url = tpl
            auxHTML = f'<a href="{url}" target="_blank">{mot}</a>'
            auxText = auxText.replace(mot, auxHTML)
            auxText = auxText.replace(chr(10), '<br>')  # Remplacer les retours à la ligne en HTML
        self.tedTexte.setText("<p>" + auxText + "</p>")
        self.tedTexte.setOpenExternalLinks(True)
        self.btnTexte.setText('Mode texte')

    def modeTexte(self):
        if self.btnTexte.text() == 'Mode HTML':
            self.tedTexte.setReadOnly(True)
            self.btnTexte.setText('Mode texte')
        else:
            self.tedTexte.setReadOnly(False)
            self.btnTexte.setText('Mode HTML')

    def closeEvent(self, event):
        query = QSqlQuery()
        bOK = query.exec(f'SELECT cle FROM paragraph WHERE cleVideo={self.videoID} AND timeNote={self.marqueCour}')
        if query.next():
            pass
        else: #  Les notes correspondant aux tags et aux liens créés n'ont pas été enregistrées. il faut les supprimer
            query = QSqlQuery()
            query.exec(f'DELETE FROM tagTab WHERE timeCode={self.marqueCour} AND cleVideo={self.videoID}')

        query = QSqlQuery()
        bOK = query.exec(f'SELECT cle FROM paragraph WHERE cleVideo={self.videoID} AND timeNote={self.marqueCour} '
                         f'AND Note={True}')
        if query.next():
            pass
        else:  # Les notes correspondant aux tags et aux liens créés n'ont pas été enregistrées. il faut les supprimer
            query = QSqlQuery()
            query.exec(f'DELETE FROM linkTab WHERE timeCode={self.marqueCour} AND cleVideo={self.videoID}')


    def  creerTag(self):
        cur = self.tedTexte.textCursor()
        tag = cur.selectedText()
        if tag == '':
            return

        self.tedTexte.setTextCursor(cur)
        cur.clearSelection()
        self.grpBoxTag.lneTag.setText(tag)
        self.grpBoxTag.sauverTag()

    def creerLien(self):
        self.tedTexte.setReadOnly(True)
        cursor = self.tedTexte.textCursor()
        lien = cursor.selectedText()
        if len(lien) == 0:
            QMessageBox.information(self, "Création d'un lien Web, 'Saisir un titre et sélectionnez le.")
            return
        text, ok = QInputDialog.getText(self, 'Insérer une page web', "Saisir l'URL")
        if ok:
            self.listLien.append((lien, text))
        else:
            return
        auxText = self.tedTexte.toPlainText()
        auxText = auxText.replace(chr(10), '<br>')  # Remplacer les retours à la ligne en HTML

        for tpl in self.listLien:
            mot, url = tpl
            auxHTML = f'<a href="{url}" target="_blank">{mot}</a>'
            auxText = auxText.replace(mot, auxHTML)
        self.tedTexte.setText(auxText)
        self.tedTexte.setOpenExternalLinks(True)

        self.btnTexte.setText('Mode texte')

    def evt_chkIgnorer_stateChanged(self):
        self.btnSauver.setIcon(QIcon(None))
        if self.chkIgnorer.isChecked():
            self.grpBoxImage.setStyleSheet('QGroupBox{border: 1px solid red}')
            self.boolCadreRougeImage = True
        else:
            self.grpBoxImage.setStyleSheet('QGroupBox{border: 1px solid #455364}')
            self.boolCadreRougeImage = False

    def evt_tedTitre_textChanged(self):
        self.btnSauver.setIcon(QIcon(None))
        if self.tedTitre.toPlainText() == '':
            self.tedTitre.setStyleSheet('border: 1px solid red')
            self.boolCadreRougeTitre = True
        else:
            self.tedTitre.setStyleSheet('border: 1px solid #455364;')
            self.boolCadreRougeTitre = False

    def evt_tedTexte_textChanged(self):
        self.btnSauver.setIcon(QIcon(None))
        if self.tedTexte.toPlainText() == '':
            self.tedTexte.setStyleSheet('border: 1px solid red')
            self.boolCadreRougeTexte = True
        else:
            self.tedTexte.setStyleSheet('border: 1px solid #455364;')
            self.boolCadreRougeTexte = False

    def evt_lneURL_textChanged(self):
        self.btnSauver.setIcon(QIcon(None))
        if self.lneURL.text() == '':
            self.lneURL.setStyleSheet('border: 1px solid red')
            self.boolCadreRougeURL = True
        else:
            self.lneURL.setStyleSheet('border: 1px solid #455364;')
            self.boolCadreRougeURL = False

    def evt_lneLegende_textChanged(self):
        self.btnSauver.setIcon(QIcon(None))
        if self.lneLegende.text() == '':
            self.lneLegende.setStyleSheet('border: 1px solid red')
        else:
            self.lneLegende.setStyleSheet('border: 1px solid #455364;')

    def evt_btnLienWeb_clicked(self):
        if self.grpBoxTag.lneTag.hasFocus():
            return
        mainWindow.URLCour = self.lneURL.text()
        win = FormWebBrowser(self)
        win.resize(QSize(600, 500))
        win.show()

    def evt_btnSauver_clicked(self):
        message = ''
        if self.boolCadreRougeTitre:
            message += 'Titre'
        if self.boolCadreRougeImage:
            if message != '':
                message += ', image'
            else:
                message += 'image'
        if self.boolCadreRougeTexte:
            if message != '':
                message += ', note'
            else:
                message += 'note'
        if self.boolCadreRougeURL:
            if message != '':
                message += ', lien Web'
            else:
                message += 'lienWeb'

        if message != '':
            rep = QMessageBox.question(self, 'Enregistrement', f"Les éléments suivants : {message} \n"
                                                               f"sont encadrés en rouge et ne seront pas enregistrés.\n\n "
                                                               "S'ils ont déjà été créés, ils seront supprimés.\n\n"
                                                               "Confirmez-vous l'opération?")
            if rep == QMessageBox.No:
                QMessageBox.information(self, 'Enregistrement', 'Opération abandonnée.')
                return
        if 1:
            #  ********************************************************************************
            #  Cas du titre
            #  ********************************************************************************
            if self.cleTitreCour == 0:  # Cas d'une création
                #  recherche de l'index suivant par la primary key
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                #  Cas d'une création
                if self.boolCreer:
                    self.cleTitreCour = maxCle
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                                 'cleVideo', 'cle', 'icone', 'note', 'lienWeb')
                    txt = self.tedTitre.toPlainText().replace(chr(10), '$$')
                    txt = txt.replace(chr(34), ')|')  # guillements
                    txt = txt.replace(chr(9), 'µµ')  # Tabulation
                    tplData = (self.marqueCour, 0, True, False, 337, 647, txt, self.videoID, self.cleTitreCour,
                               False, False, False)
                    if self.tedTitre.toPlainText() != '':
                        query = QSqlQuery()
                        query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                        #  Recherche des tags avec une clé de Note à -99 pour la mettre à maxCle
                        tplChamps = ('cleVideo', 'cleParagraph')
                        tplData = (self.videoID, maxCle)
                        queryTag = QSqlQuery()
                        queryTag.exec(f'UPDATE tagTab  SET {tplChamps} = {tplData} WHERE '
                                      f'cleParagraph = -99')
            #  Cas d'une modification
            else:
                if self.tedTitre.toPlainText() == '':
                    # Suppression
                    query = QSqlQuery()
                    bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleTitreCour}')
                else:
                    query = QSqlQuery()
                    txt = self.tedTitre.toPlainText().replace(chr(10), '$$')
                    txt = txt.replace(chr(34), ')|')  # guillements
                    txt = txt.replace(chr(9), 'µµ')  # Tabulation
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                 'texte', 'cleVideo', 'icone', 'Note', 'lienWeb')
                    tplData = (self.marqueCour, 0, True, False, 337, 647, txt
                               , self.videoID, False, False, False)
                    bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                     f'cle = {self.cleTitreCour}')
            #  ********************************************************************************
            #  Cas de la note
            #  ********************************************************************************
            if self.cleTexteCour == 0:  # Cas d'une création
                #  recherche de l'index suivant par la primary key
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                self.cleTexteCour = maxCle
                tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                             'cleVideo', 'cle', 'icone', 'note', 'lienWeb')
                txt = self.tedTexte.toPlainText().replace(chr(10), '$$')
                txt = txt.replace(chr(34), ')|')  # guillements
                txt = txt.replace(chr(9), 'µµ')  # Tabulation
                tplData = (self.marqueCour, 0, False, False, 337, 647, txt, self.videoID, self.cleTexteCour,
                           False, True, False)
                if self.tedTexte.toPlainText() != '':
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                    #  Recherche des tags avec une clé de Note à -99 pour la mettre à maxCle
                    tplChamps = ('cleVideo', 'cleParagraph')
                    tplData = (self.videoID, maxCle)
                    queryTag = QSqlQuery()
                    queryTag.exec(f'UPDATE tagTab  SET {tplChamps} = {tplData} WHERE '
                                  f'cleParagraph = -99')
            #  Cas d'une modification
            else:
                if self.tedTexte.toPlainText() == '':
                    # Suppression
                    query = QSqlQuery()
                    bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleTexteCour}')
                else:
                    txt = self.tedTexte.toPlainText().replace(chr(10), '$$')
                    txt = txt.replace(chr(34), ')|')  # guillements
                    txt = txt.replace(chr(9), 'µµ')  # Tabulation
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                 'texte', 'cleVideo', 'icone', 'Note', 'lienWeb')
                    tplData = (self.marqueCour, 0, False, False, 337, 647, txt
                               , self.videoID, False, True, False)
                    query = QSqlQuery()
                    bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                     f'cle = {self.cleTexteCour}')
            #  ********************************************************************************
            #  cas de l'image
            #  ********************************************************************************
            query = QSqlQuery()
            bOk = query.exec(f'SELECT icone, cle FROM paragraph WHERE cleVideo={self.videoID}')
            if query.next():
                tplChamps = ('cleVideo', 'icone')
                tplData = (self.videoID, False)
                bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE cle = {query.value("cle")}')
            #  recherche de l'index suivant par la primary key
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) FROM paragraph')
            try:
                if query.next():
                    maxCle = query.value(0) + 1
            except:
                maxCle = 1
            #  Cas d'une création
            if self.cleImageCour == 0:
                # if self.boolCreer or self.cleImageCour == 0:
                self.cleImageCour = maxCle
                tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                             'cleVideo', 'cle', 'icone', 'note', 'lienWeb')
                txt = self.lneLegende.text()
                tplData = (self.marqueCour, 0, False, True, 337, 647, txt, self.videoID, self.cleImageCour,
                           self.chkIcone.isChecked(), False, False)
                if not self.chkIgnorer.checkState():
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                    #  Recherche des tags avec une clé de Note à -99 pour la mettre à maxCle
                    tplChamps = ('cleVideo', 'cleParagraph')
                    tplData = (self.videoID, maxCle)
                    queryTag = QSqlQuery()
                    queryTag.exec(f'UPDATE tagTab  SET {tplChamps} = {tplData} WHERE '
                                  f'cleParagraph = -99')
            #  Cas d'une modification
            else:
                if self.chkIgnorer.isChecked():
                    # Suppression
                    query = QSqlQuery()
                    bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleImageCour}')
                else:
                    txt = self.lneLegende.text()
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                 'texte', 'cleVideo', 'Icone', 'Note', 'lienWeb')
                    tplData = (self.marqueCour, 0, False, True, 337, 647, txt
                               , self.videoID, self.chkIcone.isChecked(), False, False)
                    bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                     f'cle = {self.cleImageCour}')
            #  ********************************************************************************
            #  Cas du lien Web
            #  ********************************************************************************
            #  Effacer les liens dans la table linkTab
            query.exec(f'DELETE FROM linkTab WHERE timeCode={self.marqueCour} AND cleVideo={self.videoID}')
            #  Enregistrer les liens mis à jour
            for tpl in self.listLien:
                #  recherche de l'index suivant par la primary key
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM linkTab')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1

                mot, url = tpl
                query1 = QSqlQuery()
                tplChamps = ('timeCode', 'mot', 'url', 'cleVideo', 'cle')
                tplData = (self.marqueCour, mot, url, self.videoID, maxCle)
                query1.exec(f'INSERT INTO linkTab {tplChamps} VALUES {tplData}')

        self.boolCreer = False
        QMessageBox.information(self, "Enregistrement", "L'opération a été réalisée.")
        self.btnSauver.setIcon(QIcon('ressources/cocher.png'))
        formScreen1.marqueNote.marqueCour = self.marqueCour
        objNote.populateObjNote(self.videoID)
        self.close()

    def modifParagraph(self, paragraphCour):
        self.paragraphCour = paragraphCour
        if paragraphCour.picture:
            self.lneLegende.setText(paragraphCour.texte)
            self.chkIcone.setChecked(paragraphCour.icone)
            self.cleImageCour = paragraphCour.cle
            self.testBloc(paragraphCour)
            if self.cleImageCour != 0:
                self.chkIgnorer.setChecked(False)
            else:
                self.chkIgnorer.setChecked(True)

        if paragraphCour.titre:
            self.tedTitre.setText(paragraphCour.texte)
            self.cleTitreCour = paragraphCour.cle
            self.miseEnFormeTag(self.tedTitre, paragraphCour.cleVideo)
            self.testBloc(paragraphCour)

        if paragraphCour.note:
            self.tedTexte.setText(paragraphCour.texte)
            self.cleTexteCour = paragraphCour.cle
            self.miseEnFormeTag(self.tedTexte, paragraphCour.cleVideo)
            self.testBloc(paragraphCour)
            self.populateLien()

        if paragraphCour.lienWeb:
            self.lneURL.setText(paragraphCour.texte)
            self.cleWebCour = paragraphCour.cle
            self.testBloc(paragraphCour)

    def testBloc(self, paragraphCour):
        #  recherche d'éventuelle note dans le même bloc
        query = QSqlQuery()
        query.exec(f'SELECT * FROM paragraph where cleVideo={paragraphCour.cleVideo} '
                   f'and timeNote={paragraphCour.timeNote}')
        while query.next():
            if query.value('cle') != paragraphCour.cle:
                if query.value('picture'):
                    self.cleImageCour = query.value('cle')
                    self.lneLegende.setText(query.value('texte'))
                    self.chkIcone.setChecked(query.value('icone'))
                    if self.cleImageCour != 0:
                        self.chkIgnorer.setChecked(False)
                    else:
                        self.chkIgnorer.setChecked(True)
                if query.value('note'):
                    self.cleTexteCour = query.value('cle')
                    auxText = query.value('texte')
                    auxText = auxText.replace('$$', chr(10))
                    auxText = auxText.replace(')|', chr(34))
                    auxText = auxText.replace('µµ', chr(9))
                    auxText = auxText.replace(chr(10), '<br>')
                    auxText = "<p>" + auxText + "</p>"
                    self.tedTexte.setText(auxText)
                    self.populateLien()
                if query.value('titre'):
                    self.cleTitreCour = query.value('cle')
                    self.tedTitre.setText(query.value('texte'))
                    self.miseEnFormeTag(self.tedTexte, paragraphCour.cleVideo)

    def miseEnFormeTag(self, widget, cleVideo):
        #  Mise en page
        texte = widget.toPlainText().replace('$$', chr(10))
        texte = texte.replace(')|', chr(34))
        texte = texte.replace('µµ', chr(9))
        widget.setText(texte)
        return
        #  Affichage des tags
        #  Collecter les tags de la vidéo concernée
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={cleVideo}')
        while query.next():
            mot = query.value('mot')
            cursor = widget.textCursor()
            format = QTextCharFormat()
            format.setForeground(QColor(102, 204, 204))
            pattern = mot
            regex = QRegExp(pattern)
            pos = 0
            index = regex.indexIn(widget.toPlainText(), pos)
            while (index != -1):
                cursor.setPosition(index)
                cursor.movePosition(QTextCursor.EndOfWord, 1)
                cursor.mergeCharFormat(format)
                pos = index + regex.matchedLength()
                index = regex.indexIn(widget.toPlainText(), pos)

    def extractPicture(self, video, haut, large, timeNote):
        vidcap = cv2.VideoCapture(video)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
        success, image = vidcap.read()
        if success:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            M A R Q U E N O T E            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MarqueNote(QLabel):
    def __init__(self, parent=None, videoID=None, duration=None):
        super(MarqueNote, self).__init__()
        # self.setFixedHeight(50)
        # self.setStyleSheet('background-color: orange')

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

        # btnPlus = QPushButton(self)
        # btnPlus.setIcon(QIcon('ressources/btnPlus.png'))
        # btnPlus.setFixedSize(QSize(22, 22))
        # btnPlus.move(83, 25)
        # btnPlus.setCursor(QCursor(Qt.PointingHandCursor))
        # btnMoins = QPushButton(self)
        # btnMoins.setIcon(QIcon('ressources/btnMoins.png'))
        # btnMoins.setFixedSize(QSize(22, 22))
        # btnMoins.move(0, 25)
        # btnMoins.setCursor(QCursor(Qt.PointingHandCursor))
        # self.lblPlusMoins = QPushButton(self)
        # self.lblPlusMoins.setText('Editer')
        # self.lblPlusMoins.setFixedSize(QSize(70, 22))
        # self.lblPlusMoins.move(18, 25)
        # # self.lblPlusMoins.setAlignment(Qt.AlignCenter)
        # self.lblPlusMoins.setStyleSheet('background-color: #455364')
        # self.lblPlusMoins.setCursor(QCursor(Qt.PointingHandCursor))
        #
        # btnMoins.clicked.connect(self.evt_btnMoins_clicked)
        # btnPlus.clicked.connect(self.evt_btnPlus_clicked)
        # self.lblPlusMoins.clicked.connect(self.evt_lblPlusmoins_clicked)

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
# ***************               L A B E L T A G             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelTag(QLabel):
    def __init__(self, parent, texte, coulor):
        # QLabel.__init__(self, parent)
        super(LabelTag, self).__init__(parent)
        self.texte = texte
        self.styleDeselect = f'color: white; background-color: {coulor}; border: 1px solid {coulor}; border-radius: 10px'
        self.styleSelect = f'color: white; background-color: #f05a24; border: 1px solid {coulor}; border-radius: 10px'
        self.setStyleSheet(self.styleDeselect)
        self.setFixedSize(50, 50)
        width = self.fontMetrics().boundingRect(texte).width()
        self.parent = parent
        self.width = width
        self.setFixedWidth(width + 20)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignCenter)
        self.largeur = self.width
        self.setText(texte)
        self.boolSelect = False

    def setPosition(self, x, y):
        self.move(x, y)

    def majEtatSelect(self):
        if self.boolSelect:
            self.boolSelect = False
            self.setStyleSheet(self.styleDeselect)
        else:
            self.boolSelect = True
            self.setStyleSheet(self.styleSelect)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             G R P B O X T A G             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GrpBoxTag(QGroupBox):
    def __init__(self, parent, videoID, lytMain):
        super().__init__()
        # self.setFixedWidth(640)
        # self.setFixedHeight(250)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumHeight(240)
        self.parent = parent
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False
        self.setStyleSheet('margin: 0px')
        self.lneTag = QLineEdit(self)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.lneTag.setStyleSheet('margin: 0px')
        self.lneTag.setFixedWidth(640)
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
        # QMessageBox.information(self, 'toto', 'titi')
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
        #  la cle correspodant au tag concerné
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
        if query.next():
            cle = query.value('cle')
        rep = QMessageBox.question(self, 'Supprimer ce tag', 'Confirmez-vous la suppression?')
        if rep == QMessageBox.Yes:
            query = QSqlQuery()
            bOK = query.exec(f'DELETE FROM tagTab WHERE cle = {cle}')
        self.populateGrpBoxAffichTag()

    def modifTag(self):
        self.lneTag.setText(self.motCour)
        self.boolModif = True
        #  la cle correspodant au tag concerné
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
        if query.next():
            cle = query.value('cle')

    def sauverTag(self):

        #  Vérifier l'existence du tag en doublon
        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))
        mot = self.lneTag.text()

        if mot in self.listTag:
            QMessageBox.information(self, 'Enregistrement annulé', 'Le tag existe déja pour cette vidéo.')
        else:
            if self.boolModif:
                #  la cle correspodant au tag concerné
                query = QSqlQuery()
                query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
                if query.next():
                    cle = query.value('cle')
                query = QSqlQuery()
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                tplData = (cle, self.parent.marqueCour, self.lneTag.text(), self.videoID)
                bOk = query.exec(f'UPDATE tagTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
                self.populateGrpBoxAffichTag()
            else:
                #  Recherche de l'index suivant
                cleMax = 1
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) AS cleMax FROM tagTab')
                try:
                    if query.next():
                        cleMax = query.value('cleMax') + 1
                except:
                    pass
                # #  -99 cle provisoire de la note attachée au tag dans le cas où la note est en cours de création
                # #  en cas de modification d'une note existante : on récupère la clé de la note concernée
                # try:
                #     cleParagraphAux = self.parent.paragraphCour.cle
                # except:
                #     cleParagraphAux = -99
                tplData = (cleMax, self.parent.marqueCour, mot, self.videoID)
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                query1 = QSqlQuery()
                query1.exec(f'INSERT INTO tagTab {tplChamps} VALUES {tplData}')
                self.listTag.append(mot)
        self.lneTag.setText('')
        self.boolModif = False
        self.populateGrpBoxAffichTag()

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
        #  Mise à jour de la listTag
        #  1 -  Recherche des note d'un éventuel bloc partageant le même timeCode
        timeCode = self.parent.marqueCour
        # query = QSqlQuery()
        # query.exec(f'SELECT cle FROM paragraph WHERE timeNote = {timeCode}')
        # requete = ''
        # while query.next():
        #     requete += f' cleParagraph={query.value("cle")} OR'
        # requete = f' AND ({requete[:-3]})'
        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND timeCode={timeCode}')
        while query.next():
            self.listTag.append(query.value('mot'))

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
        # gprBox.setFixedHeight(50)
        lyt = QHBoxLayout()
        grpBox.setLayout(lyt)
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(self.listTag[i], '#2e8cff')
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


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        F O R M W E B B R O W S E R          *********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(FormWebBrowser, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 500, 500)

        self.URL = mainWindow.URLCour
        self.browser.setUrl(QUrl(self.URL))

        # adding action when url get changed
        self.browser.urlChanged.connect(self.update_urlbar)

        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)

        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)

        # creating a status bar object
        self.status = QStatusBar()

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # adding this tool bar tot he main window
        self.addToolBar(navtb)

        # adding actions to the tool bar
        # creating a action for back
        back_btn = QAction("Back", self)

        # setting status tip
        back_btn.setStatusTip("Back to previous page")

        # adding action to the back button
        # making browser go back
        back_btn.triggered.connect(self.browser.back)

        # adding this action to tool bar
        navtb.addAction(back_btn)

        # similarly for forward action
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")

        # adding action to the next button
        # making browser go forward
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # similarly for reload action
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")

        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # similarly for home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # adding a separator in the tool bar
        navtb.addSeparator()

        # creating a line edit for the url
        self.urlbar = QLineEdit()

        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding this to the tool bar
        navtb.addWidget(self.urlbar)

        # adding stop action to the tool bar
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")

        # adding action to the stop button
        # making browser to stop
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # showing all the components
        self.show()

    # method for updating the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Geek Browser" % title)

    # method called by the home action
    def navigate_home(self):
        # open the google
        self.browser.setUrl(QUrl("http://www.google.com"))

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())

        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("http")

        # set the url to the browser
        self.browser.setUrl(q)

    # method for updating url
    # this method is called by the QWebEngineView object
    def update_urlbar(self, q):
        # setting text to the url bar
        self.urlbar.setText(q.toString())
        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             N A V F I C H I E R S         ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class NavigFichiers(QMainWindow):

    # =========================================================================
    def __init__(self, repertoire, parent=None):
        super().__init__(parent)

        self.resize(300, 400)
        # self.setStyleSheet('background-color: orange')
        self.setWindowTitle("Navigateur de fichiers")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: black')

        # crée le modèle
        model = QFileSystemModel()
        model.setRootPath(repertoire)


        # Crée le QTreeView et intégre le modèle
        self.view = QTreeView()
        self.view.setModel(model)
        self.view.setRootIndex(model.index(repertoire))
        f = open('styles/QTreeView.txt', 'r')
        style = f.read()
        styleQTreeView = style
        # self.view.setStyleSheet('QHeaderView::section {color: #ffffff; background-color: #000000;} '
        #                         'QTreeView {background-color: black; color: white; border: 0px}')
        self.view.setStyleSheet(styleQTreeView )

        # Police de caractères à utiliser
        font = QFont()
        font.setStyleHint(QFont.Monospace)
        self.view.setFont(font)

        # largeur de la colonne 0
        self.view.setColumnWidth(0, 350)

        # place le QTreeView dans la fenêtre
        self.setCentralWidget(QFrame())
        layout = QGridLayout()
        layout.addWidget(self.view, 0, 0)
        self.centralWidget().setLayout(layout)

        # Etablissement lien entre signal et méthode
        self.view.clicked.connect(self.clicligne)

    # =========================================================================
    def clicligne(self, qindex):

        nom = self.view.model().fileName(qindex)
        chemin = self.view.model().filePath(qindex)
        if os.path.isdir(chemin):
            print("Répertoire:", nom, "===> avec chemin:", chemin)
        else:
            print("fichier:", nom, "===> avec chemin:", chemin)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                P U S H O N G L E T             ******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class PushOnglet(QLabel):
    def __init__(self, parent=None, cleVideo=None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(125, 55)
        self.setAlignment(Qt.AlignTop)
        self.styleDesabled = 'QLabel {background-color: #60798B; border-top-left-radius: 7px; padding: 0px; ' \
                        'border-top-right-radius: 7px; color: white; padding-left: 4px;} ' \
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
            self.setText(videoCour.titreVideo + '...')


        self.btnRemove = QPushButton(self)
        self.btnRemove.setFixedSize(25, 25)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(11)
        font.setBold(True)
        self.btnRemove.setFont(font)
        self.btnRemove.setText('X')
        self.btnRemove.setStyleSheet('QPushButton {background-color: transparent; color: #E0E1E3; border-radius: 4px; '
                                     'padding: 2px; outline: none; border: none} '
                                     'QPushButton::hover{color: red;}')
        self.btnRemove.move(103, 0)
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
        self.setGeometry(100, 100, 500, 600)
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
        self.grpBoxOnglet.setFixedHeight(40)
        self.grpBoxOnglet.setStyleSheet('border: 0px; background-color: #333333')
        lytOnglet.addWidget(self.grpBoxOnglet)
        lyt = QHBoxLayout()
        lyt.setSpacing(2)
        self.grpBoxOnglet.setLayout(lyt)

        self.styleDesabled = 'QLabel {background-color: #60798B; border-top-left-radius: 7px; padding: 0px; ' \
                             'border-top-right-radius: 7px; color: white; padding-left: 4px;} ' \
                             'QLabel::hover {background-color: #555588}'
        self.styleEnabled = 'QLabel {background-color: #455364; border-top-left-radius: 7px; padding: 0px; ' \
                            'border-top-right-radius: 7px; color: white; padding-left: 4px; border: 0px solid 455364} ' \
                            'QLabel::hover {background-color: #555588}'

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
            self.btnPlus.setFixedSize(32, 32)
            self.btnPlus.setText('+')
            self.btnPlus.setStyleSheet('QPushButton {background-color: #60798B; color: #E0E1E3; border-radius: 4px; '
                                         'padding: 2px; outline: none; border: none} QPushButton::hover{color: red;'
                                       ' background-color: #455364}')
            self.btnPlus.setFont(QFont('Arial', 20))
            lyt.addWidget(self.btnPlus)
            spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            lyt.addItem(spacerItem)

        self.btnPlus.clicked.connect(mainWindow.evt_btnPlusTab_clicked)

    def createFormScreen1(self):
        qwidget = QWidget()
        qwidget.setStyleSheet('background-color: orange')
        global formScreen1
        try:
            if formScreen1:
                formScreen1.close()
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
# ***************            G R I D V I G N E T T E        ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GridVignette(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: #222222; border: 0px')
        self.lstVideo = []
        self.lstVignette1 = []
        self.initUI()
        self.indexCour = -1

    def initUI(self):
        # ***************************************************************
        # ******  Construction du complexe QScrollArea
        # ***************************************************************
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.grpBox = QGroupBox()


        self.grpBox.setFixedHeight(5000)
        self.widget.setLayout(self.vbox)
        self.vbox.addWidget(self.grpBox)
        self.widget.resizeEvent = self.onResize

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        styleQGroupBox = style
        self.scroll.setStyleSheet(styleQGroupBox)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 997, 631)
        # self.show()
        self.populateGrpBox(self.lstVideo)


    def populateGrpBox(self, lstVideo):
        self.lstVideo = lstVideo
        lenLstVideo = len(self.lstVideo)
        if lenLstVideo == 0:
            return
        #  Effacer le GrpBox
        for itm in self.grpBox.findChildren(LabelIndex):
            itm.deleteLater()
        for itm in self.grpBox.findChildren(QLabel):
            itm.deleteLater()

        self.lstVignette1 = []
        self.nbLigne = lenLstVideo // 4
        resteColonne = lenLstVideo % 4
        if resteColonne > 0:
            self.nbLigne += 1

        if lenLstVideo <= 28:
            self.nbLigne = 5
        listeSQL, lstVignetteOnglet = mainWindow.filtreCour
        lstVignetteOnglet = [lbl.index for (lbl, lblTitre) in lstVignetteOnglet if lbl.boolOnglet]

        for ligne in range(0, self.nbLigne):
            for colonne in range(0, 4):
                index = ligne * 4 + colonne
                if index < lenLstVideo:
                    # ****************************************************************
                    #  VIGNETTE
                    # ****************************************************************
                    vidcap = cv2.VideoCapture(mainWindow.racine + self.lstVideo[index].internalPath
                                              + self.lstVideo[index].videoName)
                    vidcap.set(cv2.CAP_PROP_POS_MSEC, self.lstVideo[index].timeCodeIcone * 1000)
                    success, image = vidcap.read()
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if success:
                        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                        pixmap01 = QPixmap.fromImage(image)
                    lbl = QLabel(self.grpBox)
                    lbl = LabelIndex(self.grpBox, self.lstVideo[index].cle, pixmap01, ligne, colonne)
                    lbl.setStyleSheet('border: 1px solid #000000; border-radius: 9px')
                    # shadow = QGraphicsDropShadowEffect()
                    # shadow.setBlurRadius(15)
                    # lbl.setGraphicsEffect(shadow)

                    lbl.installEventFilter(self)
                    #  Mise à jour des vignettes marquées pour l'onglet
                    if self.lstVideo[index].cle in lstVignetteOnglet:
                        lbl.mousePressEventMethod()
                    # ****************************************************************
                    #  TITRE VIDEO
                    # ****************************************************************
                    lblTitre = QLabel(self.grpBox)
                    lblTitre.setWordWrap(True)
                    duree = self.videoDuration(f'{mainWindow.racine}{self.lstVideo[index].internalPath}'
                                               f'{self.lstVideo[index].videoName}')

                    aux = self.lstVideo[index].titreVideo.replace('$$', chr(10))
                    aux = aux.replace(')|', chr(34))  # guillements
                    aux = aux.replace('µµ', chr(9))  # Tabulation
                    auxHTML = f'<p><FONT color="#eeeeee"><FONT size=4>{aux}</FONT><br>Durée: {self.strTime(duree)}</p>'
                    lblTitre.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                    lblTitre.setText(auxHTML)
                    # ****************************************************************
                    self.lstVignette1.append((lbl, lblTitre))
                    newSize = QSize(self.grpBox.width(), self.grpBox.height())

        self.onResize(QResizeEvent)

    def onResize(self, event):
        if len(self.lstVignette1) == 0:
            return

        w = self.grpBox.width()
        h = self.grpBox.height()
        x = w // 5
        y = int(x * 0.74)
        y = int(x * 9 / 16)
        bord = 15
        marge = (w - 4 * x - 2 * bord)//3

        for itm in self.lstVignette1:
            lbl, lblTitre = itm
            #  Vignette
            lbl.setPixmap(lbl.picture.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            lbl.setFixedSize(QSize(x, y))
            if lbl.colonne == 0:
                offset = bord
            else:
                offset = marge
            lbl.move(lbl.colonne * (x + offset) + 10, lbl.ligne * (y + 90))
            self.grpBox.setFixedHeight((self.nbLigne + 1) * (y + 20) + 190)
            #  lblTitre
            lblTitre.setFixedSize(QSize(x, 70))
            # lblTitre.setStyleSheet('background-color: orange')
            lblTitre.move(lbl.colonne * (x + offset) + 10, lbl.ligne * (y + 90) + y)

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

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            self.sourceCour = source
            menu = QMenu()
            menu.addAction(QIcon('ressources/crayon.png'), 'Mode édition',  mainWindow.gridWindow.editVideo)  #  self.editVideo)
            menu.addSeparator()
            menu.addAction(QIcon('ressources/voir.png'), 'Mode étude', self.modeEtude)  #   self.etudeVideo)
            menu.addSeparator()
            if source.boolOnglet:
                menu.addAction(QIcon('ressources/onglet.png'), 'Voir les vidéos', self.voirOnglets)  #  mainWindow.evt_actEtudeVideo_clicked)
            # else:
            #     menu.addAction(QIcon('ressources/onglet.png'), 'Voir les vidéos',  self.test)  #  self.ajouterOnglet)
            if menu.exec_(event.globalPos()):
                return True
        return super().eventFilter(source, event)

    def modeEtude(self):
        self.sourceCour.mouseDoubleClickMethod()

    def voirOnglets(self):
        self.setCursor(Qt.WaitCursor)
        L1 = self.lstVignette1
        L2 = [(lbl, lblTitre) for (lbl, lblTitre) in L1 if lbl.boolOnglet]
        # Stockage des vignettes marquée pour les onglets
        filtreSQL, listTemp = mainWindow.filtreCour
        mainWindow.filtreCour = (filtreSQL, L2)
        L3 = [a.index for (a, b) in L2]
        mainWindow.displayTabWindow(L3)

        return
        for vignette in L2:
            lbl, lblTitre = vignette

            try:
                mainWindow.nbTab = mainWindow.tabWidget.count() + 1
                videoAux = VideoFileRecord(lbl.index)
                mainWindow.tabObjetScreen = TabObjectScreen(mainWindow, videoAux.cle)
                mainWindow.tabWidget.addTab(mainWindow.tabObjetScreen, f'{videoAux.videoName}')
            except:
                videoAux = VideoFileRecord(lbl.index)
                mainWindow.tabWidget = QTabWidget()
                mainWindow.setCentralWidget(mainWindow.tabWidget)
                f = open('styles/OngletVideo.txt', 'r')
                style = f.read()
                styleQTabWidget = style
                mainWindow.tabWidget.setStyleSheet(styleQTabWidget)
                mainWindow.tabWidget.setTabsClosable(True)
                mainWindow.tabWidget.tabCloseRequested.connect(mainWindow.removeTab)
                mainWindow.nbTab = mainWindow.tabWidget.count() + 1
                mainWindow.tabObjetScreen = TabObjectScreen(mainWindow, videoAux.cle)
                mainWindow.tabWidget.addTab(mainWindow.tabObjetScreen, f'{videoAux.videoName}')

            try:
                if mainWindow.btnPlusTab:
                    mainWindow.btnPlusTab.close()
            except:
                pass
            mainWindow.btnPlusTab = QPushButton(mainWindow.tabWidget)
            mainWindow.btnPlusTab.setFixedSize(QSize(28, 28))
            mainWindow.btnPlusTab.setText('+')
            mainWindow.btnPlusTab.setStyleSheet('background-color: #999999; border: 0px')
            mainWindow.btnPlusTab.move((125 * mainWindow.nbTab+3), 2)
            mainWindow.btnPlusTab.setFont(QFont('Arial', 15))
            mainWindow.btnPlusTab.clicked.connect(mainWindow.evt_btnPlusTab_clicked)

        self.unsetCursor()

    def test(self):
        pass


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            G R I D W I N D O W            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GridWindow(QWidget):
    def __init__(self, parent, lstVideo):
        # super(GridWindow, self).__init__()
        QWidget.__init__(self)

        self.parent = parent
        self.lstVideo = []
        self.boolSearch = self.parent.boolSearch
        self.searchString = self.parent.searchString
        self.btnCour = -1
        self.sourceCour = None
        self.listCherche = []
        self.lstVignette = []
        self.lstGridVideo = []
        self._flag = True
        self.lstVideo = lstVideo


        # ***************************************************************
        # ******  Initialisation nb ligne dans la grille
        # ***************************************************************
        self.nbRowGrid = 4
        self.statutCour = -1
        self.classeurCour = -1

        self.initUI1()

    def initUI1(self):
        self.setStyleSheet('background-color: gray')
        lytMain = QVBoxLayout()
        self.setLayout(lytMain)

        #  *********************************************************
        #  Zone Top
        #  *********************************************************
        self.grpTop = QGroupBox()
        f = open('styles/QGroupBox.txt', 'r')
        style = f.read()
        styleQGroupBox = style
        lytTop = QHBoxLayout()
        self.grpTop.setLayout(lytTop)
        self.grpTop.setStyleSheet(styleQGroupBox)
        self.grpTop.setFixedHeight(60)
        lytMain.addWidget(self.grpTop)
        #  *********************************************************
        #  Logo VideoFinder
        lblLogo = QLabel()
        lblLogo.setText('VideoFinder')
        lblLogo.setFont(QFont('Arial', 16))
        lblLogo.setStyleSheet('color: white; background-color: #000000')
        lytTop.addWidget(lblLogo)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytTop.addItem(spacerItem)
        #  *********************************************************

        # Sort listBox
        self.listSortMode = QComboBox()
        f = open('styles/QComboBox.txt', 'r')
        style = f.read()
        styleQComboBox = style
        self.listSortMode.setStyleSheet(styleQComboBox)
        # self.listSortMode.setStyleSheet('color: white; background-color: orange')
        self.listSortMode.setFixedWidth(200)
        self.listSortMode.setFixedHeight(34)
        self.listSortMode.setEditable(True)
        self.listSortMode.lineEdit().setPlaceholderText('Sort mode')

        self.listSortMode.addItem('Récents')
        self.listSortMode.addItem('Favoris')
        self.listSortMode.addItem('All items')

        self.listSortMode.setCurrentIndex(self.parent.cmbSortIndex)
        self.listSortMode.currentIndexChanged.connect(self.evt_listSortMode_currentIndexChanged)
        lytTop.addWidget(self.listSortMode)
        #  *********************************************************
        # Recherche
        self.lneRecherche = QLineEdit()
        f = open('styles/QLineEdit.txt', 'r')
        style = f.read()
        styleQLineEdit = style
        self.lneRecherche.setStyleSheet(styleQLineEdit)
        self.lneRecherche.setFixedWidth(300)
        self.lneRecherche.setFixedHeight(32)
        self.lneRecherche.setPlaceholderText('Recherche dans le texte...')
        self.lneRecherche.setText(self.searchString)
        #  Boutons voir total
        self.btnVueItem = QPushButton(self.lneRecherche)
        self.btnVueItem.setIcon(QIcon('ressources/voirItem.png'))
        self.btnVueItem.setIconSize(QSize(28, 22))
        self.btnVueItem.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnVueItem.move(222, 4)
        self.btnVueItem.clicked.connect(self.evt_btnVueItem_clicked)
        self.btnVueItem.setStyleSheet('background-color: transparent; border: 1px solid #666666; border-radius: 5px')
        #  Boutons voir dossier
        self.btnDossierItem = QPushButton(self.lneRecherche)
        self.btnDossierItem.setIcon(QIcon('ressources/dossierItem.png'))
        self.btnDossierItem.setIconSize(QSize(28, 22))
        self.btnDossierItem.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnDossierItem.move(261, 4)
        self.btnDossierItem.clicked.connect(self.evt_btnVueItem_clicked)
        self.btnDossierItem.setStyleSheet('background-color: transparent; border: 1px solid #666666; border-radius: 5px')
        lytTop.addWidget(self.lneRecherche)
        self.btnLoupe = ButtonSwitch()
        self.btnLoupe.setText("")
        self.btnLoupe.setFixedSize(QSize(28, 28))
        self.btnLoupe.setIcon(QIcon('ressources/loupe.png'))
        lytTop.addWidget(self.btnLoupe)
        self.btnLoupe.setStyleSheet('background-color: #F05A24; border-radius: 4px;')

        #  *********************************************************
        #  Zone Bottom
        #  *********************************************************
        self.lytBottom = QHBoxLayout()
        lytMain.addLayout(self.lytBottom)
        #  *********************************************************
        #  Zone left (listes)
        self.grpLeft = QGroupBox()
        self.grpLeft.setFixedWidth(300)
        f = open('styles/grpLeft.txt', 'r')
        style = f.read()
        styleQGroupBox = style
        self.grpLeft.setStyleSheet(styleQGroupBox)
        self.lytBottom.addWidget(self.grpLeft)
        self.lytLeft = QVBoxLayout()
        self.lytLeftTop = QHBoxLayout()
        self.grpLeft.setLayout(self.lytLeft)
        self.lytLeft.addLayout(self.lytLeftTop)
        #  GroupBox
        self.grpLeftTop = QGroupBox()
        self.grpLeftTop.setFixedHeight(30)
        self.grpLeftTop.setFixedWidth(245)
        self.grpLeftTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grpLeftTop.setStyleSheet('background-color: #222222')
        self.lytLeftTop.addWidget(self.grpLeftTop)
        #  ComboBox
        self.listSelectItem = QComboBox(self.grpLeftTop)
        f = open('styles/QComboBox.txt', 'r')
        style = f.read()
        styleQComboBox = style
        self.listSelectItem.setStyleSheet(styleQComboBox)
        self.listSelectItem.setFixedWidth(240)
        self.listSelectItem.setFixedHeight(28)
        self.listSelectItem.setEditable(True)
        self.listSelectItem.lineEdit().setPlaceholderText('Select item')
        self.listSelectItem.move(2, 2)
        # #  populate
        self.listSelectItem.addItem('Labels')
        self.listSelectItem.addItem('Classeurs')
        self.listSelectItem.addItem('Arborescence')
        #
        self.listSelectItem.setCurrentIndex(-1)
        self.listSelectItem.currentIndexChanged.connect(self.evt_listSelectItem_currentIndexChanged)

        #  liste des items
        self.listItem = QListWidget()
        self.listItem.setFrameStyle(0)
        self.listItem.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.listItem.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.listItem.setFixedWidth(280)
        self.listItem.itemClicked.connect(self.evt_listItem_itemClicked)
        self.listItem.setSpacing(7)
        self.lytLeft.addWidget(self.listItem)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        self.listItem.setStyleSheet(styleQScrollBar)

        #  *********************************************************
        #  Zone right (vignettes)
        #  *********************************************************
        self.gridVignette = GridVignette()
        self.lytBottom.addWidget(self.gridVignette)

        boolMajLstVideo = True
        self.fillGridLayout1()

    def evt_listSortMode_currentIndexChanged(self):
        mainWindow.cmbSortIndex = self.listSortMode.currentIndex()

        self.setCursor(Qt.WaitCursor)
        query = QSqlQuery()
        # filtreSQL, listOnglet = mainWindow.filtreCour
        # print(filtreSQL)
        filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleBiblio={mainWindow.cleBiblio}'

        if mainWindow.cmbSortIndex == 0:  # récents
            query.exec(filtreSQL + f' ORDER BY dateLastView DESC LIMIT {mainWindow.NbVideosRecentes}')
        if mainWindow.cmbSortIndex == 1:  # favoris
            query.exec(filtreSQL + ' AND favori')
        if mainWindow.cmbSortIndex == 2:  # All items
            query.exec(filtreSQL)
        lstVideo = []
        while query.next():
            lstVideo.append(VideoFileRecord(query.value('cle')))

        mainWindow.displayGridWindow(lstVideo)
        self.unsetCursor()

    def evt_listItem_itemClicked(self):
        pass

    def evt_btnVueItem_clicked(self):
        lstItems = self.listItem.selectedItems()

    def resizeEvent(self, e):
        if not self._flag:
            self._flag = True
            self.setLabel()
            QTimer.singleShot(50, lambda: setattr(self, "_flag", False))
        for itm in self.lstVignette:
            itmVignette = itm[0]
            itmVignette.setFixedHeight(int(itmVignette.width() / 1.87))
            # itmTitre.setFixedWidth(int(itmVignette.width()))
        super().resizeEvent(e)

    def evt_listSelectItem_currentIndexChanged(self, index):
        self.listSelectItem.setCurrentIndex(index)
        if index == 0:
            self.populateLabels()
        if index == 1:
            self.populateClasseurs()
        if index == 2:
            self.populateArborescence()

    def populateLabels(self):
        try:
            self.navigfichiers.close()
        except:
            pass
        self.listItem.setVisible(True)
        self.listItem.clear()
        self.listItem.itemClicked.connect(self.onClicked)
        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab ORDER BY nom')
        while query.next():
            if query.value('color') is None:
                self.couleurCour = '#FFFFFF'
            else:
                if query.value('color') == '':
                    self.couleurCour = '#FFFFFF'
                else:
                    self.couleurCour = query.value('color')
                lbl = QLabel()
                lbl.setFixedSize(QSize(12, 12))
                lbl.setStyleSheet(f'background-color: {self.couleurCour}; border-radius: 6px')
                itemN = QListWidgetItem(self.listItem)
                itemN.setSizeHint(QSize(0, 40))
                itemN.setText(f"     {query.value('nom')}")
                itemN.setData(Qt.UserRole, query.value('cle'))
                itemN.setSizeHint(lbl.sizeHint())
                self.listItem.addItem(itemN)
                self.listItem.setItemWidget(itemN, lbl)

    def populateLabelsGrid(self, cleLabel):
        #  Effacer le GrpBox
        for itm in self.gridVignette.grpBox.findChildren(LabelIndex):
            itm.deleteLater()
        for itm in self.gridVignette.grpBox.findChildren(QLabel):
            itm.deleteLater()

        query = QSqlQuery()
        filtreSQL = f'SELECT cle FROM videoFileTab WHERE statut={cleLabel} AND cleBiblio={mainWindow.cleBiblio}'

        query.exec(filtreSQL)
        self.lstVideo = []
        while query.next():
            self.lstVideo.append(VideoFileRecord(query.value('cle')))

        mainWindow.displayGridWindow(self.lstVideo)
        self.listSelectItem.setCurrentIndex(0)
        listTempOnglet = []
        mainWindow.filtreCour = (filtreSQL, listTempOnglet)
        self.fillGridLayout1()

    def populateClasseursGrid(self, cleClasseur):
        #  Effacer le GrpBox
        for itm in self.gridVignette.grpBox.findChildren(LabelIndex):
            itm.deleteLater()
        for itm in self.gridVignette.grpBox.findChildren(QLabel):
            itm.deleteLater()

        query = QSqlQuery()
        filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleClasseur={cleClasseur} AND cleBiblio={mainWindow.cleBiblio}'

        query.exec(filtreSQL)
        self.lstVideo = []
        while query.next():
            self.lstVideo.append(VideoFileRecord(query.value('cle')))

        mainWindow.displayGridWindow(self.lstVideo)
        self.listSelectItem.setCurrentIndex(0)
        listTempOnglet = []
        mainWindow.filtreCour = (filtreSQL, listTempOnglet)
        self.fillGridLayout1()

    def onClicked(self, item):
        if self.listSelectItem.currentIndex() == 0: #Labels
            current_row = self.listItem.currentItem().data(Qt.UserRole)
            self.populateLabelsGrid(current_row)

        if self.listSelectItem.currentIndex() == 1: #Classeurs
            current_row = self.listItem.currentItem().data(Qt.UserRole)
            self.populateClasseursGrid(current_row)


    def populateClasseurs(self):
        try:
            self.navigfichiers.close()
        except:
            pass
        self.listItem.setVisible(True)
        self.listItem.clear()
        self.listItem.itemClicked.connect(self.onClicked)
        query = QSqlQuery()
        query.exec(f'SELECT * FROM classeurTab ORDER BY nom')
        while query.next():
            # labelClasseur = LabelClasseur(self, query.value('nom'), query.value('cle'))
            lbl = QLabel()
            lbl.setFixedSize(QSize(20, 17))
            lbl.setPixmap(QPixmap('ressources/dossier.png'))
            itemN = QListWidgetItem(self.listItem)
            itemN.setSizeHint(QSize(0, 20))
            itemN.setText(f'        {query.value("nom")}')
            itemN.setData(Qt.UserRole, query.value('cle'))
            self.listItem.addItem(itemN)
            self.listItem.setItemWidget(itemN, lbl)
        # mainWindow.showMaximized()
        # mainWindow.showNormal()

    def populateArborescence(self):
        self.listItem.close()
        # from Brouillon import NavigFichiers
        query = QSqlQuery()
        query.exec(f'SELECT path FROM biblioTab WHERE cle={mainWindow.cleBiblio}')
        if query.next():
            self.navigfichiers = NavigFichiers(query.value('path'))
            self.lytLeft.addWidget(self.navigfichiers)

    def initUI(self):
        lytMain = QVBoxLayout()
        lytTitre = QHBoxLayout()
        lytMain.addLayout(lytTitre)
        lytCentral = QHBoxLayout()
        lytMain.addLayout(lytCentral)

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([150, 600])

        lytCentral.addWidget(splitter)

        self.setLayout(lytMain)
        self.setGeometry(100, 60, 1513, 663)
        self.show()

        #  ***************************************************************************
        #  Cadre Titre
        #  ***************************************************************************
        #  Bouton Reset
        self.btnReset = QPushButton('Reset')
        lytTitre.addWidget(self.btnReset)
        self.btnReset.setFixedSize(QSize(140, 35))
        self.btnReset.setIcon(QIcon('ressources/btnReset.png'))
        self.btnReset.setIconSize(QSize(45, 30))
        self.btnReset.setStyleSheet("QPushButton { text-align: left; background-color: transparent; "
                                    "margin-left: 8px}"
                                    "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        #  Bouton Selectionner
        self.btnSelect = QPushButton('Sélectionner')
        lytTitre.addWidget(self.btnSelect)
        self.btnSelect.setFixedSize(QSize(140, 35))
        self.btnSelect.setIcon(QIcon('ressources/btnSelect.png'))
        self.btnSelect.setIconSize(QSize(45, 30))
        self.btnSelect.setStyleSheet("QPushButton { text-align: left; background-color: transparent; "
                                     "margin-left: 8px}"
                                     "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lytTitre.addItem(spacerItem)

        self.frmPrecSuiv = FrmPrecSuiv(self)
        lytTitre.addWidget(self.frmPrecSuiv)

        self.lneRecherche = QLineEdit()
        self.lneRecherche.setFixedWidth(300)
        self.lneRecherche.setPlaceholderText('Recherche dans le texte...')
        self.lneRecherche.setText(self.searchString)
        lytTitre.addWidget(self.lneRecherche)
        self.btnLoupe = ButtonSwitch()
        self.btnLoupe.setText("")
        self.btnLoupe.setFixedSize(QSize(34, 32))
        self.btnLoupe.setIcon(QIcon('ressources/loupe.png'))
        lytTitre.addWidget(self.btnLoupe)
        self.btnLoupe.setStyleSheet('background-color: #F05A24')
        #  Signal Handlers ***********************************************************
        self.btnLoupe.clicked.connect(self.evt_btnLoupe_clicked)

        #  ***************************************************************************
        #  Cadre liste
        #  ***************************************************************************
        self.lytListe = QVBoxLayout(left)
        self.listeButtonGroup = []
        #  Bouton All Items
        self.btnAllItems = ButtonGroup(0, False)
        self.lytListe.addWidget(self.btnAllItems)

        self.btnAllItems.setText('  All Items')
        self.btnAllItems.setFixedSize(QSize(140, 35))
        self.btnAllItems.setIcon(QIcon('ressources/allItems.png'))
        self.btnAllItems.setIconSize(QSize(45, 30))
        self.btnAllItems.setStyleSheet("QPushButton { text-align: left; background-color: transparent; "
                                       "margin-left: 8px}"
                                       "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        self.listeButtonGroup.append(self.btnAllItems)
        self.btnAllItems.clicked.connect(partial(self.evt_btnGroup_clicked, '0'))
        self.btnAllItems.setMaximumWidth(2000)

        #  Bouton Recents
        self.btnRecents = ButtonGroup(1, False)
        self.lytListe.addWidget(self.btnRecents)
        self.btnRecents.setText('  Recents')
        self.btnRecents.setFixedSize(QSize(140, 35))
        self.btnRecents.setIcon(QIcon('ressources/recents.png'))
        self.btnRecents.setIconSize(QSize(45, 30))
        self.btnRecents.setStyleSheet("QPushButton { text-align: left; background-color : transparent; "
                                      "margin-left: 8px} "
                                      "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        self.listeButtonGroup.append(self.btnRecents)
        self.btnRecents.clicked.connect(partial(self.evt_btnGroup_clicked, '1'))
        self.btnRecents.setMaximumWidth(2000)
        self.btnRecents.etat = True
        self.btnRecents.initEtat()

        #  Bouton Delete
        self.btnDeleteItems = ButtonGroup(2, False)
        self.lytListe.addWidget(self.btnDeleteItems)
        self.btnDeleteItems.setText('  Deleted Items')
        self.btnDeleteItems.setFixedSize(QSize(140, 35))
        self.btnDeleteItems.setIcon(QIcon('ressources/deletedItems.png'))
        self.btnDeleteItems.setIconSize(QSize(45, 30))
        self.btnDeleteItems.setStyleSheet("QPushButton { text-align: left; background-color : transparent; "
                                          "margin-left: 8px}"
                                          "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        self.listeButtonGroup.append(self.btnDeleteItems)
        self.btnDeleteItems.clicked.connect(partial(self.evt_btnGroup_clicked, '2'))
        self.btnDeleteItems.setMaximumWidth(2000)
        self.majButtonGroupEtat()

        #  Bouton Favori
        self.btnFavoriItems = ButtonGroup(3, False)
        self.lytListe.addWidget(self.btnFavoriItems)
        self.btnFavoriItems.setText('  Vidéos favorites')
        self.btnFavoriItems.setFixedSize(QSize(140, 35))
        self.btnFavoriItems.setIcon(QIcon('ressources/favoriBtn.png'))
        self.btnFavoriItems.setIconSize(QSize(45, 30))
        self.btnFavoriItems.setStyleSheet("QPushButton { text-align: left; background-color : transparent; "
                                          "margin-left: 8px}"
                                          "QPushButton:hover {background-color: #54687A; color: #E0E1E3;}")
        self.listeButtonGroup.append(self.btnFavoriItems)
        self.btnFavoriItems.clicked.connect(partial(self.evt_btnGroup_clicked, '3'))
        self.btnFavoriItems.setMaximumWidth(2000)
        self.majButtonGroupEtat()

        #  Liste des pastiles de statut
        self.buildListePastille()

        listClasseur = []
        self.cadreListClasseur = CadreListClasseur(self, listClasseur)
        self.lytListe.addWidget(self.cadreListClasseur)


        #  Signal Handlers ***********************************************************
        # self.lstClasseur.clicked.connect(self.evt_lstClasseur_clicked)
        self.btnSelect.clicked.connect(self.fillGridLayout)
        self.btnReset.clicked.connect(self.evt_btnReset_clicked)

        #  ***************************************************************************
        #  cadre grille
        #  ***************************************************************************
        self.lytGrille = QGridLayout(right)
        #  ***************************************************************************

        #  ***************************************************************************
        #  recupération des vidéos affichées dans le Grid
        #  ***************************************************************************
        if mainWindow.btnGroupCour != -1:
            index = mainWindow.btnGroupCour
            bouton = None
            for btn in self.listeButtonGroup:
                if btn.indexButton == index:
                    btn.etat = True
                    bouton = btn
                    self.btnCour = index
                else:
                    btn.etat = False
                btn.initEtat()
            bouton.setCursor(QCursor(Qt.WaitCursor))

            bouton.setCursor(QCursor(Qt.PointingHandCursor))
        self.fillGridLayout()

    #  Slot Handlers *****************************************************
    def evt_btnReset_clicked(self):
        return
        self.lstVideo = []
        #  3 boutons AllItems, etc
        for itm in self.listeButtonGroup:
            itm.etat = False
            itm.initEtat()
        #  Bouton favori
        self.btnFavoriItems.etat = False
        self.btnFavoriItems.initEtat()
        #  Pastilles statut
        self.cadreListStatut.initCadrePastille()
        self.cadreListStatut.clePastilleCour = -1
        #  Classeurds
        self.cadreListClasseur.initCadreClasseur()
        self.cadreListClasseur.cleClasseurCour = -1
        #  recherche mot
        self.listCherche = []

        for i in reversed(range(self.lytGrille.count())):
            self.lytGrille.itemAt(i).widget().setParent(None)

    def evt_cmbStatut_clicked(self, index):
        self.cmbStatut.setCurrentIndex(index)
        self.statutCour = self.cmbStatut.currentData()
        self.cmbStatut.setCursor(QCursor(Qt.WaitCursor))

        # if index == 0:  # all items
        self.btnAllItems.setEnabled(True)
        self.btnAllItems.etat = False
        self.btnAllItems.initEtat()

        self.fillGridLayout()
        self.cmbStatut.setCursor(QCursor(Qt.PointingHandCursor))

    def evt_btnGroup_clicked(self, buttonName):
        bouton = None
        index = int(buttonName)
        if index == 3:
            if self.btnFavoriItems.etat:
                self.btnFavoriItems.etat = False
            else:
                self.btnFavoriItems.etat = True
            self.btnFavoriItems.initEtat()
            bouton = self.btnFavoriItems
        else:
            for btn in self.listeButtonGroup[:-1]:
                if btn.indexButton == index:
                    btn.etat = True
                    bouton = btn
                    self.btnCour = index
                else:
                    btn.etat = False
                btn.initEtat()

        bouton.setCursor(QCursor(Qt.WaitCursor))
        mainWindow.btnGroupCour = index  #
        # self.lneRecherche.setText('')
        # self.boolSearch = False
        # self.fillGridLayout()
        bouton.setCursor(QCursor(Qt.PointingHandCursor))

    def majButtonGroupEtat(self):
        for btn in self.listeButtonGroup:
            if btn.etat:
                btn.setStyleSheet("text-align: left; border: 2px solid orange; background-color: transparent; "
                                  "margin-left: 8px")

    def evt_btnLoupe_clicked(self):
        if self.lneRecherche.text() == "":
            self.boolSearch = False
            return
        self.boolSearch = True

        # for i in range(0, 50):
        txtCherche = self.majusculeSansAccent(self.lneRecherche.text())
        self.searchString = txtCherche
        mainWindow.searchString = txtCherche
        mainWindow.boolSearch = True
        query = QSqlQuery()
        bOk = query.exec(f'SELECT cleVideo, texte, cleBiblio FROM paragraph, videoFileTab '
                         f'WHERE clevideo=videoFileTab.cle AND cleBiblio={mainWindow.cleBiblio}')
        listCherche = []
        while query.next():
            txt = query.value('texte')
            txt = txt.replace('$$', ' ')
            txt = txt.replace(')|', ' ')
            texte = txt.replace('µµ', ' ')
            texte = self.majusculeSansAccent(texte)
            if txtCherche in texte:
                listCherche.append(query.value('cleVideo'))
        listCherche = set(listCherche)
        listCherche = list(listCherche)
        self.listCherche = listCherche

        self.fillGridLayout()

        # for i in reversed(range(self.lytGrille.count())):
        #     self.lytGrille.itemAt(i).widget().setParent(None)

    def evt_lstClasseur_clicked(self):
        self.lneRecherche.setText('')
        itm = self.lstClasseur.currentItem()
        indexCour = itm.data(Qt.UserRole)
        self.classeurCour = indexCour
        listAux = [aux for aux in self.lstVideo if aux.cleClasseur == indexCour]
        self.frmPrecSuiv.initDataTab(listAux)

    #  Méthodes ** *****************************************************

    def buildListePastille(self):
        try:
            self.cadreListStatut.close()
        except:
            self.cadreListStatut = CadreListStatut(self)
            self.lytListe.addWidget(self.cadreListStatut)

    def majusculeSansAccent(self, chaine):
        txt = chaine.upper()
        chnorm = normalize('NFKD', txt)
        return "".join([c for c in chnorm if not combining(c)])

    def majCadreListe(self):
        #  Construire la liste des classeurs
        self.lstClasseur.clear()
        listClasseur = [(aux.cleClasseur, aux.nomClasseur) for aux in self.lstVideo]
        listClasseur = set(listClasseur)
        listClasseur = list(listClasseur)
        listClasseur.sort(key=self.listSortKeyClasseurs)

        # self.lstClasseur.setIconSize(QSize(22, 23))
        for record in listClasseur:
            if record[1] != '':
                record = list(record)

                itm = QListWidgetItem()
                itm.setSizeHint(QSize(211, 45))
                lbl = QLabel()
                lbl.setStyleSheet('background-color: gray; padding: 0px')
                lbl1 = QLabel(lbl)
                lbl1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                lbl1.setFixedSize(QSize(45, 45))
                lbl1.setStyleSheet('background-color: orange')
                lbl1.setPixmap(QPixmap('ressources/classeurs26.png'))
                lbl2 = QLabel(record[1])
                lbl2.setAlignment(Qt.AlignLeft)
                lbl2.setStyleSheet('background-color: green')
                lbl1.setFixedSize(QSize(140, 40))
                lytClasseur = QHBoxLayout()
                lbl.setLayout(lytClasseur)
                lytClasseur.addWidget(lbl1)
                lytClasseur.addWidget(lbl2)
                spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
                lytClasseur.addItem(spacerItem)

                # lbl.setFixedSize(QSize(111, 35))

                # itm.setIcon(QIcon('ressources/classeurs26.png'))
                # itm.setData(Qt.UserRole, record[0])

                self.lstClasseur.addItem(itm)
                self.lstClasseur.setItemWidget(itm, lbl)
        self.lstClasseur.setCursor(QCursor(Qt.PointingHandCursor))

    def listSortKeyClasseurs(self, element):
        return element[1]

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

        duree = f'{heureTxt}:{minuteTxt}:{secondeTxt}'
        return duration

    def fillGridLayout1(self):
        self.setCursor(Qt.WaitCursor)
        self.gridVignette.populateGrpBox(self.lstVideo)
        self.unsetCursor()

    def fillGridLayout(self):
        #  Liste totale
        self.setCursor(Qt.WaitCursor)
        nbCases = 5 * self.nbRowGrid

        self.majLstVideo()

        return

        listeTotale = self.lstVideo

        #  Effacer le gridLayout
        for i in reversed(range(self.lytGrille.count())):
            self.lytGrille.itemAt(i).widget().setParent(None)

        self.frmPrecSuiv.initDataTab(listeTotale)

        i = 0
        j = 0
        lenListTotal = len(listeTotale)
        nbPages = lenListTotal // nbCases
        if lenListTotal % nbCases > 0:
            nbPages += 1

        pageCour = 0
        if nbPages > 1:
            self.frmPrecSuiv.setVisible(True)
            pageCour = self.frmPrecSuiv.pageCour
            self.frmPrecSuiv.initPages(pageCour, nbPages)
        else:
            self.frmPrecSuiv.setVisible(False)
            pageCour = 1
            self.frmPrecSuiv.initPages(pageCour, nbPages)

        #  Extraire les données de la liste correspondant à la pageCour
        listAux = []
        debut = 0
        nbRec = 0
        if pageCour < nbPages:
            debut = nbCases * (pageCour - 1)
            nbRec = nbCases
        if pageCour == nbPages:
            debut = nbCases * (pageCour - 1)
            nbRec = lenListTotal - nbCases * (pageCour - 1)

        for x in range(debut, nbRec + debut):
            listAux.append(listeTotale[x])

        lenListAux = len(listAux)
        index = 0
        fini = False
        listeOnglet = [cleVideo for cleVideo in mainWindow.lstOngletVideo]
        while not fini:
            if index + 1 <= lenListAux:
                ligne = 2 * j
                if listAux[index].boolTag:
                    titreAux = '......'
                    lblVignette1 = LabelIndex(self)
                    lblVignette1.setStyleSheet('border-radius: 4px; border: 1px solid gray')
                    lblVignette1.setFixedSize(192, 107)
                    lblVignette1.setCursor(QCursor(Qt.PointingHandCursor))
                    self.lytGrille.addWidget(lblVignette1, ligne, i)
                    lblVignette1.index = listAux[index].cle
                    videoCleTest = listAux[index].cle
                    query1 = QSqlQuery()
                    #  Mise en place du eventFilter pour le menu contextuel
                    lblVignette1.installEventFilter(self)
                    #  Cas où une icon a été définie pour la vidéo dans paragraph
                    bOk = query1.exec(f'SELECT * FROM paragraph WHERE cleVideo = {videoCleTest} AND icone = True')

                    if query1.next():
                        timeNote = query1.value('timeNote')
                        vidcap = cv2.VideoCapture(self.parent.racine + listAux[index].internalPath
                                                  + listAux[index].videoName)
                        vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
                        success, image = vidcap.read()
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        if success:
                            image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                            pixmap01 = QPixmap.fromImage(image)
                            lblVignette1.setPixmap(pixmap01.scaled(192, 107, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                    query12 = QSqlQuery()
                    bOk = query12.exec(f'SELECT * FROM paragraph WHERE cleVideo={videoCleTest} AND titre=True '
                                       f'AND timeNote=0')
                    if query12.next():
                        titreAux = query12.value('texte')
                        titreAux = titreAux.replace('$$', chr(10))
                    #  Titre de la video
                    # toto = str(listAux[index].cle)
                    lblTitre1 = QLabel(titreAux)
                    lblTitre1.setWordWrap(True)
                    lblTitre1.setFixedSize(192, 30)
                    self.lytGrille.addWidget(lblTitre1, ligne + 1, i)
                    if videoCleTest in listeOnglet:
                        lblVignette1.cocherPlayCursor(True)
                    index += 1
                else:
                    # i -= 1
                    # if i == -1:
                    #     i = self.nbRowGrid
                    #     j -= 1
                    lblVignette1 = LabelIndex(self)
                    lblVignette1.index = listAux[index].cle
                    lblVignette1.installEventFilter(self)
                    lblVignette1.setStyleSheet('border-radius: 4px; border: 2px solid red; background-color: black')
                    lblVignette1.setFixedSize(192, 107)
                    lblVignette1.setPixmap(QPixmap('ressources/newVideo.png').scaled(96, 53, Qt.KeepAspectRatio,
                                                                                     Qt.SmoothTransformation))
                    lblVignette1.setAlignment(Qt.AlignCenter)
                    lblVignette1.setCursor(QCursor(Qt.PointingHandCursor))
                    self.lytGrille.addWidget(lblVignette1, ligne, i)
                    lblTitre1 = QLabel(listAux[index].videoName)
                    lblTitre1.setWordWrap(True)
                    lblTitre1.setFixedSize(192, 30)
                    self.lytGrille.addWidget(lblTitre1, ligne + 1, i)
                    index += 1
            else:

                ligne = 2 * j
                lblVignette1 = LabelIndex(self)
                lblVignette1.index = -1  # la vidéo n'est pas encore enregistrée dans la base

                lblVignette1.setStyleSheet('border-radius: 4px; border: 1px solid gray')
                lblVignette1.setFixedSize(192, 107)
                self.lytGrille.addWidget(lblVignette1, ligne, i)

            #  Création de vignettes vides pour finir de remplir le QGridFormLayout (les 20cases)
            i += 1
            if i == 5:
                i = 0
                j += 1
                if j == self.nbRowGrid:
                    fini = True
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # if len(self.lstOngletVideo) == 0:
        #     mainWindow.actEtudeVideo.setIcon(QIcon('ressources/etudeVideoGris.png'))
        #     mainWindow.actEtudeVideo.setEnabled(False)
        # else:
        #     mainWindow.actEtudeVideo.setIcon(QIcon('ressources/etudeVideoBleu.png'))
        #     mainWindow.actEtudeVideo.setEnabled(True)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            self.sourceCour = source
            menu = QMenu()
            menu.addAction('Mode édition', self.editVideo)
            menu.addSeparator()
            menu.addAction('Mode étude', self.etudeVideo)
            menu.addSeparator()
            if source.boolOnglet:
                menu.addAction('Voir les vidéos', mainWindow.evt_actEtudeVideo_clicked)
            # else:
            #     menu.addAction('Voir les vidéos', self.ajouterOnglet)
            if menu.exec_(event.globalPos()):
                return True
        return super().eventFilter(source, event)

    def editVideo(self):
        try:
            self.formListVideo.close()
        except:
            pass
        # self.formListVideo = FormListVideo(self, lien=False, videoCour=self.gridVignette.sourceCour.index)
        self.formEditionVideo = FormEditionVideo(self.gridVignette.sourceCour.index)
        self.formEditionVideo.show()

    def etudeVideo(self):
        # self.ajouterOnglet()
        self.sourceCour.modeEtude()

    def ajouterOnglet(self):
        cleVideo = self.sourceCour.index
        aux = [item for item in self.lstVideo if item.cle == cleVideo][0]
        index = self.lstVideo.index(aux)
        if self.sourceCour.lbl.isVisible():
            self.sourceCour.cocherPlayCursor(False)
            self.lstVideo[index].ongletVideo = False
            index1 = mainWindow.lstOngletVideo.index(cleVideo)
            del mainWindow.lstOngletVideo[index1]
        else:
            self.sourceCour.cocherPlayCursor(True)
            self.lstVideo[index].ongletVideo = True
            mainWindow.lstOngletVideo.append(cleVideo)
        if len(mainWindow.lstOngletVideo) == 0:

            mainWindow.actEtudeVideo.setIcon(QIcon('ressources/etudeVideoGris.png'))
            mainWindow.actEtudeVideoAnnul.setIcon(QIcon('ressources/etudeVideoGrisAnnul.png'))
            mainWindow.actEtudeVideo.setEnabled(False)
            mainWindow.actEtudeVideoAnnul.setEnabled(False)
        else:
            mainWindow.actEtudeVideo.setIcon(QIcon('ressources/etudeVideoBleu.png'))
            mainWindow.actEtudeVideoAnnul.setIcon(QIcon('ressources/etudeVideoBleuAnnul.png'))
            mainWindow.actEtudeVideo.setEnabled(True)
            mainWindow.actEtudeVideoAnnul.setEnabled(True)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              M A I N S T A T U T          ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainStatut(QDialog):
    def __init__(self, parent, cleVideo):
        super(MainStatut, self).__init__()
        self.parent = parent
        self.cleVideo = cleVideo
        self.resize(QSize(500, 400))
        # self.show()
        # self.exec_()

        #  Layout principal
        lytMain = QVBoxLayout()
        self.setLayout(lytMain)
        #  Layout haut
        lytTop = QHBoxLayout()
        lytMain.addLayout(lytTop)
        #  Layout Liste
        lytListe = QHBoxLayout()
        lytTop.addLayout(lytListe)
        lstStatut = QListWidget()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************       T A B  W I D G E T  D R A G  R O W S       ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class TableWidgetDragRows(QTableWidget):
    signalFini = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)
            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index
                             in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)
        self.signalFini.emit('fini')

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()
        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) \
               and pos.y() >= rect.center().y()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           L A B E L C L A S S E U R           *******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelClasseur(QLabel):
    def __init__(self, parent=None, nom='', cleClasseur=None):
        QLabel.__init__(self)
        self.parent = parent
        self.nom = nom
        self.etat = False
        self.initEtat()
        self.cleClasseur = cleClasseur
        self.setFixedHeight(80)

    def paintEvent(self, e):
        #  image classeur
        painter = QPainter(self)
        point = QPoint(10, 0)
        image = QImage('ressources/dossier.png')
        painter.drawImage(point, image)
        #  nom classeur
        pen = QPen(Qt.white)
        painter.setPen(pen)
        painter.drawText(55, 14, self.nom)
        return

    def mousePressEvent(self, event):
        return
        if self.etat:
            self.parent.initCadreClasseur()
            self.etat = False
            self.initEtat()
            self.parent.cleClasseurCour = -1
        else:
            self.parent.initCadreClasseur()
            self.etat = True
            self.initEtat()
            self.parent.cleClasseurCour = self.cleClasseur

    def initEtat(self):
        if self.etat:
            self.setStyleSheet("text-align: left; border: 2px solid orange; background-color: transparent; "
                               "margin-left: 8px; border-radius: 4px")
        else:
            self.setStyleSheet("text-align: left; border: 0px solid orange; background-color: transparent; "
                               "margin-left: 8px")


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           L A B E L P A S T I L L E           *******************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelPastille(QLabel):
    def __init__(self, parent=None, color='#FFFFFF', nom='', clePastille=None):
        QLabel.__init__(self)
        self.parent = parent
        self.color = color
        self.nom = nom
        self.etat = False
        self.initEtat()
        self.clePastille = clePastille
        self.setFixedHeight(25)
        self.colorPen = 'gray'

    def setPosition(self, x, y):
        self.move(x, y)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(QColor(self.color))
        painter.setPen(pen)
        painter.setBrush(QColor(self.color))
        painter.setRenderHints(QPainter.Antialiasing)
        painter.drawEllipse(5, 5, 15, 15)
        pen = QPen(QColor(self.colorPen))
        painter.setPen(pen)
        painter.setBrush(Qt.white)
        painter.drawText(55, 16, self.nom)
        return

    def mousePressEvent(self, event):
        return
        if self.etat:
            self.etat = False
            self.colorPen = 'gray'
            self.parent.clePastilleCour = -1
        else:
            self.etat = True
            self.colorPen = 'white'
            self.parent.clePastilleCour = -1
            # self.parent.initCadrePastille()
            # self.etat = True
            # self.initEtat()
            # self.parent.clePastilleCour = self.clePastille
        self.paintEvent(event)

    def initEtat(self):
        if self.etat:
            self.setStyleSheet("text-align: left; border: 2px solid orange; background-color: transparent; "
                               "margin-left: 8px; border-radius: 4px")
        else:
            self.setStyleSheet("text-align: left; border: 0px solid orange; background-color: transparent; "
                               "margin-left: 8px")


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           C A D R E L I S T C L A S S E U R       ***************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class CadreListClasseur(QMainWindow):
    def __init__(self, parent=None, listClasseur=None):
        super(CadreListClasseur, self).__init__()
        self.parent = parent
        self.setFixedSize(QSize(250, 200))
        self.listeClasseur = listClasseur
        self.listeLabelClasseur = []
        self.cleClasseurCour = -1

        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        self.populateCadreListClasseur()

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)
        vsb = self.scrollArea.verticalScrollBar()

    def listSortKeyClasseurs(self, element):
        return element[1]

    def populateCadreListClasseur(self):
        query = QSqlQuery()
        query.exec(f'SELECT cle FROM videoFileTab')
        lstVideo = []
        while query.next():
            videoFileRecord = VideoFileRecord(query.value('cle'))
            lstVideo.append(videoFileRecord)

        listClasseur = [(aux.cleClasseur, aux.nomClasseur) for aux in lstVideo]
        listClasseur = set(listClasseur)
        listClasseur = list(listClasseur)
        listClasseur.sort(key=self.listSortKeyClasseurs)

        for classeur in listClasseur:
            classeur = list(classeur)
            labelClasseur = LabelClasseur(self, classeur[1], classeur[0])
            self.vbox.addWidget(labelClasseur)
            self.listeLabelClasseur.append(labelClasseur)

    def initCadreClasseur(self):
        for wid in self.listeLabelClasseur:
            wid.etat = False
            wid.initEtat()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           C A D R E L I S T S T A T U T           ***************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class CadreListStatut(QMainWindow):
    def __init__(self, parent=None):
        super(CadreListStatut, self).__init__()
        self.parent = parent
        self.setFixedWidth(250)
        self.setFixedHeight(200)
        self.couleurCour = '#FFFFFF'
        self.listPastille = []
        self.clePastilleCour = -1

        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        self.populateCadrePastille()

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)
        vsb = self.scrollArea.verticalScrollBar()

    def populateCadrePastille(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)

        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab ORDER by nom')
        while query.next():
            if query.value('color') is None:
                self.couleurCour = '#FFFFFF'
            else:
                if query.value('color') == '':
                    self.couleurCour = '#FFFFFF'
                else:
                    self.couleurCour = query.value('color')
            labelPastille = LabelPastille(self, self.couleurCour, query.value('nom'), query.value('cle'))
            self.vbox.addWidget(labelPastille)
            # self.listPastille.clicked.connect(self.evt_listePastille_clicked)
            self.listPastille.append(labelPastille)

    def initCadrePastille(self):
        for wid in self.listPastille:
            wid.etat = False
            wid.initEtat()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           F O R M _ S T A T U T           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormStatut(QDialog, DialogStatut):
    def __init__(self, parent):
        super(FormStatut, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.btSupprimer.setVisible(False)
        self.btnSauver.setVisible(False)
        self.btnNouveau.setEnabled(True)
        self.statutCreer = False
        self.lneNom.setVisible(False)
        self.chkDefaut.setVisible(False)
        self.lblCouleur.setVisible(False)
        self.colorCour = ''
        self.boolMiseAJour = False

        self.btnFermer.clicked.connect(self.evt_btnFermer_clicked)
        self.btnSauver.clicked.connect(self.evt_btnSauver_clicked)
        self.btnNouveau.clicked.connect(self.evt_btnNouveau_clicked)
        self.btSupprimer.clicked.connect(self.evt_btSupprimer_clicked)
        self.btnAnnuler.clicked.connect(self.evt_btnAnnuler_clicked)
        self.lstStatut.clicked.connect(self.evt_lstStatut_clicked)
        self.lblCouleur.mousePressEvent = self.evt_lblCouleur_mousePress

        self.populateLstStatut()

    def evt_btnFermer_clicked(self):
        if self.boolMiseAJour:
            self.parent.lstClasseurPopulate()
        self.close()

    def evt_btnAnnuler_clicked(self):
        self.lneNom.setText('')
        self.chkDefaut.setChecked(False)
        self.statutCreer = False
        self.statutCour = -1
        self.colorCour = '#FFFFFF'
        self.lneNom.setVisible(False)
        self.chkDefaut.setVisible(False)
        self.btnSauver.setVisible(False)
        self.btSupprimer.setVisible(False)
        self.lblCouleur.setVisible(False)
        self.btnNouveau.setVisible(True)
        if self.boolMiseAJour:
            self.parent.populateListStatut()
            self.close()

    def evt_lblCouleur_mousePress(self, e):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorCour = color.name()
            self.lblCouleur.setStyleSheet(f'border: 1px solid #FFFFFF; background-color: {self.colorCour}')

    def evt_btnNouveau_clicked(self):
        #  Effacer la fiche
        self.lneNom.setText('')
        self.chkDefaut.setChecked(False)
        self.statutCreer = True
        self.statutCour = -1
        self.colorCour = '#FFFFFF'
        self.lblCouleur.setStyleSheet(f'border: 1px solid #FFFFFF; background-color: {self.colorCour}')
        self.lneNom.setVisible(True)
        self.chkDefaut.setVisible(True)
        self.btnSauver.setVisible(True)
        self.btSupprimer.setVisible(False)
        self.lblCouleur.setVisible(True)

    def evt_btSupprimer_clicked(self):
        if self.chkDefaut.isChecked():
            QMessageBox.information(self, 'Suppression impossible', 'Choisir un autre statut par défaut\n'
                                                                    'pour supprimer le statut courant.')
        else:
            rep = QMessageBox.question(self, 'Supprimer ce staut', 'Confirmez-vous la suppression?')
            if rep == QMessageBox.Yes:
                query = QSqlQuery()
                bOk = query.exec(f'DELETE FROM statutTab WHERE cle={self.statutCour}')
                self.populateLstStatut()
                self.btnSauver.setVisible(False)
                self.btSupprimer.setVisible(False)
                self.btnNouveau.setVisible(True)
                self.lblCouleur.setVisible(False)
                self.lneNom.setVisible(False)
                self.lneNom.setText('')
                self.chkDefaut.setVisible(False)

    def evt_btnSauver_clicked(self):
        if self.lneNom == '':
            QMessageBox.information(self, 'Enregistrement impossible', 'Veuillez saisir le nom')
        #  ***********************************************************************
        #  Modification d'un statut existant
        #  ***********************************************************************
        if not self.statutCreer:
            #  *****  Modification d'un statut existant  *****
            #  1 - vérification de l'existence d'un statut par défaut
            #  1 - 1 Si le statut courant est par défaut, vérifier qu'il n'y en a pas d'autres dans la table
            if self.chkDefaut.isChecked():
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut={True}')
                if query.next():
                    #  On retire l'attribut déf aaut existant
                    tplChamps = ('nom', 'defaut', 'color')
                    tplData = (query.value('nom'), False, self.colorCour)
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {query.value("cle")}')
                    #  Sauvegarde du statut par défaut
                    tplData = (self.lneNom.text(), True, self.colorCour)
                    tplChamps = ('nom', 'defaut', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {self.statutCour}')
                    self.populateLstStatut()
                    self.chkDefaut.setChecked(True)
                else:
                    tplChamps = (self.lneNom.text(), True, self.colorCour)
                    tplData = ('nom', 'defaut', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {self.statutCour}')
                    self.populateListStatut()
                    self.chkDefaut.setChecked(True)
            #  1 - 2 Si le statut courant n'est pas par défaut, vérifier qu'il n'y en a pas d'autres dans la table
            else:
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut={True}')
                if query.next():
                    tplData = (self.lneNom.text(), False, self.colorCour)
                    tplChamps = ('nom', 'defaut', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {self.statutCour}')
                    self.populateLstStatut()
                else:
                    tplData = (self.lneNom.text(), True, self.colorCour)
                    tplChamps = ('nom', 'defaut', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {self.statutCour}')
                    self.populateLstStatut()
                    self.chkDefaut.setChecked(True)
        #  ***********************************************************************
        #  Création d'un nouveau statut
        #  ***********************************************************************.
        else:
            #  Recherche de l'index suivant
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM statutTab')
            if query.next():
                try:
                    cleMax = int(query.value('cleMax')) + 1
                except:
                    cleMax = 1

            if self.chkDefaut.isChecked():
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut={True}')
                if query.next():
                    #  On retire l'attribut déf aaut existant
                    tplChamps = ('nom', 'defaut', 'color')
                    tplData = (query.value('nom'), False, self.colorCour)
                    query1 = QSqlQuery()
                    query1.exec(f'UPDATE statutTab SET {tplChamps} = {tplData} WHERE cle = {query.value("cle")}')
                    #  Sauvegarde du statut par défaut
                    tplData = (self.lineEdit.text(), True, cleMax, self.colorCour)
                    tplChamps = ('nom', 'defaut', 'cle', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'INSERT INTO statutTab {tplChamps} VALUES {tplData}')
                    self.populateListStatut()
                    self.chkDefaut.setChecked(True)
                    self.populateListStatut()
                    self.chkDefaut.setChecked(True)
                else:
                    tplData = (self.lineEdit.text(), True, cleMax, self.colorCour)
                    tplChamps = ('nom', 'defaut', 'cle', 'color')
                    query1 = QSqlQuery()
                    query1.exec(f'INSERT INTO statutTab {tplChamps} VALUES {tplData}')
                    self.populateListStatut()
                    self.chkDefaut.setChecked(True)
                    self.populateListStatut()
                    self.chkDefaut.setChecked(True)
            else:
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut={True}')
                checkAux = True
                if query.next():
                    checkAux = False  # un statut par défaut existe déja

                tplData = (self.lneNom.text(), checkAux, cleMax, self.colorCour)
                tplChamps = ('nom', 'defaut', 'cle', 'color')
                query1 = QSqlQuery()
                query1.exec(f'INSERT INTO statutTab {tplChamps} VALUES {tplData}')
                self.populateLstStatut()
                self.chkDefaut.setChecked(True)
                self.populateLstStatut()
                self.chkDefaut.setChecked(True)
        self.btnSauver.setVisible(False)
        self.btSupprimer.setVisible(False)
        self.btnNouveau.setVisible(True)
        self.lblCouleur.setVisible(False)
        self.lneNom.setText('')
        self.lneNom.setVisible(False)
        self.chkDefaut.setChecked(False)
        self.chkDefaut.setVisible(False)
        self.colorCour = ''

        if mainWindow.gridWindow:
            mainWindow.gridWindow.cadreListStatut.populateCadrePastille()

        if self.boolMiseAJour:
            self.parent.populateListStatut()
            self.close()


    def evt_lstStatut_clicked(self):
        itm = self.lstStatut.currentItem()
        self.statutCour = list(itm.data(Qt.UserRole))[0]
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM statutTab WHERE  cle = {self.statutCour}')
        if query.next():
            self.lneNom.setVisible(True)
            self.lblCouleur.setVisible(True)
            self.chkDefaut.setVisible(True)
            self.lblCouleur.setVisible(True)
            self.lneNom.setText(query.value('nom'))
            self.colorCour = ''
            if query.value('color') is not None:
                self.colorCour = query.value('color')
            if self.colorCour != '':
                self.lblCouleur.setStyleSheet(f'border: 1px solid #FFFFFF; background-color: {self.colorCour}')
            else:
                self.lblCouleur.setStyleSheet(f'border: 1px solid #FFFFFF; background-color: #FFFFFF')
            self.btnSauver.setEnabled(True)
            self.statutCreer = False
            self.btSupprimer.setEnabled(True)
            self.chkDefaut.setChecked(bool(query.value('defaut')))
        self.btnNouveau.setVisible(False)
        self.btnSauver.setVisible(True)
        self.btSupprimer.setVisible(True)

    def populateLstStatut(self):
        self.lstStatut.clear()
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM StatutTab ORDER BY nom')
        while query.next():
            lwi = QListWidgetItem(query.value('nom'))
            if query.value('defaut') == 1:
                lwi.setData(Qt.UserRole, (query.value('cle'), True))
                brush = QBrush(QColor('orange'))
                lwi.setForeground(brush)
            else:
                lwi.setData(Qt.UserRole, (query.value('cle'), False))
            self.lstStatut.addItem(lwi)
            self.btnSauver.setVisible(False)
        #  Effacer la fiche
        self.lneNom.setText('')
        self.chkDefaut.setChecked(False)
        self.statutCour = -1


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           F O R M _ B I B L I O           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormBiblio(QDialog, DialogBiblio):
    def __init__(self, parent):
        super(FormBiblio, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.btSupprimer.setEnabled(False)
        self.btSauver.setEnabled(False)
        self.btOuvrir.setEnabled(False)
        self.statutCreer = False
        self.biblioCour = -1
        self.racine = ''

        self.btnFermer.clicked.connect(self.checkRacine)
        self.btnRacine.clicked.connect(self.evt_btnRacine_clicked)
        self.btSauver.clicked.connect(self.evt_btSauver_clicked)
        self.btOuvrir.clicked.connect(self.evt_btOuvrir_clicked)
        self.btSupprimer.clicked.connect(self.evt_btSupprimer_clicked)
        self.lstBiblio.clicked.connect(self.evt_lstBiblio_clicked)

        self.populateLstBiblio()

    def closeEvent(self, event):
        self.checkRacine()

    def checkRacine(self):
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM parametersTab')
        if query.next():
            aux = query.value('cleRacine')
            if aux != -1:
                self.biblioCour = aux
                query = QSqlQuery()
                bOk = query.exec(f'SELECT * FROM biblioTab WHERE cle = {aux}')
                if query.next():
                    self.parent.setWindowTitle(f"Bibliothèque courante : {query.value('nom')}")
                    try:
                        mainWindow.racine = query.value('path')
                        mainWindow.cleBiblio = aux
                    except:
                        exit()
            else:
                exit()
        else:
            exit()

    def evt_btSupprimer_clicked(self):
        pass

    def evt_btOuvrir_clicked(self):
        self.setCursor(Qt.WaitCursor)
        self.parent.cleBiblio = self.biblioCour
        query = QSqlQuery()
        query.exec(f'SELECT path FROM biblioTab WHERE cle = {self.biblioCour}')
        if query.next():
            self.parent.racine = query.value('path')

        query = QSqlQuery()
        tplChamps = ('cleRacine', 'autre')
        tplData = (self.biblioCour, 'ok')
        bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')
        self.btOuvrir.setEnabled(False)
        self.btSupprimer.setEnabled(False)
        self.btSauver.setEnabled(False)
        self.lneNom.setText('')
        self.lneChemin.setText('')
        self.biblioCour = -1


        lstVideo = []
        filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleBiblio={self.parent.cleBiblio}'

        query = QSqlQuery()
        query.exec(filtreSQL)
        lstVideo = []
        while query.next():
            lstVideo.append(VideoFileRecord(query.value('cle')))

        #  Première utilisation
        query1 = QSqlQuery()
        query1.exec(f'SELECT firstUse FROM parametersTab WHERE cle={1}')

        if query1.next():
            if query1.value('firstUse') == 1:
                QMessageBox.information(self, 'Première utilisation', "L'application va se fermer."
                                                                      "\nVeillez la redémarrer" )
                query1 = QSqlQuery()
                tplChamps = ('firstUse', 'autre')
                tplData = (0, 'ok')
                bOk = query1.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')
                sys.exit()

        self.parent.displayGridWindow(lstVideo)
        self.unsetCursor()
        self.close()

    def evt_btnRacine_clicked(self):
        self.lneNom.setText('')
        self.lneChemin.setText('')
        folder = QFileDialog.getExistingDirectory(self, 'Séleectionner la racine de la bibliothèque')
        if folder:
            self.racine = folder + '/'
            # query = QSqlQuery()
            # tplChamps = ('Racine', 'autre')
            # tplData = (self.racine, 'ok')
            # bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')
            self.lneChemin.setText(self.racine)
            self.statutCreer = True
            self.btSauver.setEnabled(True)
            self.btOuvrir.setEnabled(False)

    def evt_btSauver_clicked(self):
        if self.statutCreer:
            if self.lneNom.text() == '':
                QMessageBox.information(self, 'Nom de bibliothèque manquent', 'Veuillez saisir un nom pour la '
                                                                              'nouvelle bibliothèque')
            else:
                #  recherche du nouvelle cle
                query = QSqlQuery()
                bOK = query.exec('SELECT MAX(cle) FROM biblioTab')
                maxCle = 1
                try:
                    if bOK:
                        while query.next():
                            maxCle = query.value(0) + 1
                except:
                    pass

                tplData = (self.lneNom.text(), self.lneChemin.text(), maxCle)
                tplChamps = ('nom', 'path', 'cle')
                query = QSqlQuery()
                bOK = query.exec(f'INSERT INTO biblioTab {tplChamps} VALUES {tplData}')
                if bOK:
                    QMessageBox.information(self, 'Bibliothèque', 'Bibliothèque sucessfully added.')
                    self.btSauver.setEnabled(False)
                    self.btOuvrir.setEnabled(False)
                    self.btSupprimer.setEnabled(False)
                    self.populateLstBiblio()
                    self.lneNom.setText('')
                    self.lneChemin.setText('')
        else:  # Modification de la bibliothèque
            if self.lneNom.text() == '':
                QMessageBox.information(self, 'Nom de bibliothèque manquent', 'Veuillez saisir un nom pour la '
                                                                              'nouvelle bibliothèque')
            else:
                tplData = (self.lneNom.text(), self.lneChemin.text())
                tplChamps = ('nom', 'path')
                query = QSqlQuery()
                bOK = query.exec(f'UPDATE biblioTab  SET {tplChamps} = {tplData} WHERE cle = {self.biblioCour}')
                if bOK:
                    QMessageBox.information(self, 'Bibliothèque', 'Bibliothèque sucessfully updated.')
                    self.btSauver.setEnabled(False)
                    self.btOuvrir.setEnabled(False)
                    self.btSupprimer.setEnabled(False)
                    self.populateLstBiblio()
                    self.lneNom.setText('')
                    self.lneChemin.setText('')

    def evt_lstBiblio_clicked(self):
        itm = self.lstBiblio.currentItem()
        self.biblioCour = itm.data(Qt.UserRole)
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM biblioTab WHERE  cle = {self.biblioCour}')
        if query.next():
            self.lneNom.setText(query.value('nom'))
            self.racine = query.value('path')
            self.lneChemin.setText(query.value('path'))
            self.btSauver.setEnabled(True)
            self.btOuvrir.setEnabled(True)
            self.statutCreer = False
            self.btSupprimer.setEnabled(True)

    def populateLstBiblio(self):
        self.lstBiblio.clear()
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM biblioTab')
        while query.next():
            lwi = QListWidgetItem(query.value('nom'))
            lwi.setData(Qt.UserRole, query.value('cle'))
            self.lstBiblio.addItem(lwi)




# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************         F O R M P A R A M E T E R S       ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormParameters(QDialog, DialogParameters):
    def __init__(self, parent):
        super(FormParameters, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.btnRacine.setFixedSize(QSize(130, 35))
        self.lblRacine.setStyleSheet('border: 1px solid #3A3939;')

        try:
            f = open("DarkStyle.txt", 'r')
            contenu = f.read()
            self.setStyleSheet(contenu)
        except:
            pass

        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM parametersTab')
        if query.next():
            if query.value('racine') == '':
                self.lblRacine.setText('<- Cliquer pour saisir la racine de la bibliothèque')
            else:
                self.lblRacine.setText(query.value('racine'))
        else:
            self.lblRacine.setText('<- Cliquer pour saisir la racine de la bibliothèque')

        self.btnRacine.clicked.connect(self.evt_btnRacine_clicked)

    def evt_btnRacine_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, 'Séleectionner la racine de la bibliothèque')
        if folder:
            self.lblRacine.setText(folder)
            racine = folder + '/'
            query = QSqlQuery()
            tplChamps = ('Racine', 'autre')
            tplData = (racine, 'ok')
            bOk = query.exec(f'UPDATE parametersTab SET {tplChamps} = {tplData} WHERE cle = 1')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            F O R M C L A S S E U R        ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormClasseur(QDialog, dialogClasseur):
    def __init__(self, parent):
        super(FormClasseur, self).__init__()
        self.setupUi(self)
        self.indexCour = -1
        self.parent = parent
        self.boolMiseAJour = False

        try:
            f = open("DarkStyle.txt", 'r')
            contenu = f.read()
            self.setStyleSheet(contenu)
        except:
            pass

        self.initTabGeneral()
        self.populateList()

        #############################################
        ###  signal handler
        #############################################
        self.btnAnnuler.clicked.connect(self.evt_btnAnnuler_clicked)
        self.btnNouveau.clicked.connect(self.evt_btnNouveau_clicked)
        self.btnSauver.clicked.connect(self.evt_btnSauver_clicked)
        self.listClasseur.clicked.connect(self.populateFiche)
        self.btnDelete.clicked.connect(self.evt_btnDelete_clicked)
        # self.tabWidgetClasseur.currentChanged.connect(self.populateListVideo)

    # *******************************************************************************************************
    # *******************************************************************************************************
    # ***************  Slots Handlers
    # *******************************************************************************************************
    # *******************************************************************************************************
    def evt_btnAnnuler_clicked(self):
        if self.boolMiseAJour:
            self.parent.lstClasseurPopulate()
        self.close()

    def evt_btnNouveau_clicked(self):
        self.lneNom.setText('')
        self.lneNom.setEnabled(True)
        self.lneNom.setFocus()
        self.textEdit.setText('')
        self.textEdit.setEnabled(True)
        self.chkDefaut.setChecked(False)
        self.indexCour = -1

    def evt_btnSauver_clicked(self):
        if self.indexCour == -1:
            self.sauverNouveau()
        else:
            self.sauverModif()
        if mainWindow.gridWindow:
            mainWindow.gridWindow.cadreListClasseur.populateCadreListClasseur()
        if self.boolMiseAJour:
            self.parent.lstClasseurPopulate()
            self.close()

    def evt_btnDelete_clicked(self):
        if self.indexCour == -1:
            return
        #  recherche des vidéos éventuellement présente dans le classeur à supprimer
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab where cleClasseur={self.indexCour}')
        lstVideo = []
        while query.next():
            lstVideo.append(query.value('cle'))

        if len(lstVideo) == 0:
            pass
        else:
            pass

        rep = QMessageBox.question(self, 'Supprimer un classeur', 'Confirmez-vous la suppression?')
        if rep == QMessageBox.Yes:
            query = QSqlQuery()
            bOk = query.exec(f'DELETE FROM classeurTab WHERE cle={self.indexCour}')
            self.initTabGeneral()
            self.populateList()

    # ****************************************************************************
    # ****************************************************************************
    # ****************************************************************************
    def initTabGeneral(self):
        self.lneNom.setText('')
        self.lneNom.setEnabled(False)
        self.textEdit.setText('')
        self.textEdit.setEnabled(False)
        self.chkDefaut.setChecked(False)
        self.indexCour = -1

    def sauverNouveau(self):
        #  Gestion du classeur par défaut
        if self.chkDefaut.isChecked():  # supprimer l'ancien classseur par défaut
            boolDefaut = False
            query1 = QSqlQuery()
            bOk = query1.exec(f'SELECT cle FROM classeurTab WHERE defaut')
            if query1.next():
                tplChamps = ('defaut')
                tplData = (False)
                query2 = QSqlQuery()
                bOk = query2.exec(f'UPDATE classeurTab SET {tplChamps} = {tplData} WHERE cle={query1.value("cle")}')
            else:
                self.chkDefaut.setChecked(True)

        #  enregistrer le nouveau classeur
        query = QSqlQuery()
        #  Recherche de l'indice suivant pour la primary key
        bOK = query.exec('SELECT MAX(cle) FROM classeurTab')
        maxCle = 1
        try:
            if bOK:
                while query.next():
                    maxCle = query.value(0) + 1
        except:
            pass

        tplChamps = ('nom', 'commentaire', 'cle', 'defaut')
        #
        txt = self.lneNom.text().replace(chr(10), '$$')
        txt = txt.replace(chr(34), ')|')  # guillements
        txt = txt.replace(chr(9), 'µµ')  # Tabulation
        nom = txt
        #
        txt = self.textEdit.toPlainText().replace(chr(10), '$$')
        txt = txt.replace(chr(34), ')|')  # guillements
        txt = txt.replace(chr(9), 'µµ')  # Tabulation
        commentaire = txt
        tplData = (nom, commentaire, maxCle, self.chkDefaut.isChecked())
        bOK = query.exec(f'INSERT INTO classeurTab {tplChamps} VALUES {tplData}')
        if bOK:
            self.initTabGeneral()
            self.populateList()
        else:
            QMessageBox.critical(self, 'Database Error', f'Database Error \n\n{query.lastError().text()}')

    def sauverModif(self):
        if self.indexCour == -1:
            return
        #  Gestion du classeur par défaut
        if self.chkDefaut.isChecked():  # supprimer l'ancien classseur par défaut
            boolDefaut = False
            query1 = QSqlQuery()
            bOk = query1.exec(f'SELECT cle FROM classeurTab WHERE defaut')
            if query1.next():
                tplChamps = ('defaut')
                tplData = (False)
                query2 = QSqlQuery()
                bOk = query2.exec(f'UPDATE classeurTab SET {tplChamps} = {tplData} WHERE cle={query1.value("cle")}')
            else:
                self.chkDefaut.setChecked(True)

        #  enregistrer le nouveau classeur
        query = QSqlQuery()
        #  Recherche de l'indice suivant pour la primary key
        bOK = query.exec('SELECT MAX(cle) FROM classeurTab')
        maxCle = 1
        try:
            if bOK:
                while query.next():
                    maxCle = query.value(0) + 1
        except:
            pass

        tplChamps = ('nom', 'commentaire', 'cle', 'defaut')
        #
        txt = self.lneNom.text().replace(chr(10), '$$')
        txt = txt.replace(chr(34), ')|')  # guillements
        txt = txt.replace(chr(9), 'µµ')  # Tabulation
        nom = txt
        #
        txt = self.textEdit.toPlainText().replace(chr(10), '$$')
        txt = txt.replace(chr(34), ')|')  # guillements
        txt = txt.replace(chr(9), 'µµ')  # Tabulation
        commentaire = txt
        tplData = (nom, commentaire, maxCle, self.chkDefaut.isChecked())
        bOK = query.exec(f'UPDATE classeurTab SET {tplChamps} = {tplData} WHERE cle = {self.indexCour}')
        if bOK:
            self.initTabGeneral()
            self.populateList()
        else:
            QMessageBox.critical(self, 'Database Error', f'Database Error \n\n{query.lastError().text()}')

    def populateList(self):
        self.listClasseur.clear()
        query = QSqlQuery()
        bOk = query.exec('SELECT * from classeurTab ORDER BY nom')
        boolDefaut = False
        if bOk:
            while query.next():
                lwi = QListWidgetItem(query.value('nom'))
                lwi.setData(Qt.UserRole, (query.value('cle'), query.value('commentaire'), query.value('defaut')))
                if query.value('defaut'):
                    boolDefaut = True
                    brush = QBrush(QColor('orange'))
                    lwi.setForeground(brush)
                    self.listClasseur.addItem(lwi)
        else:
            QMessageBox.critical(self, 'Database Error', f'Database Error \n\n{query.lastError().text()}')
        self.initTabGeneral()

    def populateFiche(self):
        self.tabWidgetClasseur.setCurrentIndex(0)
        itm = self.listClasseur.currentItem()
        self.lneNom.setText(itm.text())
        self.indexCour, commentaire, defaut = itm.data(Qt.UserRole)
        self.textEdit.setPlainText(commentaire)
        self.lneNom.setEnabled(True)
        self.textEdit.setEnabled(True)
        if defaut:
            self.chkDefaut.setChecked(True)
        else:
            self.chkDefaut.setChecked(False)

        self.populateListVideo()

    def evt_table_signalFini(self):
        #  remise en place de l'aternance des couleurs dans les lignes de la tabWidget
        couleurBool = True
        couleur = '#666666'
        nb = self.table.rowCount()
        for i in range(0, nb):
            if couleurBool:
                couleur = '#666666'
                couleurBool = not couleurBool
            else:
                couleur = '#777777'
                couleurBool = not couleurBool
            self.table.item(i, 0).setBackground(QColor(couleur))
            #  mise à jour de la base avec les nouveaux ordreClasseur
            itm = self.table.item(i, 0)
            cle = itm.data(Qt.UserRole)
            query = QSqlQuery()
            tplChamps = ('ordreClasseur')
            tplData = (i + 1)
            bOk = query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle = {cle}')

    def populateListVideo(self):
        if self.indexCour == -1:
            return
        self.table = TableWidgetDragRows(self.tab_2)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setVisible(False)
        self.table.setGeometry(0, 0, 490, 350)
        self.table.signalFini.connect(self.evt_table_signalFini)

        lblAux = QLabel(self.tab_2)
        lblAux.setText("Déplacer les vidéos de la liste pour les ranger dans l'ordre souhaité")
        lblAux.setStyleSheet('color:#999999')
        lblAux.move(0, 360)

        self.table.setColumnCount(2)

        #  Construire les QLabel pour ls vidéos du classeur et populate la table
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab where cleClasseur={self.indexCour} ORDER BY ordreClasseur')
        lstCleVideo = []
        while query.next():
            lstCleVideo.append(query.value('cle'))
        self.table.setRowCount(len(lstCleVideo))
        i = 0
        couleurBool = True
        for cle in lstCleVideo:
            titre = ''
            note0 = ''
            query = QSqlQuery()
            bOk = query.exec(f'SELECT texte FROM paragraph where clevideo={cle} AND titre={True} AND '
                             f'indentation={0} AND timeNote={0}')
            if query.next():
                # self.lblTitre.setStyleSheet('font: 11pt; color:#eeeeec; font-weight: bold')
                titre = query.value('texte').replace('$$', chr(32))
                titre = titre.replace(')|', chr(34))  # guillements
                titre = titre.replace('µµ', chr(9))  # Tabulation
                # self.lblTitre.setText(aux)
            query1 = QSqlQuery()
            bOk = query1.exec(f'SELECT texte FROM paragraph where clevideo={cle} AND Note={True} AND '
                              f'indentation={0} AND picture={False}')
            if query1.next():
                note0 = query1.value('texte').replace('$$', chr(32))
                note0 = note0.replace(')|', chr(34))  # guillements
                note0 = note0.replace('µµ', chr(9))  # Tabulation
                # self.lblNote0.setText(aux)
            # lbl = QLabel(self)
            # lbl.setTextFormat(Qt.RichText)
            if couleurBool:
                couleur = '#666666'
                couleurBool = not couleurBool
            else:
                couleur = '#777777'
                couleurBool = not couleurBool
            self.table.setRowHeight(i, 25)
            lwi = QTableWidgetItem(titre)
            lwi.setData(Qt.UserRole, cle)
            self.table.setItem(i, 0, lwi)
            self.table.item(i, 0).setBackground(QColor(couleur))
            self.table.setColumnWidth(0, 460)
            self.table.setColumnWidth(1, 0)
            i += 1

    def __del__(self):
        boolDefaut = True
        query = QSqlQuery()
        bOk = query.exec(f'SELECT defaut, cle FROM classeurTab WHERE defaut={True}')
        if query.next():
            boolDefaut = True
        else:
            boolDefaut = False

        if not boolDefaut and not self.chkDefaut.isChecked():
            QMessageBox.information(self, 'Absence de classeur par défaut', 'Veuiilez choisir un classseur par défaut.')
            self.parent.evt_actClasseurVideo_clicked()

    def extractVignette(self):
        # recherche de la vignette
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM paragraph WHERE cleVideo=11 AND icone=True')
        if not query.next():
            return
        timeNote = query.value('timeNote')
        # recherche du chemin de la video
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle=11')
        if query.next():
            vidcap = mainWindow.racine + cv2.VideoCapture(query.value('internalPath') + query.value('VideoName'))
            vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
            success, image = vidcap.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if success:
                image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                pixmap01 = QPixmap.fromImage(image)
                return pixmap01


#  ************************************************************************************************
#  ************  FONCTIONS GLOBALES
#  ************************************************************************************************

# def onResize(event):
#
#     try:
#         w = mainWindow.gridWindow.mainWidget.width()
#         h = mainWindow.gridWindow.mainWidget.height()
#         x = w // 5
#         y = int(x * 0.74)
#         mainWindow.setWindowTitle(f'{w}, {h}, {x}, {y}')
#         for itm in mainWindow.gridWindow.lstVignette:
#             lbl, lblTitre, pixmap01 = itm
#             lbl.setPixmap(pixmap01.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation))
#             lbl.setFixedSize(QSize(x, y))
#     except:
#         pass


def extractPicture(video, haut, large, timeNote):
    vidcap = cv2.VideoCapture(video)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
    success, image = vidcap.read()
    if success:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image


def strTime(seconde):
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


#  *********************************************************************************************
def decoupe(seconde):
    heure = seconde / 3600
    seconde %= 3600
    minute = seconde / 60
    seconde %= 60
    strHeure, strMinute, strSeconde = '', '', ''
    if heure >= 10:
        strHeure = str(heure)
    else:
        strHeure = '0' + str(heure)[0]
    if minute >= 10:
        strMinute = str(minute)
    else:
        strMinute = '0' + str(minute)[0]
    if seconde >= 10:
        strSeconde = str(seconde)
    else:
        strSeconde = '0' + str(seconde)[0]
    return (f'{strHeure}:{strMinute}:{strSeconde}')


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
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # f = open('ressources/DarkStyle.txt', 'r')
    # style = f.read()
    # app.setStyleSheet(style)

    #  Création de la fenêtre principale
    global mainWindow
    mainWindow = MainWindow()
    #  Récupération du paramètre NbVideosRecentes
    query1 = QSqlQuery()
    query1.exec(f'SELECT NbVideosRecentes FROM parametersTab')
    NbVideosRecentes = 5
    if query1.next():
        NbVideosRecentes = query1.value('NbVideosRecentes')
    mainWindow.NbVideosRecentes = NbVideosRecentes
    filtreSQL = f'SELECT cle FROM videoFileTab WHERE cleBiblio={mainWindow.cleBiblio}'

    filtreSQLRecent = f' ORDER BY dateLastView DESC LIMIT {mainWindow.NbVideosRecentes}'

    query = QSqlQuery()
    query.exec(filtreSQL + filtreSQLRecent)
    lstVideo = []
    while query.next():
        lstVideo.append(VideoFileRecord(query.value('cle')))

    listTempOnglet = []
    mainWindow.filtreCour = (filtreSQL, listTempOnglet)

    mainWindow.displayGridWindow(lstVideo)

    mainWindow.show()
    sys.exit(app.exec_())

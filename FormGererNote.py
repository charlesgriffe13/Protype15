import sys
import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from AtelierDesign2022 import ParagrapheRecord, VideoFileRecord, FormWebBrowser

class FormGererNote(QDialog):
    def __init__(self, parent, videoPath, videoID, marqueCour, boolCreer):
        super(FormGererNote, self).__init__()
        QDialog.__init__(self)
        self.parent = parent
        self.videoPath = videoPath
        self.videoID = videoID
        self.marqueCour = marqueCour
        self.lienCour = -1
        self.setWindowTitle('Gestion des notes')

        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('c:/videoFinder/protype/data/VideoLearnerX.db')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            print(db.tables())

        self.videoCour = VideoFileRecord(videoID)
        self.setGeometry(100, 100, 640, 700)
        self.setFixedHeight(820)

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

        img = self.extractPicture(self.videoPath, 266, 431, self.marqueCour)
        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(qimg)
        # self.lblImage.setPixmap(pixmap01.scaled(431, 266, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        #  Initialisation du racclourci clavier pour créer des tags
        # self.shortCutTag = QShortcut(QKeySequence('Ctrl+T'), self)
        # self.shortCutTag.activated.connect(self.creerTag)

    def setupUI(self):

        #**************************************************************
        #  Layout Principal
        self.lytMain =QVBoxLayout()
        self.setLayout(self.lytMain)
        #  Entete
        lytEntete = QHBoxLayout()
        self.lytMain.addLayout(lytEntete)
        query = QSqlQuery()
        query.exec(f'SELECT texte FROM paragraph where clevideo={self.videoID} AND titre={True} AND timeNote={0}')
        if query.next():
            lblEntete = QLabel(query.value('texte'))
            lblEntete.setFont(QFont('Arial', 14))
            lblEntete.setFixedHeight(50)
            lblEntete.setStyleSheet('color: gray')
            lytEntete.addWidget(lblEntete)
            spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            lytEntete.addItem(spacerItem)
            lblTimeCode = QLabel()
            lblTimeCode.setFixedHeight(50)
            lblTimeCode.setText(f'Timecode : {strTime(self.marqueCour)}')
            lytEntete.addWidget(lblTimeCode)
        #  Titre
        lytTitre = QVBoxLayout()
        self.lytMain.addLayout(lytTitre)
        self.tedTitre = QTextEdit()
        self.tedTitre.setPlaceholderText('Saisir ou modifier le titre de la vidéo')
        self.tedTitre.setStyleSheet('border: 1px solid red')
        self.tedTitre.setFixedHeight(55)
        self.tedTitre.setFont(QFont('Arial', 12))
        lytTitre.addWidget(self.tedTitre)
        #  Note
        lytTexte = QVBoxLayout()
        self.lytMain.addLayout(lytTexte)
        self.tedTexte = QTextEdit()
        self.tedTexte.setStyleSheet('border: 1px solid red')
        self.tedTexte.setFixedHeight(150)
        self.tedTexte.setPlaceholderText('Saisir ou modifier le titre de la vidéo')
        lytTexte.addWidget(self.tedTexte)
        #  Lien Web
        lytLienWeb = QHBoxLayout()
        self.lytMain.addLayout(lytLienWeb)
        self.lneURL = QLineEdit()
        self.lneURL.setStyleSheet('border: 1px solid red')
        self.lneURL.setPlaceholderText("Saisir ou coller l'URL du site")
        self.lneURL.setFixedHeight(35)
        lytLienWeb.addWidget(self.lneURL)
        self.btnLienWeb = QPushButton('Afficher le site')
        self.btnLienWeb.setFixedSize(QSize(111, 35))
        lytLienWeb.addWidget(self.btnLienWeb)
        #  Image
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
        #  Tag
        from FormGrpBoxTag import GrpBoxTag
        grpBoxTag = GrpBoxTag(self, self.videoID)
        self.lytMain.addWidget(grpBoxTag)
        #  Boutons
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
        self.btnLienWeb.clicked.connect(self.evt_btnLienWeb_clicked)
        self.btnAnnuler.clicked.connect(self.close)
        self.tedTitre.textChanged.connect(self.evt_tedTitre_textChanged)
        self.tedTexte.textChanged.connect(self.evt_tedTexte_textChanged)
        self.lneURL.textChanged.connect(self.evt_lneURL_textChanged)
        # self.lneLegende.textChanged.connect(self.evt_lneLegende_textChanged)
        self.chkIgnorer.stateChanged.connect(self.evt_chkIgnorer_stateChanged)

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
        if self.tedTitre.toPlainText() == '':
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
        win = FormWebBrowser(self)
        win.resize(QSize(600, 500))
        win.show()

    def evt_btnSauver_clicked(self):
        message = ''
        if self.boolCadreRougeTitre:
            message += 'Titre'
        if self.boolCadreRougeImage:
            if message !='':
                message += ', image'
            else:
                message += 'image'
        if self.boolCadreRougeTexte:
            if message !='':
                message += ', note'
            else:
                message += 'note'
        if self.boolCadreRougeURL:
            if message !='':
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
            if self.tedTitre.toPlainText() == ''and self.boolCreer:
                pass
                # QMessageBox.information(self, "Enregistrement du titre", "Enregistrement du titre impossible,\n"
                #                                                          "aucune donnée n'a été saisie.")
            else:
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
                                  'cleVideo', 'cle', 'note', 'lienWeb')
                    txt = self.tedTitre.toPlainText().replace(chr(10), '$$')
                    txt = txt.replace(chr(34), ')|')  # guillements
                    txt = txt.replace(chr(9), 'µµ')  # Tabulation
                    tplData = (self.marqueCour, 0, True, False, 337, 647, txt, self.videoID, self.cleTitreCour,
                               False, False)
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                #  Cas d'une modification
                else:
                    if self.tedTitre.toPlainText() == '':
                        # Suppression
                        query = QSqlQuery()
                        bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleTitreCour}')
                    else:
                        txt = self.tedTitre.toPlainText().replace(chr(10), '$$')
                        txt = txt.replace(chr(34), ')|')  # guillements
                        txt = txt.replace(chr(9), 'µµ')  # Tabulation
                        tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                     'texte', 'cleVideo', 'Note', 'lienWeb')
                        tplData = (self.marqueCour, 0, True, False, 337, 647, txt
                                   , self.videoID, False, False)
                        # print(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE cle = {self.cleTitreCour}')
                        bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                         f'cle = {self.cleTitreCour}')
            #  ********************************************************************************
            #  Cas de la note
            #  ********************************************************************************
            if self.tedTexte.toPlainText() == '' and self.boolCreer:
                pass
                # QMessageBox.information(self, "Enregistrement de la note", "Enregistrement de la note impossible,\n"
                #                                                          "aucune donnée n'a été saisie.")
            else:
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
                    self.cleTexteCour = maxCle
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                                 'cleVideo', 'cle', 'note', 'lienWeb')
                    txt = self.tedTexte.toPlainText().replace(chr(10), '$$')
                    txt = txt.replace(chr(34), ')|')  # guillements
                    txt = txt.replace(chr(9), 'µµ')  # Tabulation
                    tplData = (self.marqueCour, 0, False, False, 337, 647, txt, self.videoID, self.cleTexteCour,
                               True, False)
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
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
                                     'texte', 'cleVideo', 'Note', 'lienWeb')
                        tplData = (self.marqueCour, 0, False, False, 337, 647, txt
                                   , self.videoID, True, False)
                        bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                         f'cle = {self.cleTexteCour}')
            #  ********************************************************************************
            #  cas de l'image
            #  ********************************************************************************
            if self.chkIgnorer.isChecked() and self.boolCreer:
                pass
                # QMessageBox.information(self, "Enregistrement de l'image", "Enregistrement de l'image impossible,\n"
                #                                                          "la case Ignorer a été cochée.")
            else:
                #  recherche de l'index suivant par la primary key
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                #  Cas d'une création
                if self.boolCreer or self.cleImageCour == 0:
                    self.cleImageCour = maxCle
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                                  'cleVideo', 'cle', 'note', 'lienWeb')
                    txt = self.lneLegende.text()
                    tplData = (self.marqueCour, 0, False, True, 337, 647, txt, self.videoID, self.cleImageCour,
                               False, False)
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                #  Cas d'une modification
                else:
                    if self.chkIgnorer.isChecked():
                        # Suppression
                        query = QSqlQuery()
                        bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleImageCour}')
                    else:
                        txt = self.lneLegende.text()
                        tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                     'texte', 'cleVideo', 'Note', 'lienWeb')
                        tplData = (self.marqueCour, 0, False, True, 337, 647, txt
                                   , self.videoID, False, False)
                        bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                         f'cle = {self.cleImageCour}')
            #  ********************************************************************************
            #  Cas du lien Web
            #  ********************************************************************************
            if self.lneURL.text() == '' and self.boolCreer:
                pass
                # QMessageBox.information(self, "Enregistrement du lien Web", "Enregistrement du lien Web impossible,\n"
                #                                                          "aucune donnée n'a été saisie.")
            else:
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
                    self.cleWebCour = maxCle
                    tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur', 'texte',
                                 'cleVideo', 'cle', 'note', 'lienWeb')
                    txt = self.lneURL.text()
                    tplData = (self.marqueCour, 0, False, False, 337, 647, txt, self.videoID, self.cleWebCour,
                               False, True)
                    query = QSqlQuery()
                    query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                #  Cas d'une modification
                else:
                    if self.lneURL.text() == '':
                        # Suppression
                        query = QSqlQuery()
                        bOK = query.exec(f'DELETE FROM paragraph WHERE cle = {self.cleWebCour}')
                    else:
                        txt = self.lneURL.text()
                        tplChamps = ('timeNote', 'indentation', 'titre', 'picture', 'hauteur', 'largeur',
                                     'texte', 'cleVideo', 'Note', 'lienWeb')
                        tplData = (self.marqueCour, 0, False, False, 337, 647, txt
                                   , self.videoID, False, True)
                        bOK = query.exec(f'UPDATE paragraph  SET {tplChamps} = {tplData} WHERE '
                                         f'cle = {self.cleWebCour}')
        #  Mise à jour de paragraph
        self.boolCreer = False
        QMessageBox.information(self, "Enregistrement", "L'opération a été réalisée.")
        self.btnSauver.setIcon(QIcon('ressources/cocher.png'))
        # objNote.populateObjNote(self.videoID)

    def extractPicture(self, video, haut, large, timeNote):
        try:
            vidcap = cv2.VideoCapture(video)
            vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
            success, image = vidcap.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if success:
                return image
        except:
            pass



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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aux = 'C:/VideoFinder/Protype/video/Keep It - Preview.mp4'
    win = FormGererNote(app, videoPath=aux, videoID=223, marqueCour=125, boolCreer=True)
    win.show()
    sys.exit(app.exec_())
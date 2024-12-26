from PyQt5.QtSql import *
from PyQt5.QtCore import *
from VF_MainTab_UI import Ui_MainWindow
from PyQt5.QtWidgets import *
import sys
import cv2
import qdarkstyle
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtGui import *

class DlgMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)
        # self.setWindowState(Qt.WindowMaximized)
        # rendre la barre d'outils horizontale supérieure invisible
        # self.toolBar.setVisible(False)

        # self.setFixedSize(1213, 663)
        self.setGeometry(100, 60, 1213, 663)

        self.lblTitre.setFixedHeight(63)
        self.lytTitre.setAlignment(Qt.AlignTop)

        self.lytListe.setAlignment(Qt.AlignLeft)

        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('c:/videoFinder/Atelier_Constructor/data/VideoLearnerX.db')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            print(db.tables())

        # ***************************************************************
        # ******  Initialisation des vignettes
        # ***************************************************************

        #  Récupération des cle des vidéos de la base
        query = QSqlQuery()
        lstVideo = []
        bOk = query.exec(f'SELECT * FROM videoFileTab')

        while query.next():
            lstVideo.append(query.value('cle'))

        for x in range(4):
            for y in range(5):
                index = x * 4 + y
                # Création vignette
                lblVignette = QLabel()
                lblVignette.setStyleSheet('border-radius: 4px; border: 1px solid gray')
                lblVignette.setFixedSize(192, 107)
                self.lytGrille.addWidget(lblVignette, 2*x, y)
                # Création titre vidéo2
                lblTitre = QLabel('...')
                # lblTitre.setStyleSheet('border-radius: 4px; border: 1px solid gray')
                lblTitre.setFixedSize(192, 20)
                self.lytGrille.addWidget(lblTitre, 2 * x+1, y)
                if index + 1 <= len(lstVideo):
                    videoCleTest = lstVideo[index]
                    query1 = QSqlQuery()
                    bOk = query1.exec(f'SELECT * FROM paragraph WHERE cleVideo = {videoCleTest} AND icone = True')
                    if query1.next():
                        timeNote = query1.value('timeNote')
                        query2 = QSqlQuery()
                        bOk = query2.exec(f'SELECT videoFullPath, videoName FROM videoFileTab WHERE cle = {videoCleTest}')
                        if query2.next():
                            # print(query2.value(('videoFullPath')))
                            vidcap = cv2.VideoCapture(query2.value('videoFullPath'))
                            vidcap .set(cv2.CAP_PROP_POS_MSEC, timeNote*1000)
                            success, image = vidcap.read()
                            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            if success:
                                image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                                pixmap01 = QPixmap.fromImage(image)
                                lblVignette.setPixmap(pixmap01.scaled(192, 107, Qt.KeepAspectRatio,
                                                                      Qt.SmoothTransformation))
                            lblTitre.setText(query2.value('videoName'))
                    else:
                        query2 = QSqlQuery()
                        bOk = query2.exec(f'SELECT videoFullPath, videoName FROM videoFileTab WHERE cle = {videoCleTest}')
                        if query2.next():
                            lblTitre.setText(query2.value('videoName'))


        self.cmbStatut.setFixedWidth(200)
        self.lneRecherche.setFixedWidth(300)
        self.btnLoupe.setIcon(QIcon('ressources/loupe.png'))
        self.btnLoupe.setFixedSize(QSize(34, 32))
        self.btnLoupe.setStyleSheet('background-color: #F05A24')

        # ***************************************************************
        # ******  Initialisation de la liste des statuts
        # ***************************************************************
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM statutTab Order BY nom')
        self.cmbStatut.clear()
        while query.next():
            self.cmbStatut.addItem(query.value('nom'), query.value('cle'))
        # self.cmbStatut.setCurrentIndex(indexCour)

    # ***************************************************************
    # ***************************************************************
    # ******  M E T H O D E S
    # ***************************************************************
    # ***************************************************************

    def videoNbFrameDuration(self, video):
        v = cv2.VideoCapture(video)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        return frame_count, duration

    def videoDuration(self, video):
        # print(video)
        v = cv2.VideoCapture(video)
        #  v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        # QMessageBox.information(self, '', str(duration))
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

    def extractVignette(self):
        self.lblIcone.setPixmap(QPixmap())
        self.lblIcone.setStyleSheet('border-radius:4px; border: 1px solid gray')
        # recherche de la vignette
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM paragraph WHERE cleVideo={self.parent.videoID} AND icone=True')
        if not query.next():
            return
        timeNote = query.value('timeNote')
        # recherche du chemin de la video
        query = QSqlQuery()
        bOk = query.exec(f'SELECT videoFullPath FROM videoFileTab WHERE cle={self.parent.videoID}')
        if query.next():
            vidcap = cv2.VideoCapture(query.value('videoFullPath'))
            vidcap.set(cv2.CAP_PROP_POS_MSEC, timeNote * 1000)
            success, image = vidcap.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if success:
                image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                pixmap01 = QPixmap.fromImage(image)
                self.lblIcone.setPixmap(pixmap01.scaled(182, 111, Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == '__main__':

    def catch_exceptions(t, val, tb):
        QMessageBox.critical(None,
                             "An exception was raised",
                             "Exception type: {}".format(t))
        old_hook(t, val, tb)
    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


    app = QApplication(sys.argv)

    dlgMain = DlgMain()
    dlgMain.show()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    sys.exit(app.exec_())

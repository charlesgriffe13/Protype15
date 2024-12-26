
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import *

# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************               L A B E L T A G             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelTag(QLabel):
    def __init__(self, texte):
        super(LabelTag, self).__init__()
        self.texte = texte
        self.setStyleSheet('border:1px; background-color: gray; border: 1px solid gray; border-radius: 10px')
        self.width = self.fontMetrics().boundingRect(texte).width()
        self.setFixedWidth(self.width + 20)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignCenter)
        self.setText(texte)

    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('ok')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             G R P B O X T A G             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GrpBoxTag(QGroupBox):
    def __init__(self, parent, videoID):
        super().__init__()
        self.setFixedWidth(640)
        self.parent = parent
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False


        self.lneTag = QLineEdit(self)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText('Saisir un tag ou cliquer sur la liste...')
        self.setStyleSheet('margin: 0px')
        self.lneTag.setStyleSheet('margin: 0px')
        self.lneTag.setFixedWidth(640)
        self.parent.lytMain.addWidget(self.lneTag)

        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))

        self.grpBoxAffichTag = QGroupBox()
        self.grpBoxAffichTag.setStyleSheet('border: 0px')
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        self.grpBoxAffichTag.setFixedWidth(590)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(self.grpBoxAffichTag)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(220)
        scroll.setFixedWidth(620)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        self.populateGrpBoxAffichTag()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            menu = QMenu()
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
                tplChamps = ('cle', 'cleVideo', 'mot')
                tplData = (cle, self.videoID, self.lneTag.text())
                bOk = query.exec(f'UPDATE tagTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
                self.populateGrpBoxAffichTag()
            else:
                #  Recherche de l'index suivant
                cleMax = 1
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) AS cleMax FROM tagTab')
                if query.next():
                    cleMax = query.value('cleMax') + 1
                tplData = (cleMax, self.videoID, mot)
                tplChamps = ('cle', 'cleVideo', 'mot')
                query1 = QSqlQuery()
                query1.exec(f'INSERT INTO tagTab {tplChamps} VALUES {tplData}')
                self.listTag.append(mot)
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
        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))

        i = 0
        continuerLigne = True
        largLigneTag = 0
        largeur = 400
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
                lblTag = LabelTag(self.listTag[i])
                lblTag.installEventFilter(self)
                largLigneTag += lblTag.width + offSet
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





# if __name__ == '__main__':
#     app = QApplication(['Test'])
#     window = GrpBoxTag(12)
#     window.setGeometry(500, 300, 640, 180)
#     window.show()
#     app.exec_()
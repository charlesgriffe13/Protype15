from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from AtelierClassCommun import MainWindowCustom, DialogCustom, VideoFileRecord, LabelTag, FormBlockNote, \
    PastilleSimple, LabelIndex
import subprocess
from PyQt5.QtSql import QSqlQuery
from unicodedata import normalize, combining
import cv2
import sys
from datetime import date


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           T I M E P I C K U P                    ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TimePickUp(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('border-radius: 4px; color: #333; background-color: #ddd')
        self.setFixedSize(240, 25)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        font = QFont()
        font.setFamily('Ariel')
        font.setPointSize(6)
        #
        lblHeure = QLabel(self)
        lblHeure.setFont(font)
        lblHeure.setText(self._trad('Heure :', self.lngCourGlobal))
        lblHeure.setFixedSize(40, 25)
        lblHeure.move(2, 0)
        self.spinHeure = QSpinBox(self)
        self.spinHeure.setMinimum(0)
        self.spinHeure.setMaximum(10)
        self.spinHeure.setValue(0)
        self.spinHeure.setFixedSize(35, 25)
        self.spinHeure.move(40, 1)
        #
        lblMinute = QLabel(self)
        lblMinute.setFont(font)
        lblMinute.setText(self._trad('Minute :', self.lngCourGlobal))
        lblMinute.setFixedSize(50, 25)
        lblMinute.move(82, 0)
        self.spinMinute = QSpinBox(self)
        self.spinMinute.setMinimum(0)
        self.spinMinute.setMaximum(59)
        self.spinMinute.setValue(0)
        self.spinMinute.setFixedSize(35, 25)
        self.spinMinute.move(120, 1)
        #
        lblSeconde = QLabel(self)
        lblSeconde.setFont(font)
        lblSeconde.setText(self._trad('Seconde :', self.lngCourGlobal))
        lblSeconde.setFixedSize(50, 25)
        lblSeconde.move(160, 0)
        self.spinSeconde = QSpinBox(self)
        self.spinSeconde.setMinimum(0)
        self.spinSeconde.setMaximum(59)
        self.spinSeconde.setValue(0)
        self.spinSeconde.setFixedSize(35, 25)
        self.spinSeconde.move(205, 1)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def value(self):
        return self.spinHeure.value() * 3600 + self.spinMinute.value() * 60 + self.spinSeconde.value()

    def display(self, heure, minute, seconde):
        self.spinHeure.setValue(heure)
        self.spinMinute.setValue(minute)
        self.spinSeconde.setValue(seconde)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************          L A B E L    D A T A                    ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class LabelData(QLabel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.parent = parent
        self.data = data


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             F O R M S A V E D S E A R C H        ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormSavedSearch(MainWindowCustom):
    def __init__(self, parent, contenant):
        super().__init__()
        self.parent = parent
        self.contenant = contenant
        self.setGeometry(200, 100, 970, 600)

        self.setPoignee(False)
        self.setBtnMax(False)
        self.setBtnMini(False)
        self.boolModif = False
        self.cleLineCour = 0
        self.cleSavedSearchCour = 0

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.setTitle(self._trad('   Requètes sauvegardées', self.lngCourGlobal))
        self.setUpUi()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def setUpUi(self):
        #  ***********************************************************************************************
        #  Cadre top listWidgetSavedSearch
        grpTop = QGroupBox(self)
        grpTop.setFixedSize(250, 557)
        grpTop.setStyleSheet('background-color: #444; border: 0px')
        grpTop.move(4, 38)
        #  Widget listWidgetSavedSearch
        self.listWidgetSavedSearch = QListWidget(grpTop)
        self.listWidgetSavedSearch.setFixedSize(240, 540)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        self.listWidgetSavedSearch.setStyleSheet('background-color: #333; color: #aaa')
        self.listWidgetSavedSearch.move(5, 5)
        self.listWidgetSavedSearch.itemClicked.connect(self.evt_listSavedSearch_itemClicked)
        self.populatelistWidgetSavedSearch()

        #  ***********************************************************************************************
        #  Cadre Nom listWidgetSavedSearch
        grpNom = QGroupBox(self)
        grpNom.setFixedSize(708, 50)
        grpNom.setStyleSheet('background-color: #444; border: 0px')
        grpNom.move(257, 38)
        # lblNom
        lblNom = QLabel(grpNom)
        lblNom.setText(self._trad('Nom : ', self.lngCourGlobal))
        lblNom.setStyleSheet('color: #aaa')
        lblNom.move(10, 15)
        # lneNom
        self.lneNom = QLineEdit(grpNom)
        self.lneNom.setFixedSize(400, 30)
        self.lneNom.setText('')
        self.lneNom.setStyleSheet('color: white; border: 1px solid #666')
        self.lneNom.move(50, 10)

        self.widget = QWidget(self)
        self.widget.setStyleSheet('background-color: #444')
        self.widget.setFixedSize(708, 440)
        self.widget.move(257, 91)
        self.lytCadre = QVBoxLayout()
        self.widget.setLayout(self.lytCadre)
        self.cadreBuildSearch = CadreBuildSearch(self.widget, self)
        self.lytCadre.addWidget(self.cadreBuildSearch)
        #  ***********************************************************************************************
        #  Zone des boutons sauver, fermer, supprimer, nouveau
        #  Bouton sauver
        self.btnSauver = QPushButton(self)
        self.btnSauver.setText(self._trad('Sauver', self.lngCourGlobal))
        self.btnSauver.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSauver.setFixedSize(100, 35)
        self.btnSauver.move(730, 550)
        self.btnSauver.clicked.connect(self.sauveLine)
        #
        #  Bouton supprimer
        self.btnSupprimer = QPushButton(self)
        self.btnSupprimer.setText(self._trad('Supprimer', self.lngCourGlobal))
        self.btnSupprimer.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                        'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnSupprimer.setFixedSize(100, 35)
        self.btnSupprimer.move(620, 550)
        self.btnSupprimer.clicked.connect(self.supprimeSavedSearch)
        #
        #  Bouton nouveau
        self.btnNouveau = QPushButton(self)
        self.btnNouveau.setText(self._trad('Nouveau', self.lngCourGlobal))
        self.btnNouveau.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                      'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnNouveau.setFixedSize(100, 35)
        self.btnNouveau.move(510, 550)
        self.btnNouveau.clicked.connect(self.evt_btnNouveau_clicked)
        #
        #  Bouton exécuter
        self.btnExecuter = QPushButton(self)
        self.btnExecuter.setText(self._trad('Exécuter', self.lngCourGlobal))
        self.btnExecuter.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                      'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnExecuter.setFixedSize(100, 35)
        self.btnExecuter.move(260, 550)
        self.btnExecuter.clicked.connect(self.evt_btnExecuter_clicked)

    def evt_btnExecuter_clicked(self):
        if len(self.cadreBuildSearch.listLineSavedSearch) == 0:
            return
        self.contenant.boolModifExecuterSearch = True
        self.contenant.selectZoneDroit.populateLstVideoSelect()
        self.close()


    def supprimeSavedSearch(self):
        query = QSqlQuery()
        bOk = query.exec(f'DELETE FROM savedSearchTab WHERE indiceLigne={self.cleLineCour}')
        #  *****************************************************************************
        #  Faire disparaitre la ou les lignes en cours
        for line in self.cadreBuildSearch.listLineSavedSearch:
            line.close()
        i = len(self.cadreBuildSearch.listLineSavedSearch)
        self.cadreBuildSearch.grp.setFixedHeight(i * 45)
        try:
            self.spacer.close()
        except:
            pass
        self.lneNom.setText('')
        self.populatelistWidgetSavedSearch()

    def sauveLine(self):
        #  *****************************************************************************
        #  Suppression des lignes de la trequète courante (self.cleLineCour) puis enregistrement
        query = QSqlQuery()
        bOk = query.exec(f'DELETE FROM savedSearchTab WHERE indiceLigne={self.cleLineCour}')

        #  *****************************************************************************
        #  indice max de la ligne dans la requéte en cours d'enregistrement
        query = QSqlQuery()
        query.exec(f'SELECT MAX(cle) FROM savedSearchTab')
        maxCle = 0
        try:
            if query.next():
                maxCle = query.value(0) + 1
        except:
            maxCle = 1
        #  Si le titre a été oublié
        if self.lneNom.text() == '':
            self.lneNom.setText(f'Nouvelle requète {maxCle}')
        #  indice max de la requète (indiceLigne)
        query = QSqlQuery()
        query.exec(f'SELECT MAX(indiceLigne) FROM savedSearchTab')
        maxIndiceLigne = 0
        try:
            if query.next():
                maxIndiceLigne = query.value(0) + 1
        except:
            maxIndiceLigne = 1

        for line in self.cadreBuildSearch.listLineSavedSearch:
            maxCle += 1
            indiceChamp = line.cmbChamp.currentIndex()
            print(indiceChamp)
            #  **********************************************************************
            if indiceChamp == 0:  # Nom
                indiceOperateur = line.cmbOperateur.currentIndex()
                textValeur = line.lneValeur.text()
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'textValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, textValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 1:  # Dossier
                indiceOperateur = line.cmbOperateur.currentIndex()
                indice = line.cmbValeur.currentIndex()
                indiceValeur = line.cmbValeur.itemData(indice) - 1
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'indiceValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, indiceValeur,
                           self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 2:  # Favori
                indiceOperateur = line.cmbOperateur.currentIndex()
                indice = line.cmbValeur.currentIndex()
                indiceValeur = line.cmbValeur.itemData(indice)

                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'indiceValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, 0, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 3:  # Tag paragraph
                indiceOperateur = line.cmbOperateur.currentIndex()
                textValeur = line.lneValeur.text()
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'textValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, textValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 4:  # Création - date d'entrée de la vidéo dans la base
                indiceOperateur = line.cmbOperateur.currentIndex()
                dateValeur = line.dateValeur.date().toString('yyyy/MM/dd')
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'dateValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, dateValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 5:  # duration
                indiceOperateur = line.cmbOperateur.currentIndex()
                timeValeur = line.timeValeur.value()
                query = QSqlQuery()

                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'timeValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, timeValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 6:  # Rating
                indiceOperateur = line.cmbOperateur.currentIndex()
                indice = line.cmbValeur.currentIndex()
                indiceValeur = line.cmbValeur.itemData(indice)
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'indiceValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, indice, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 7:  # Dernier visionnage
                indiceOperateur = line.cmbOperateur.currentIndex()
                dateValeur = line.dateValeur.date().toString('yyyy/MM/dd')

                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'dateValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, dateValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 8:  # statut (label)
                indiceOperateur = line.cmbOperateur.currentIndex()
                indiceValeur = line.cmbValeur.currentIndex() + 1
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'indiceValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, indiceValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
            if indiceChamp == 9:  # Note
                indiceOperateur = line.cmbOperateur.currentIndex()
                indice = line.cmbValeur.currentIndex()
                textValeur = line.lneValeur.text()
                query = QSqlQuery()
                tplChamps = ('cle', 'indiceLigne', 'indiceChamp', 'indiceOperateur', 'textValeur', 'nom')
                tplData = (maxCle, maxIndiceLigne, indiceChamp, indiceOperateur, textValeur, self.lneNom.text())
                query.exec(f'INSERT INTO savedSearchTab {tplChamps} VALUES {tplData}')
            #  **********************************************************************
        #  Faire disparaitre la ou les lignes en cours
        for line in self.cadreBuildSearch.listLineSavedSearch:
           line.close()
        i = len(self.cadreBuildSearch.listLineSavedSearch)
        self.cadreBuildSearch.grp.setFixedHeight(i * 45)
        try:
            self.spacer.close()
        except:
            pass
        self.lneNom.setText('')
        self.populatelistWidgetSavedSearch()

    def evt_btnNouveau_clicked(self):
        for line in self.cadreBuildSearch.listLineSavedSearch:
            line.close()
        self.boolModif = False
        self.cadreBuildSearch.close()
        self.cadreBuildSearch = CadreBuildSearch(self.widget, self)
        self.lytCadre.addWidget(self.cadreBuildSearch)
        # Création de la p1ère ligne
        self.lneNom.setText('')
        self.cadreBuildSearch.listLineSavedSearch = []
        self.cadreBuildSearch.createLine()

    def populatelistWidgetSavedSearch(self):
        self.listWidgetSavedSearch.clear()
        #  Chargement des requètes enregistrée
        query = QSqlQuery()
        query.exec(f'SELECT nom, indiceLigne FROM savedSearchTab GROUP BY indiceLigne')
        while query.next():
            lbl = QLabel()
            lbl.setFixedSize(27, 27)
            lbl.setPixmap(QPixmap('ressources\savedSearch.png'))
            item = QListWidgetItem(self.listWidgetSavedSearch)
            item.setSizeHint(QSize(0, 40))
            item.setText(f"        {query.value('nom')}")
            item.setData(1, query.value('indiceLigne'))
            self.listWidgetSavedSearch.addItem(item)
            self.listWidgetSavedSearch.setStyleSheet('color: #eee')
            self.listWidgetSavedSearch.setItemWidget(item, lbl)

    def evt_listSavedSearch_itemClicked(self, item):
        #  effacer le contenu du cadreBuildSearch
        self.cadreBuildSearch.clearLytCadre()
        self.cadreBuildSearch.listLineSavedSearch = []

        self.boolModif = True
        cleRequete = item.data(1)
        self.cleLineCour = cleRequete #  clé de la requète courante
        query = QSqlQuery()
        query.exec(f'SELECT * FROM savedSearchTab WHERE indiceLigne={cleRequete}')
        # print(cleRequete)
        i = 0
        while query.next():
            self.lneNom.setText(query.value('nom'))
            self.cadreBuildSearch.createLine()
            indiceList = len(self.cadreBuildSearch.listLineSavedSearch) - 1 #  indiceList : commence à 0 dans la list
                                                                            #  qui commence à 1 dans la table
            cleLigne = query.value('cle') #  clé de la ligne courante dans la requète
            ligne = self.cadreBuildSearch.listLineSavedSearch[indiceList]
            ligne.cleRequete = cleRequete
            ligne.cleLigne = cleLigne
            ligne.indiceValeur = query.value('indiceValeur')
            ligne.cmbChamp.setCurrentIndex(query.value('indiceChamp'))
            ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
            indiceChamp = query.value('indiceChamp')
            if indiceChamp == 0:  # Nom vidép
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(True)
                ligne.lneValeur.setText(query.value('textValeur'))
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 1:  # Dossier
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.clear()
                for itm in ligne.listValeur[indiceChamp]:
                    cle, nom = itm
                    ligne.cmbValeur.addItem(nom, cle)
                ligne.cmbValeur.setVisible(True)
                ligne.cmbValeur.setCurrentIndex(query.value('indiceValeur'))
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 2:  # Favori
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.clear()
                for itm in ligne.listValeur[indiceChamp]:
                    ligne.cmbValeur.addItem(itm)
                ligne.cmbValeur.setVisible(True)
                ligne.cmbValeur.setCurrentIndex(query.value('indiceValeur'))
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 3:  # Tag paragraph
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(True)
                ligne.lneValeur.setText(query.value('textValeur'))
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 4:  # création
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(True)
                annee, mois, jour = map(int, query.value('dateValeur').split('/'))
                date = QDate(annee, mois, jour)
                ligne.dateValeur.setDate(date)
            if indiceChamp == 5:  # Duration
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(True)
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(False)
                ligne.timeValeur.setVisible(True)
                timeAux = query.value('timeValeur')
                heure = timeAux // 3600
                timeAux -= heure * 3600
                minute = timeAux // 60
                timeAux -= minute * 60
                seconde = timeAux
                ligne.timeValeur.display(heure, minute, seconde)
            if indiceChamp == 6:  # Rating
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbValeur.clear()
                for itm in ligne.listValeur[indiceChamp]:
                    ligne.cmbValeur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(True)
                ligne.cmbValeur.setCurrentIndex(query.value('indiceValeur'))
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 7:  # dernier visionnage
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(True)
                annee, mois, jour = map(int, query.value('dateValeur').split('/'))

                date = QDate(annee, mois, jour)
                ligne.dateValeur.setDate(date)
            if indiceChamp == 8:  # statut (label)
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.clear()
                for itm in ligne.listValeur[indiceChamp]:
                    cle, nom, color = itm
                    pastille = self.drawPastille(6, color)
                    itemN = QListWidgetItem(nom)
                    itemN.setSizeHint(QSize(0, 20))
                    itemN.setText(f'     {nom}')
                    ligne.cmbValeur.addItem(QIcon(pastille), itemN.text())
                ligne.cmbValeur.setVisible(True)
                ligne.cmbValeur.setCurrentIndex(query.value('indiceValeur') - 1)
                ligne.lneValeur.setVisible(False)
                ligne.dateValeur.setVisible(False)
            if indiceChamp == 9:  # Note
                ligne.cmbOperateur.clear()
                for itm in ligne.listOperateur[indiceChamp]:
                    ligne.cmbOperateur.addItem(itm)
                ligne.cmbOperateur.setCurrentIndex(query.value('indiceOperateur'))
                ligne.cmbValeur.setVisible(False)
                ligne.lneValeur.setVisible(True)
                ligne.lneValeur.setText(query.value('textValeur'))
                ligne.dateValeur.setVisible(False)
        try:
            self.cadreBuildSearch.spacer.close()
        except:
            pass

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
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            del painter
        return pixmap


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        C A D R E B U I L D S E A R C H           ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class CadreBuildSearch(QMainWindow):
    def __init__(self, parent, contenant):
        super().__init__(parent)
        self.parent = parent
        self.contenant = contenant
        self.setStyleSheet('background-color: #444')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.listLineSavedSearch = []
        self.setupUI()

    def setupUI(self):
        # ***************************************************************************
        # contruction du scrollArea
        scrollArea = QScrollArea()
        scrollArea.setStyleSheet('border: 0px')
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.grp = QGroupBox(self)
        self.grp.setFixedWidth(708)
        self.grp.setFixedHeight(300)
        self.grp.setStyleSheet('border: 0px; background-color: #444')

        scrollArea.setWidget(self.grp)
        self.setCentralWidget(scrollArea)
        self.lytCadre = QVBoxLayout()
        self.grp.setLayout(self.lytCadre)

    def createLine(self):
        try:
            self.spacer.close()
        except:
            pass
        i = len(self.listLineSavedSearch)
        lbl = LineSavedSearch(self.grp, self)
        lbl.cleLigne = -1 #  ligne de requète créée - pas de clé attribuée
        self.listLineSavedSearch.append(lbl)
        self.lytCadre.addWidget(lbl)
        self.grp.setFixedHeight(i * 45 + 45)

    def deleteLine(self, lineCour):
        for line in self.listLineSavedSearch:
            if line == lineCour:
                self.listLineSavedSearch.remove(line)
                line.close()
        i = len(self.listLineSavedSearch)
        self.grp.setFixedHeight(i * 45)

    def clearLytCadre(self):
        while self.lytCadre.count():
            item = self.lytCadre.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clearLytCadre()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************             L I N E S A V E D S E A R C H        ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LineSavedSearch(QGroupBox):
    def __init__(self, parent, contenant):
        super().__init__(parent)
        self.parent = parent
        self.contenant = contenant
        self.setFixedSize(660, 35)
        self.setStyleSheet('background-color: #666; border: 1px solid #777; border-radius: 5px')
        self.critereCour = 0
        self.listOperateur = []
        self.cleRequete = 0
        self.cleLigne = 0
        self.cleValeur = 0

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.setupUI()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)


    def setupUI(self):
        # cmbChamp
        self.cmbChamp = QComboBox(self)
        self.cmbChamp.setFixedSize(150, 25)
        self.cmbChamp.view().setSpacing(1)
        f = open('styles/QComboBoxDegrade.txt', 'r')
        style = f.read()
        self.cmbChamp.setStyleSheet(style)
        self.cmbChamp.move(5, 5)
        self.cmbChamp.activated.connect(self.evt_cmbChamp_indexChanged)
        # cmbOperateur
        self.cmbOperateur = QComboBox(self)
        self.cmbOperateur.setFixedSize(150, 25)
        self.cmbOperateur.setStyleSheet(style)
        self.cmbOperateur.view().setSpacing(1)
        self.cmbOperateur.move(168, 5)
        # cmbValeur
        self.cmbValeur = QComboBox(self)
        self.cmbValeur.setFixedSize(240, 25)
        self.cmbValeur.view().setSpacing(1)
        self.cmbValeur.setStyleSheet(style)
        self.cmbValeur.move(330, 5)
        # lneValeur
        self.lneValeur = QLineEdit(self)
        self.lneValeur.setFixedSize(240, 25)
        self.lneValeur.setStyleSheet('border-radius: 4px; color: #333; background-color: #ddd')
        self.lneValeur.move(330, 5)
        #  DateValeur
        self.dateValeur = QDateEdit(self)
        self.dateValeur.setFixedSize(240, 25)
        self.dateValeur.setDate(date.today())
        self.dateValeur.setStyleSheet('border-radius: 4px; color: #333; background-color: #ddd')
        self.dateValeur.setCalendarPopup(True)
        self.dateValeur.move(330, 5)
        #  TimeValeur
        self.timeValeur = TimePickUp(self)
        self.timeValeur.move(330, 5)
        #  btPlus
        self.btnPlus = QPushButton(self)
        self.btnPlus.setText('+')
        self.font = QFont()
        self.font.setFamily('Abadi Extra Light')
        self.font.setPointSize(13)
        self.font.setBold(False)
        self.btnPlus.setFont(self.font)
        self.btnPlus.setFixedSize(25, 25)
        self.btnPlus.setStyleSheet('background-color: transparent; border: 1px solid #fff; border-radius: 6px; '
                                   'color: #fff')
        self.btnPlus.move(597, 5)
        self.btnPlus.clicked.connect(self.contenant.createLine)
        #  btMoins
        self.btnMoins = QPushButton(self)
        self.btnMoins.setText('-')
        self.btnMoins.setFont(self.font)
        self.btnMoins.setFixedSize(25, 25)
        self.btnMoins.setStyleSheet('background-color: transparent; border: 1px solid #fff; border-radius: 6px; '
                                    'color: #fff')
        self.btnMoins.move(630, 5)
        self.btnMoins.clicked.connect(lambda: self.contenant.deleteLine(self))

        self.initListeChamp()
        self.initLigne()

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
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            del painter
        return pixmap

    def initLigne(self):
        self.cmbOperateur.clear()
        self.cmbValeur.clear()
        self.lneValeur.setText('')
        #  *********************************************************************************
        if self.critereCour == 0:  # critère Nom

            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(True)
            self.dateValeur.setVisible(False)
            self.timeValeur.setVisible(False)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
        #  *********************************************************************************
        if self.critereCour == 1:  # critère Dossier
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            for itm in self.listValeur[self.critereCour]:
                cle, nom = itm
                self.cmbValeur.addItem(nom, cle)
            self.cmbValeur.setVisible(True)
            self.lneValeur.setVisible(False)
            self.timeValeur.setVisible(False)
            self.dateValeur.setVisible(False)
        #  *********************************************************************************
        if self.critereCour == 2:  # critère Favori
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(True)
            self.lneValeur.setVisible(False)
            self.dateValeur.setVisible(False)
            self.timeValeur.setVisible(False)
            for itm in self.listValeur[self.critereCour]:
                self.cmbValeur.addItem(itm)
        #  *********************************************************************************
        if self.critereCour == 3:  # critère Tag Paragraph
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(True)
            self.timeValeur.setVisible(False)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
            self.dateValeur.setVisible(False)
        #  *********************************************************************************
        if self.critereCour == 4:  # critère création
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(False)
            self.dateValeur.setVisible(True)
            self.timeValeur.setVisible(False)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
        #  *********************************************************************************
        if self.critereCour == 5:  # critère duration
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(False)
            self.dateValeur.setVisible(False)
            self.timeValeur.setVisible(True)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
        #  *********************************************************************************
        if self.critereCour == 6:  # Rating
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            for itm in self.listValeur[self.critereCour]:
                self.cmbValeur.addItem(itm)
            self.cmbValeur.setVisible(True)
            self.lneValeur.setVisible(False)
            self.timeValeur.setVisible(False)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
        #  *********************************************************************************
        if self.critereCour == 7:  # critère Dernier visionnage
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(False)
            self.dateValeur.setVisible(True)
            self.timeValeur.setVisible(False)
            self.lneValeur.setPlaceholderText(self._trad('Saisir le texte à rechercher', self.lngCourGlobal))
        #  *********************************************************************************
        if self.critereCour == 8:  # critère labels
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            self.cmbValeur.clear()
            for itm in self.listValeur[self.critereCour]:
                cle, nom, color = itm
                pastille = self.drawPastille(6, color)
                itemN = QListWidgetItem(nom)
                itemN.setSizeHint(QSize(0, 20))
                itemN.setText(f'    {nom}')
                self.cmbValeur.addItem(QIcon(pastille), itemN.text())
            self.cmbValeur.setVisible(True)
            self.lneValeur.setVisible(False)
            self.timeValeur.setVisible(False)
            self.dateValeur.setVisible(False)
        #  *********************************************************************************
        if self.critereCour == 9:  # notes
            for itm in self.listOperateur[self.critereCour]:
                self.cmbOperateur.addItem(itm)
            for itm in self.listValeur[self.critereCour]:
                cle, nom = itm
                self.cmbValeur.addItem(nom, cle)
            self.cmbValeur.setVisible(False)
            self.lneValeur.setVisible(True)
            self.timeValeur.setVisible(False)
            self.dateValeur.setVisible(False)


    def initListeChamp(self):
        #  ***************************************************************
        # Sélection d'un critère
        self.listChamp = ['Nom de la vidéo', 'Dossier', 'Favori', 'Tag paragraph', 'Création', 'Durée',
                          'Notation', 'Dernier visionnage', "Statut de la vidéo", "Note"]
        for itm in self.listChamp:
            self.cmbChamp.addItem(itm)
        self.cmbChamp.setCurrentIndex(0)
        #  ***************************************************************
        #  **************************************************************
        #  Liste des opérateurs pour chaque champ
        self.listOperateur = []
        listAux = [self._trad('Egal à', self.lngCourGlobal), self._trad('Diférent de', self.lngCourGlobal),
                   self._trad('Contient', self.lngCourGlobal),
                   self._trad('Ne contient pas', self.lngCourGlobal)]  # Nom de la vidéo
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Est présent dans', self.lngCourGlobal),
                   self._trad('Est absent dans', self.lngCourGlobal)]  # recherche dans les dossiers
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Est', self.lngCourGlobal), self._trad("N'est pas", self.lngCourGlobal)]  # Favori
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Egal à', self.lngCourGlobal), self._trad('Diférent de', self.lngCourGlobal),
                   self._trad('Contient', self.lngCourGlobal), self._trad('Ne contient pas', self.lngCourGlobal)]  # Tags paragraph
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Avant', self.lngCourGlobal), self._trad('Après', self.lngCourGlobal),
                   self._trad('Egal à', self.lngCourGlobal)]  # date de création
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Moins que', self.lngCourGlobal), self._trad('Plus que', self.lngCourGlobal),
                   self._trad('Egal à', self.lngCourGlobal)]  # Duration
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('PLus que', self.lngCourGlobal), self._trad('Moins que', self.lngCourGlobal),
                   self._trad('Egal à', self.lngCourGlobal)]  # Notation
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Avant', self.lngCourGlobal), self._trad('Après', self.lngCourGlobal),
                   self._trad('Egal à', self.lngCourGlobal)]  # date de modification
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Egal à', self.lngCourGlobal), self._trad('Différent de', self.lngCourGlobal)]  # Statut (label)
        self.listOperateur.append(listAux)
        #  **************************************************************
        listAux = [self._trad('Est présent dans', self.lngCourGlobal),
                   self._trad('Est absent dans', self.lngCourGlobal)]  # recherche dans les notes
        self.listOperateur.append(listAux)

        #  **************************************************************
        #  ***************************************************************
        #  Liste des valeurs pour chaque champ
        self.listValeur = []
        listAux = []  # Nom de la vidéo -> liste vide -> un lineEdit
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = []  # recherche dans les dossiers
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTreeTab')
        while query.next():
            listAux.append((query.value('cle'), query.value('data')))
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['Favori']  # Favori
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['Tag paragraph']  # Tag paragraph
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['Création']  # Création ---------- ajouter un widget pour saisir les dates
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['Modification']  # Modification ---------- ajouter un widget pour saisir les dates
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['0 étoile', '1 étoile', '2 étoiles', '3 étoiles', '4 étoiles', '5 étoiles']  # Notation
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = ['Dernier visionnage']  # Dernier visionnage ---------- ajouter un widget pour saisir les dates
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = []  # recherche dans les labels
        query = QSqlQuery()
        query.exec(f'SELECT * FROM statutTab')
        while query.next():
            listAux.append((query.value('cle'), query.value('nom'), query.value('color')))
        self.listValeur.append(listAux)
        #  **************************************************************
        listAux = []  # recherche dans les notes -> liste vide -> un lineEdit
        self.listValeur.append(listAux)
        #  **************************************************************

    def evt_cmbChamp_indexChanged(self):
        self.critereCour = int(self.cmbChamp.currentIndex())
        self.initLigne()


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

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

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
        self.lneTag.setPlaceholderText(self._trad('Saisir un tag ou cliquer sur la liste...', self.lngCourGlobal))
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
        return


    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def effaceTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = self._trad('Pas de tag sélectionné.', self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.dialog = DialogCustom(self)
        aux = self._trad('Vous êtes en train de supprimer les tags sélectionnés. '
                         '\nEtes-vous certain de votre choix ?', self.lngCourGlobal)
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)

        if self.dialog.exec_() == DialogCustom.Accepted:
            for tagAux in self.listTagSelect:
                self.listTag.remove(self.motCour)
                self.listTagSelect = []
                self.majMetaData()
        else:
            pass

    def modifTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = self._trad('Pas de tag sélectionné.', self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        if len(self.listTagSelect) > 1:
            self.dialog = DialogCustom(self, 0, 0)
            aux = self._trad("L'opération de modification ne s'applique\nqu'à un tag à la fois.", self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.motCour = self.listTagSelect[0].texte
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
            video = query.value('VideoFullPath')
        # with exiftool.ExifTool("exiftool.exe") as et:
        #     et.execute(f'-Comment={aux}', video)
        subprocess.run(["exiftool", f"-Comment={aux}".encode(), video])
        self.populateGrpBoxAffichTag()

    def sauverTag(self):
        mot = self.lneTag.text()
        if mot == '':
            return

        if mot in self.listTag and not self.boolModif:
            QMessageBox.information(self, self._trad('Enregistrement annulé', self.lngCourGlobal),
                                    self._trad('Le tag existe déja pour cette vidéo.', self.lngCourGlobal))
            return
        if self.boolModif:
            # del self.listTagSelect[self.listTagSelect.index(self.listTag[self.indexCour])]
            self.listTagSelect[0] = mot
            self.indexCour = self.listTag.index(self.motCour)
            self.listTag[self.indexCour] = mot
        else:
            self.listTag.append(mot)

        self.boolModif = False
        self.indexCour = -1
        self.listTagSelect = []
        self.majMetaData()
        # self.populateGrpBoxAffichTag()

    def populateGrpBoxAffichTag(self):
        # Effacer le contenu de lytAfichTag
        while 1:
            child = self.lytAffichTag.takeAt(0)
            if not child:
                break
            try:

                child.widget().deleteLater()
            except:
                pass

        for i in reversed(range(self.lytAffichTag.count())):
            widget = self.lytAffichTag.itemAt(i).widget()
            self.lytAffichTag.removeWidget(widget)
            widget.setParent(None)

        self.listTag = []
        #  Mise à jour de la listTag
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.videoID}')
        if query.next():
            video = query.value('VideoFullPath')

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
        # print(self.listTag)
        # return
        grpBox = QGroupBox()
        grpBox.setFixedHeight(1000)
        grpBox.setStyleSheet('border: 0px; background: #222')
        self.lytAffichTag.addWidget(grpBox)
        nbLigne = 0
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(grpBox, self, self.listTag[i], '#666666')
                # lblTag.installEventFilter(self)
                lblTag.setPosition(largLigneTag, nbLigne * 30)
                largLigneTag += lblTag.width + offSet
                if i + 1 == lenList:
                    self.lytAffichTag.addWidget(grpBox)
                    continuerLigne = False
                    continuerColonne = False
                    lblTag.setPosition(largLigneTag - lblTag.width - offSet, nbLigne * 30)
                else:
                    if largLigneTag > largeur - lblTag.width - offSet - 20:
                        largLigneTag = 0
                        lblTag.close()
                        nbLigne += 1
                        i -= 1
                        continuerColonne = False
                i += 1
        self.lneTag.setText('')



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
#  ***************  F O R M E D I T I O N V I D E O ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class FormEditionVideo(MainWindowCustom):
    def __init__(self, videoCour):
        super().__init__()
        self.setGeometry(200, 100, 910, 580)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.videoCour = videoCour
        self.videoRecordCour = VideoFileRecord(self.videoCour)
        self.setBtnMax(False)
        self.setBtnMini(False)
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
        lblClassement = QLabel(self)
        lblClassement.setText(self._trad('Classement', self.lngCourGlobal))
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
        self.btnInfoGene.setText(self._trad('Informations générales', self.lngCourGlobal))
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
        self.btnMatieres.setText(self._trad('Table des matières', self.lngCourGlobal))
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
        #  Les classeurs ne sont plus inclus dans l'appli
        # self.btnClasseurs = QPushButton(self)
        # self.btnClasseurs.setText('Classeurs')
        self.font1 = QFont()
        self.font1.setFamily('Arial')
        self.font1.setPointSize(12)
        self.font1.setBold(False)
        # self.btnClasseurs.setFont(self.font1)
        # self.btnClasseurs.setStyleSheet(self.styleDesabled)
        # self.btnClasseurs.setFixedSize(250, 35)
        # self.btnClasseurs.move(20, 205)
        # self.btnClasseurs.clicked.connect(self.evt_btnClasseurs_clicked)
        # self.lstMenu.append(self.btnClasseurs)

        #  Menu Labels
        self.btnLabels = QPushButton(self)
        self.btnLabels.setText(self._trad('Labels', self.lngCourGlobal))
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setPointSize(12)
        font1.setBold(False)
        self.btnLabels.setFont(font1)
        self.btnLabels.setStyleSheet(self.styleDesabled)
        self.btnLabels.setFixedSize(250, 35)
        self.btnLabels.move(20, 205)
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

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def evt_btnInfoGene_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == self._trad('Informations générales', self.lngCourGlobal):
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreInfoGene.setVisible(True)
        self.cadreTableMatiere.setVisible(False)
        # self.cadreClasseur.setVisible(False)
        self.cadreTag.setVisible(False)
        self.cadreLabel.setVisible(False)

    def evt_btnMatieres_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == self._trad('Table des matières', self.lngCourGlobal):
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(True)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(False)
        # self.cadreClasseur.setVisible(False)
        self.cadreLabel.setVisible(False)

    def evt_btnTags_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == self._trad('Tags', self.lngCourGlobal):
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
        self.cadreTableMatiere.setVisible(False)
        self.cadreInfoGene.setVisible(False)
        self.cadreTag.setVisible(True)
        # self.cadreClasseur.setVisible(False)
        self.cadreLabel.setVisible(False)

    def evt_btnClasseurs_clicked(self):
        for itm in self.lstMenu:
            if itm.text() == self._trad('Classeurs', self.lngCourGlobal):
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
            if itm.text() == self._trad('Labels', self.lngCourGlobal):
                itm.setStyleSheet(self.styleEnbled)
            else:
                itm.setStyleSheet(self.styleDesabled)
            self.cadreTableMatiere.setVisible(False)
            self.cadreInfoGene.setVisible(False)
            self.cadreTag.setVisible(False)
            # self.cadreClasseur.setVisible(False)
            self.cadreLabel.setVisible(True)

    def infoGeneUI(self):
        self.cadreInfoGene = QGroupBox(self)
        self.cadreInfoGene.setStyleSheet('background-color: #333333; color: white; border: 0px')
        self.cadreInfoGene.setFixedSize(600, 430)
        self.cadreInfoGene.move(300, 55)
        # titre
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setText(self._trad('Informations générales', self.lngCourGlobal))
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
        lblFavori.setText(self._trad('Favori', self.lngCourGlobal))
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
        lblTitre.setText(self._trad('Titre de la vidéo', self.lngCourGlobal))
        lblTitre.setFont(self.font1)
        lblTitre.move(2, 188)
        #  lblTitre vidéo
        self.lblTitreVideo = QLabel(self.cadreInfoGene)
        self.lblTitreVideo.setText(self._trad('Titre de la vidéo', self.lngCourGlobal))
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
        lblChemin.setText(self._trad('Chemin', self.lngCourGlobal))
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
        self.lblCheminVideo.setText(self.videoRecordCour.videoPath)
        self.lblCheminVideo.setToolTip(self.videoRecordCour.videoPath)
        self.pathVideo = self.videoRecordCour.videoPath
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
        lblDuree.setText(self._trad('Durée', self.lngCourGlobal))
        lblDuree.setFont(self.font1)
        lblDuree.move(2, 320)
        #  Durée vidéo
        self.lblDureeVideo = QLabel(self.cadreInfoGene)
        self.lblDureeVideo.setFixedSize(310, 30)
        self.lblDureeVideo.setText(str(self.videoDuration(self.videoRecordCour.videoPath)))
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
        lblStatut.setText(self._trad('Label de la vidéo', self.lngCourGlobal))
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
        lblClasseur.setText(self._trad('Dossier de la vidéo', self.lngCourGlobal))
        lblClasseur.setFont(self.font1)
        lblClasseur.move(2, 408)
        #  Dossier vidéo
        self.lblClasseurVideo = QLabel(self.cadreInfoGene)
        self.lblClasseurVideo.setFixedSize(310, 30)
        query = QSqlQuery()
        query.exec(f'SELECT data FROM biblioTreeTab WHERE cle={self.videoRecordCour.cleClasseur}')
        aux = ''
        if query.next():
            aux = query.value('data')
        self.lblClasseurVideo.setText(aux)
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
        lblTitre.setText(self._trad('Table des matières', self.lngCourGlobal))
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
            texte = query.value('texte')
            texte = texte.replace('$$', chr(32))
            texte = texte.replace(')|', chr(34))
            texte = texte.replace('µµ', chr(9))
            # lbl = LabelIndex(self.cadreTableMatiere, query.value('timeNote'), None, None, None)
            lbl = LabelData(self, query.value('timeNote'))
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
        timeNote = lbl.data
        query = QSqlQuery()
        query.exec(f'SELECT * from Paragraph where timeNote={timeNote}')
        if query.next():
            videoPath = self.videoRecordCour.videoPath
            videoId = self.videoRecordCour.cle
            marqueCour = query.value('TimeNote')
            boolCreer = False
            videoFullPath = self.videoRecordCour.videoPath
            formGererNote = FormBlockNote(self, videoFullPath, videoId, marqueCour, boolCreer)
            # formGererNote = FormGererNote(self, videoFullPath, videoId, marqueCour, boolCreer)
            formGererNote.show()

    def evt_btnAdmiSuppr2_clicked(self):
        lbl = self.sender().parent()
        clePagraph = lbl.index
        self.dialog = DialogCustom(self, 200, 200)
        aux = self._trad('Vous êtes en train de supprimer une note. '
                         '\nEtes-vous certain de votre choix ?', self.lngCourGlobal)
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
        lblTitre.setText(self._trad('Tags globaux', self.lngCourGlobal))
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
        return
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
        self.btnAnnulerClasseur.setStyleSheet(
            'QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
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
            aux = self._trad('Saisie du nom du label obligatoire.', self._trad())
            self.dialog.setMessage(aux)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
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
        lblAide.setText(self._trad('Aide', self.lngCourGlobal))
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
        aux = self._trad('Sélectionner le label de la vidéo', self.lngCourGlobal)
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
        lblAideValid.setText(self._trad('Sélectionner le label de la vidéo', self.lngCourGlobal))
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
        lblAidePlus.setText(self._trad('Ajouter un nouveau label.', self.lngCourGlobal))
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
        lblAideModif.setText(self._trad('Editer le label sélectionné', self.lngCourGlobal))
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
        lblAideSuppr.setText(self._trad('Supprimer le label sélectionné', self.lngCourGlobal))
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
        self.lblPlusLabel.setText(self._trad('Créer un nouveau label', self.lngCourGlobal))
        self.lblPlusLabel.setStyleSheet('color: white; border: 0px')
        self.lblPlusLabel.move(20, 25)
        self.grpCadrePlusLabel.setVisible(False)
        #  Titre plus Nom
        lblTitrePlusLabel = QLabel(self.grpCadrePlusLabel)
        lblTitrePlusLabel.setStyleSheet('QPushButton {background: transparent; color: white}')
        lblTitrePlusLabel.setText(self._trad('Nom et couleur du label', self.lngCourGlobal))
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
        lblTitrePlusLabel1.setText(self._trad('Note du label', self.lngCourGlobal))
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
        self.btnAnnulerLabel.setText(self._trad('Annuler', self.lngCourGlobal))
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
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
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
        aux = self._trad('Vous êtes en train de sélectionner un nouveau label.'
                         , self.lngCourGlobal)
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
        tptData = (self.videoRecordCour.statut, self.videoRecordCour.note, self.videoRecordCour.Favori,
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
        self.lblPlusLabel.setText(self._trad('Créer un nouveau label', self.lngCourGlobal))
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
        self.lblPlusClasseur.setText(self._trad('Modifier un classeur', self.lngCourGlobal))
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
        self.lblPlusLabel.setText(self._trad('Modifier un label', self.lngCourGlobal))
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
        self.lblPlusLabel.setText(self._trad('Supprimer un label', self.lngCourGlobal))
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
        aux = self._trad('Vous êtes en train de supprimer un label. \nEtes-vous certain de votre choix ?', self.lngCourGlobal)
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
            self.lblLabelCourant.setText(self._trad('Aucun label', self.lngCourGlobal))
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
# ***************            G R I D V I G N E T T E        ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class GridVignette(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint )
        self.setStyleSheet('background-color: #171717; border: 0px')
        self.lstVideo = []
        self.lstVignette1 = []


        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.initUI()
        self.indexCour = -1

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

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

                    # lbl.installEventFilter(self)
                    #  Mise à jour des vignettes marquées pour l'onglet
                    if self.lstVideo[index].cle in lstVignetteOnglet:
                        lbl.mousePressEventMethod()
                    # ****************************************************************
                    #  TITRE VIDEO
                    # ****************************************************************
                    lblTitre = QLabel(self.grpBox)
                    lblTitre.setWordWrap(False)

                    duree = self.videoDuration(f'{mainWindow.racine}{self.lstVideo[index].internalPath}'
                                               f'{self.lstVideo[index].videoName}')

                    aux = self.lstVideo[index].titreVideo.replace('$$', chr(10))
                    aux = aux.replace(')|', chr(34))  # guillements
                    aux = aux.replace('µµ', chr(9))  # Tabulation
                    # styleTitreVignet = 'color: #58595b; font-family: "Arial"; font-size: 14px; text-align: center!important;'
                    # styleTitreVignet = 'color: #58595b;'
                    # lblTitre.setFont(QFont('Arial', 10))
                    auxHTML = f'<p><FONT color="#a6a8ab"><FONT size=4>{aux}</FONT><br>Durée: {self.strTime(duree)}</p>'
                    # lblTitre.setAlignment(Qt.AlignCenter)
                    lblTitre.setText(auxHTML)
                    lblTitre.setToolTip(aux)
                    lblTitre.setStyleSheet(
                        "QToolTip { color: #ffffff; background-color: #333333; border: 1px solid #555555; }")

                    # lblTitre.setText(aux)
                    # lblTitre.setStyleSheet(styleTitreVignet)
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
        marge = (w - 4 * x - 2 * bord) // 3

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
            menu.addAction(QIcon('ressources/crayon.png'), self._trad('Mode édition', self.lngCourGlobal),
                           mainWindow.gridWindow.editVideo)  # self.editVideo)
            menu.addSeparator()
            menu.addAction(QIcon('ressources/voir.png'), 'Mode étude', self.modeEtude)  # self.etudeVideo)
            menu.addSeparator()
            if source.boolOnglet:
                menu.addAction(QIcon('ressources/onglet.png'), 'Voir les vidéo sélectionnées',
                               self.voirOnglets)  # mainWindow.evt_actEtudeVideo_clicked)
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
            mainWindow.btnPlusTab.move((125 * mainWindow.nbTab + 3), 2)
            mainWindow.btnPlusTab.setFont(QFont('Arial', 15))
            mainWindow.btnPlusTab.clicked.connect(mainWindow.evt_btnPlusTab_clicked)

        self.unsetCursor()

    def test(self):
        pass


# ********************************************************************************************************************
# *********************************************************************************************************************
# ***************            G R I D W I N D O W            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class GridWindow(QWidget):
    def __init__(self, parent, lstVideo):
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

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        return

        # ***************************************************************
        # ******  Initialisation nb ligne dans la grille
        # ***************************************************************
        self.nbRowGrid = 4
        self.statutCour = -1
        self.classeurCour = -1

        self.initUI1()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def initUI1(self):
        self.setStyleSheet('background-color: gray')
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
        if self.listSelectItem.currentIndex() == 0:  # Labels
            current_row = self.listItem.currentItem().data(Qt.UserRole)
            self.populateLabelsGrid(current_row)

        if self.listSelectItem.currentIndex() == 1:  # Classeurs
            current_row = self.listItem.currentItem().data(Qt.UserRole)
            self.populateClasseursGrid(current_row)

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

    def evt_lstClasseur_clicked(self):
        self.lneRecherche.setText('')
        itm = self.lstClasseur.currentItem()
        indexCour = itm.data(Qt.UserRole)
        self.classeurCour = indexCour
        listAux = [aux for aux in self.lstVideo if aux.cleClasseur == indexCour]
        self.frmPrecSuiv.initDataTab(listAux)

    #  Méthodes ** *****************************************************

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
                            lblVignette1.setPixmap(
                                pixmap01.scaled(192, 107, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                    query12 = QSqlQuery()
                    bOk = query12.exec(f'SELECT * FROM paragraph WHERE cleVideo={videoCleTest} AND titre=True '
                                       f'AND timeNote=0')
                    if query12.next():
                        titreAux = query12.value('texte')
                        titreAux = titreAux.replace('$$', chr(10))
                    #  Titre de la video
                    # toto = str(listAux[index].cle)
                    lblTitre1 = QLabel(titreAux)
                    lblTitre1.setWordWrap(False)
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
                    lblTitre1.setWordWrap(False)
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

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            self.sourceCour = source
            menu = QMenu()
            menu.addAction(self._trad('Mode édition', self.lngCourGlobal), self.editVideo)
            menu.addSeparator()
            menu.addAction(self._trad('Mode étude', self.lngCourGlobal), self.etudeVideo)
            menu.addSeparator()
            if source.boolOnglet:
                menu.addAction(self._trad('Voir les vidéos', self.lngCourGlobal), mainWindow.evt_actEtudeVideo_clicked)
            if menu.exec_(event.globalPos()):
                return True
        return super().eventFilter(source, event)

    def editVideo(self):
        try:
            self.formListVideo.close()
        except:
            pass
        self.formEditionVideo = FormEditionVideo(self.gridVignette.sourceCour.index)
        self.formEditionVideo.show()

    def etudeVideo(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = GridWindow()
    mainWindow.show()
    sys.exit(app.exec_())

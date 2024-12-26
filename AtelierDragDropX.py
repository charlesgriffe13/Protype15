import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
# from PyQt5.QtWebEngineWidgets import *
import sys
from PyQt5.QtSql import QSqlDatabase
import sqlite3
from PyQt5.QtSql import *
from AtelierClassCommun import DialogCustom, VideoFileRecord
import datetime
import os


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        D I A L O G D O S S I E R                 ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class DialogDossier(QDialog):
    def __init__(self, parent=None, modif=None, cleCreate=None, contenant=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.parent = parent
        self.modif = modif
        self.contenant = contenant

        button_global_pos = self.parent.mapToGlobal(QPoint(0, 0))

        x = button_global_pos.x() + self.parent.width() + 10
        y = button_global_pos.y()

        self.setGeometry(x, y, 300, 150)
        self.setStyleSheet('background-color: #333333')
        self.cleDossierCour = cleCreate
        self.returnCmb = True
        #
        self.setUpUI()

    def setUpUI(self):
        lblNom = QLabel(self)
        lblNom.setText('Nom :')
        lblNom.setStyleSheet('color: white')
        lblNom.move(25, 23)
        #
        self.lneNom = QLineEdit(self)
        self.lneNom.setFixedSize(220, 25)
        self.lneNom.setPlaceholderText('Saisir le nom du dossier')
        self.lneNom.setStyleSheet('color: #cccccc')
        self.lneNom.move(70, 20)
        if self.modif:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM biblioTreeTab WHERE cle={self.cleDossierCour}')
            if query.next():
                self.lneNom.setText(query.value('data'))
        #
        lblParent = QLabel(self)
        lblParent.setText('Parent :')
        lblParent.setStyleSheet('color: white')
        lblParent.move(15, 63)
        #
        self.cmbParent = QComboBox(self)
        self.cmbParent.setFixedSize(220, 25)
        self.cmbParent.setStyleSheet('color: #cccccc')
        self.cmbParent.move(70, 63)
        self.cmbParent.currentIndexChanged.connect(self.handleIndexChanged)
        self.populateParent()
        #
        btnSauver = QPushButton(self)
        btnSauver.setFixedSize(110, 35)
        btnSauver.setText('Sauver')
        btnSauver.setStyleSheet('color: white; background-color: #3a67ae')
        btnSauver.move(25, 110)
        btnSauver.clicked.connect(self.evt_btnSauver_clicked)
        #
        btnFermer = QPushButton(self)
        btnFermer.setFixedSize(110, 35)
        btnFermer.setText('Fermer')
        btnFermer.setStyleSheet('color: white; background-color: #3a67ae')
        btnFermer.move(175, 110)
        btnFermer.clicked.connect(self.evt_btnFermer_clicked)

    def populateParent(self):
        self.returnCmb = True
        self.cmbParent.clear()
        query = QSqlQuery()
        query.exec('SELECT * FROM biblioTreeTab')
        dataAux = ''
        while query.next():
            self.cmbParent.addItem(query.value('data'), userData=query.value('cle'))
            if query.value('cle') == self.cleDossierCour:
                dataAux = query.value('data')
        # self.cleDossierCour -= 1
        self.cmbParent.setCurrentIndex(self.cleDossierCour - 1)
        self.returnCmb = False

    def handleIndexChanged(self, index):
        if self.returnCmb:
            return
        self.cleDossierCour = self.cmbParent.itemData(index)

    def evt_btnSauver_clicked(self):
        if self.lneNom.text() == '':
            return
        if self.modif:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM biblioTreeTab WHERE cle={self.cleDossierCour}')
            parent_idAux = ''
            if query.next():
                parent_idAux = query.value('parent_id')
            query = QSqlQuery()
            tplChamps = ('parent_id', 'data')
            tplData = (parent_idAux, self.lneNom.text())
            query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle={self.cleDossierCour}')
        else:
            #  Recherche de l'index suivant
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM biblioTreeTab')
            try:
                if query.next():
                    cleMax = query.value('cleMax') + 1
            except:
                pass

            tplData = (cleMax, self.cleDossierCour, self.lneNom.text())
            tplChamps = ('cle', 'parent_id', 'data')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO biblioTreeTab {tplChamps} VALUES {tplData}')
        self.contenant.refreshTree()
        self.close()

    def evt_btnFermer_clicked(self):
        self.close()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                 T R E E N O D E                  ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TreeNode:
    def __init__(self, node_id, parent_id, data, boolDev):
        self.cle = node_id
        self.lstChildren = []
        self.data = data
        self.parent_id = parent_id
        self.boolDev = boolDev

    def __str__(self):
        aux = f'cle: {self.cle} - data: {self.data} - parent: {self.parent_id} - boolDev: {self.boolDev}'
        return aux


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************       M A I N W I N D O W D O S S I E R          ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainWindowDossier(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.dragCour = None
        self.listWidget = []

        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #222')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.grpTree = QGroupBox()
        self.grpTree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grpTree.setStyleSheet('background-color: #222')
        self.grpTree.setFixedSize(300, 600)
        self.grpTree.move(0, 0)

        #  Menu contextuel
        self.grpTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.grpTree.customContextMenuRequested.connect(self.showMenuContextuel0)

        self.loadListTree()

        #  Installation d'un ScrollArea
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.grpTree)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        centralLayout = self.setCentralWidget(self.scrollArea)
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        self.scrollArea.setStyleSheet(style)
        self.setStyleSheet('background-color: #222222; border: 0px')

    def showMenuContextuel0(self):
        pass

    def refreshTree(self):
        self.grpTree.close()
        # self.scrollArea

        self.grpTree = QGroupBox(self)
        self.grpTree.setStyleSheet('background-color: #222')
        self.grpTree.setGeometry(0, 0, 300, 600)

        self.loadListTree()
        self.grpTree.show()

        #  Installation d'un ScrollArea
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.grpTree)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        centralLayout = self.setCentralWidget(self.scrollArea)
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        self.scrollArea.setStyleSheet(style)
        self.setStyleSheet('background-color: #222222; border: 0px')

    def loadListTree(self):
        self.listTree = []
        self.listWidget = []
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM biblioTreeTab ORDER BY cle')
        while query.next():
            cle = query.value('cle')
            parent_id = query.value('parent_id')
            data = query.value('data')
            node = TreeNode(cle, parent_id, data, query.value('boolDev'))
            self.listTree.append(node)


        for node in self.listTree:
            lstChildren = [itm.cle for itm in self.listTree if itm.parent_id == node.cle]
            node.lstChildren = lstChildren

        #  tri de la liste par ordre de cle
        self.listTree = sorted(self.listTree, key=lambda x: x.cle)

        listEtage = []
        for node in self.listTree:
            if len(node.lstChildren) > 0:
                if node not in listEtage:
                    listEtage.append(node)
                indice = listEtage.index(node)
                for itm in node.lstChildren:
                    indice += 1
                    nodeChild = [node for node in self.listTree if node.cle == itm][0]
                    listEtage.insert(indice, nodeChild)

        self.listTree = listEtage

        if len(listEtage) == 0:
            query = QSqlQuery()
            query.exec(f'SELECT data FROM biblioTreeTab')
            if query.next():
                nodeAux = TreeNode(1, -1, query.value('data'), True)
                listEtage.append(nodeAux)

        try:
            self.indice = 0
            self.listWidget = []
            self.displayTree(listEtage[0])
        except:
            pass

    def unSelectBtnSelect(self):
        for obj in self.listWidget:
            obj.selectVert = False
            obj.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                              'QLabel::hover {background-color: #444}')
        self.parent.dossierSelectCour = -1

    def displayTree(self, root, indent=''):
        if True:  # os.path.isdir(root) -> cas répertoires + fichiers
            lblNode = DraggableWidget(self.grpTree, self, root)
            self.listWidget.append(lblNode)

            lblNode.contenant = self
            lblNode.move(len(indent) * 12 + 10, self.indice * 40 + 20)

            lblNode.setFixedWidth(lblNode.width() - lblNode.x())
            lblNode.posInit = (len(indent) * 12 + 10, self.indice * 30)

            items = root.lstChildren
            if len(items) == 0:
                lblNode.btDeveloppe.setVisible(False)
            else:
                for item in items:
                    nodeChild = [node for node in self.listTree if node.cle == item][0]
                    if True:  # os.path.isdir(item_path)  -> cas répertoires + fichiers
                        if root.boolDev:
                            self.indice += 1
                            self.displayTree(nodeChild, indent + "  ")
                else:
                    pass
                    return
                    print(indent * 3 + f"  📄 {item}")
        self.grpTree.setFixedHeight((self.indice + 1) * 80)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************         D R A G G A B L E W I D G E T            ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class DraggableWidget(QLabel):
    def __init__(self, parent, contenant, node):
        super().__init__(parent)
        self.setFixedSize(300, 30)
        self.setStyleSheet('QLabel {background-color: #222; border: 0px; color: gray} '
                           'QLabel::hover {background-color: #444}')
        self.installEventFilter(self)
        self.parent = parent
        self.contenant = contenant
        self.node = node
        self.selectVert = False
        #  Icone du dossier
        pixmap = QPixmap('ressources/dossier25.png')
        pixmapLabel = QLabel(self)
        pixmapLabel.setPixmap(pixmap)
        pixmapLabel.move(30, 5)
        #  Fléche de développement
        self.btDeveloppe = QPushButton(self)
        self.btDeveloppe.setFixedSize(20, 20)
        self.btDeveloppe.setStyleSheet('background-color: transparent')
        if self.node.boolDev:
            self.btDeveloppe.setIcon(QIcon('ressources/devPlus.png'))
        else:
            self.btDeveloppe.setIcon(QIcon('ressources/devMoins.png'))
        self.btDeveloppe.move(0, 10)
        self.btDeveloppe.clicked.connect(self.evt_btDeveloppe_clicked)
        #  Data du treeNode
        titreLabel = QLabel(self)
        titreLabel.setStyleSheet('background-color: transparent; color: white')
        titreLabel.setText(node.data)
        titreLabel.move(65, 7)

        #  Rendre le widget glissable
        self.setAcceptDrops(True)
        self.contenant.dragCour = self

    def evt_btDeveloppe_clicked(self):
        #  Swap développé / non développé
        sender = self.sender()
        cle = sender.parent().node.cle
        if sender.parent().node.boolDev:
            sender.parent().node.boolDev = False
            sender.parent().btDeveloppe.setIcon(QIcon('ressources/devMoins.png'))
        else:
            sender.parent().node.boolDev = True
            sender.parent().btDeveloppe.setIcon(QIcon('ressources/devPlus.png'))
        #  Enregistrement dans la table du statut du noeud (développé / non développé)
        query = QSqlQuery()
        tplChamps = ('boolDev')
        tplData = (sender.parent().node.boolDev)
        query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
        #
        self.contenant.refreshTree()

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.RightButton):
            menu = QMenu()
            menu.setStyleSheet('background-color: #aaa; border: 1px solid #aaaaaa')
            menu.addAction('Créer nouveau dossier', lambda:  self.createSousDossier(self.cleCreate))
            if object.node.parent_id != -1:
                menu.addAction('Supprimer  dossier', lambda: self.supprSousDossier(self.cleCreate))
            menu.addAction('Renommer  dossier', lambda: self.renommerDossier(self.cleCreate))
            menu.addAction('Importer un dossier',  lambda:  self.importerDossier(self.cleCreate))
            if menu.exec_(event.globalPos()):
                return True
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            # self.parent.boolExecuterSearch = False
            self.evt_btnSelect_clicked()
        if event.type() == QEvent.Enter:
            self.cleCreate = object.node.cle
        if event.type() == QEvent.Leave:
            pass
        if event.type() == QEvent.Drop:
            # if object.node.parent_id != -1:
            #     return
            cleTarget = object.node.cle
            auxVideo = VideoFileRecord(cleTarget)
            aux = str(type(self.contenant.dragCour))
            if 'DraggableWidget' in aux and not event.mimeData().hasUrls():
                cleDrag = self.contenant.dragCour.node.cle
                auxVideo = VideoFileRecord(cleTarget)
                #  Mise à jour de la base de données puis l'affichage de l'arbre modifié
                query = QSqlQuery()
                tplChamps = ('parent_id')
                tplData = (cleTarget)
                if cleDrag != cleTarget:  # cas du dossier déplacé sur lui-même
                    query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle = {cleDrag}')
                    self.contenant.refreshTree()
            if 'LabelIndex' in aux:
                cleVideo = self.contenant.dragCour.index
                auxVideo = VideoFileRecord(cleVideo)
                if auxVideo.deleted:  # déplacement d'une vidéo dans la corbeille dans un dossier
                    query =QSqlQuery()
                    tplChamps = ('cleClasseur', 'deleted')
                    tplData = (cleTarget, False)
                    query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle={cleVideo}')
                    self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
                else:  # autres cas de déplacement de vidéos d'un dossier à un autre
                    self.dropVideoGridDossier(cleTarget)

            if event.mimeData().hasUrls():  # Cas d'un drag and drop d'un fichier
                aux = event.mimeData().urls()[0].toLocalFile()
                videoFullPath = aux
                videoName = os.path.splitext(os.path.basename(aux))[0] + os.path.splitext(os.path.basename(aux))[1]
                cleClasseur = cleTarget
                date_du_jour = datetime.date.today()
                dateLastView = date_du_jour.strftime("%d-%m-%Y")
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut')
                statut = 0
                if query.next():
                    statut = query.value('cle')
                    aux = f"- {query.value('nom')}"
                favori = False
                #  Vérifier que la vidéo ne figure pas déja dans la base
                query = QSqlQuery()
                bOk = query.exec(f'SELECT * From videoFileTab')
                lst = []
                while query.next():
                    lst.append(query.value('videoFullPath'))
                if aux in lst:
                    self.dialog = DialogCustom(None, 500, 500)
                    aux = 'La vidéo figure déja dans la base de données.'
                    self.dialog.setSaisie('', False)
                    self.dialog.setMessage(aux)
                    self.dialog.setBouton1('', False)
                    self.dialog.setBouton2('Fermer', True)
                    if self.dialog.exec_() == DialogCustom.Accepted:
                        pass
                else:
                    #  recherche de l'indice suivant
                    query = QSqlQuery()
                    bOk = query.exec(f'SELECT MAX(cle) FROM videoFileTab')
                    maxCle = 1
                    try:
                        if bOk:
                            if query.next():
                                maxCle = query.value(0) + 1
                    except:
                        pass
                    #  Last view
                    dateCreation = QDate.currentDate()
                    dateCreationString = dateCreation.toString('yyyy-MM-dd')
                    dateLastView = dateCreationString
                    #  Duration
                    v = cv2.VideoCapture(videoFullPath)
                    fps = v.get(cv2.CAP_PROP_FPS)
                    frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = int(frame_count/fps)
                    tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'dateLastView', 'statut', 'favori',
                                 'deleted', 'cle', 'dateCreation', 'duration')
                    tplData = (videoName, videoFullPath, cleClasseur, dateLastView, statut, favori, False, maxCle,
                               dateCreationString, duration)
                    query = QSqlQuery()

                    query.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')
                    self.dialog = DialogCustom(None, 500, 500)
                    aux = 'La vidéo a été enregistrée.'
                    self.dialog.setSaisie('', False)
                    self.dialog.setMessage(aux)
                    self.dialog.setBouton1('', False)
                    self.dialog.setBouton2('Fermer', True)
                    if self.dialog.exec_() == DialogCustom.Accepted:
                        pass

            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        return super().eventFilter(object, event)

    def mousePressEvent(self, event):
        self.contenant.dragCour = self
        #  Commencer le processus de glissement
        mimeData = QMimeData()
        mimeData.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def importerDossier(self, cleDossier):
        directory = QFileDialog.getExistingDirectory(self, "Select directory")
        if directory:
            self.importArbre(directory, cleDossier)

    def importArbre(self, directory, cleDossier):
        listDir = []  # Liste des répertoires de l'arborescence à importer
        listDossier = []  # Liste des noeuds de l'arbre à importer
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                listDir.append(os.path.join(root, dir))
        cleCour = 0
        listAuxPath = []  #  Liste intermédiaire pour construire listDossier
        for dir in listDir:
            cleCour += 1
            dirName = os.path.basename(os.path.join(root, dir))
            dirPath = os.path.dirname(os.path.join(root, dir))
            dirPath = dirPath.replace(chr(47), '$')
            dirPath = dirPath.replace(chr(92), '$')
            fullPath = os.path.realpath(os.path.join(root, dir))
            fullPath = fullPath.replace(chr(47), '$')
            fullPath = fullPath.replace(chr(92), '$')
            listAuxPath.append((fullPath, dirPath, dirName, cleCour))
            #
            listFullPath = [full for (full, path, name, cle) in listAuxPath]
            #  Recherche du cleMax pour brancher l'arborescence sur la table biblioTreeTab
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM videoFileTab')
            try:
                if query.next():
                    cleMax = query.value('cleMax')
            except:
                pass
            if dirPath not in listFullPath:
                nodeAux = TreeNode(node_id=cleCour + cleMax, parent_id=cleDossier, data=dirName, boolDev=True)
                listDossier.append(nodeAux)
            else:
                cleParent = listFullPath.index(dirPath)
                nodeAux = TreeNode(node_id=cleCour + cleMax, parent_id=cleParent + cleMax, data=dirName, boolDev=True)
                listDossier.append(nodeAux)

        #  Enregistrer l'arbre importé dans la table biblioTreeTab
        for node in listDossier:
            tplData = (node.cle, node.parent_id, node.data)
            tplChamps = ('cle', 'parent_id', 'data')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO biblioTreeTab {tplChamps} VALUES {tplData}')
        self.contenant.refreshTree()

    def dropVideoGridDossier(self, cleDossier):
        cursor = QCursor()
        x_pos = cursor.pos().x()
        y_pos = cursor.pos().y()
        #  boite de dialogue menu
        self.dialMenuDrop = QDialog()
        self.dialMenuDrop.setStyleSheet('background-color: #333; border: 1px solid #555')
        self.dialMenuDrop.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.dialMenuDrop.setGeometry(x_pos, y_pos, 200, 100)
        self.dialMenuDrop.setFixedSize(200, 100)
        self.dialMenuDrop.show()
        lytMenu = QVBoxLayout()
        lytMenu.setSpacing(0)
        self.dialMenuDrop.setLayout(lytMenu)
        # QListWidget
        self.listMenuDrop = QListWidget()
        self.listMenuDrop.setStyleSheet('background-color: #333; color: #999; border: 0px;')
        self.listMenuDrop.addItem("Déplacer la vidéo")
        self.listMenuDrop.addItem("Copier la vidéo")
        self.listMenuDrop.addItem("Annuler")
        lytMenu.addWidget(self.listMenuDrop)
        self.listMenuDrop.currentItemChanged.connect(lambda: self.evt_listMenuDrop_currentItemChanged(cleDossier))

    def evt_listMenuDrop_currentItemChanged(self, cleDossier):
        indice = self.listMenuDrop.currentRow()
        if indice == 0:  # déplacer la vidéo
            query = QSqlQuery()
            tplChamps = ('cleClasseur')
            tplData = (cleDossier)
            query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle={self.contenant.dragCour.index}')
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        if indice == 1:  # copier la vidéo
            vAux = VideoFileRecord(self.contenant.dragCour.index)
            #  Recherche de l'index suivant
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM videoFileTab')
            try:
                if query.next():
                    cleMax = query.value('cleMax') + 1
            except:
                pass

            tplData = (vAux.videoName, vAux.videoPath, cleDossier, vAux.ordreClasseur, vAux.marquePage, cleMax,
                       vAux.dateLastView, vAux.statut, vAux.Favori, vAux.internalPath, vAux.cleBiblio, vAux.note,
                       vAux.deleted)
            tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'ordreClasseur', 'marquePage', 'cle',
                         'DateLastView', 'statut', 'Favori', 'internalPath', 'cleBiblio', 'note', 'deleted')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')

        if indice == 2:
            self.dialMenuDrop.close()
        self.dialMenuDrop.close()

    def evt_btnMenu_clicked(self):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))
        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        #  Affichage d'un menu dans un QListWidget dans un QDialog
        self.dialMenu = QDialog()
        self.dialMenu.setStyleSheet('background-color: #333; border: 1px solid #555')
        self.dialMenu.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.dialMenu.setGeometry(x, y, 200, 150)
        self.dialMenu.show()
        lytMenu = QVBoxLayout()
        self.dialMenu.setLayout(lytMenu)
        #  QListWidget
        self.listMenu = QListWidget()
        self.listMenu.setStyleSheet('background-color: #333; color: #999; border: 0px')
        self.listMenu.addItem('Créer nouveau dossier')
        self.listMenu.addItem('Supprimer dossier')
        self.listMenu.addItem('Renommer dossier')
        self.listMenu.addItem('Annuler...')
        lytMenu.addWidget(self.listMenu)
        self.listMenu.currentItemChanged.connect(self.evt_listMenu_currentItemChanged)
        self.contenant.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_btnSelect_clicked(self):
        #  Déselectionner les bouton TopLeft + savedSearch
        self.contenant.parent.selectZoneGauche.unSelectTopLeft()
        self.contenant.parent.boolExecuterSearch = False
        self.contenant.parent.selectZoneGauche.lblSavedSearch.setSelected(False)
        #
        sender = self.sender()
        for obj in self.contenant.listWidget:
            obj.selectVert = False
            obj.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')

        if self.selectVert:
            self.selectVert = False
            self.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')
            self.contenant.parent.dossierSelectCour = 0
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        else:
            self.contenant.parent.dossierSelectCour = self.node.cle
            self.selectVert = True
            self.setStyleSheet('QLabel {background-color: #395da4; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_listMenu_currentItemChanged(self, current):
        indice = self.listMenu.currentRow()
        if indice == 0:
            # self.parent.parent().parent().createSousDossier(self.cleCreate)
            self.createSousDossier(self.cleCreate)
        if indice == 1:
            self.supprSousDossier(self.cleCreate)
        if indice == 2:
            self.renommerDossier(self.cleCreate)
        if indice == 3:
            self.dialMenu.close()
        self.dialMenu.close()
        # self.parent.parent().setFocus(True)
        self.contenant.setFocus(True)

    def createSousDossier(self, cleCreate):
        dialogDossier = DialogDossier(self, modif=False, cleCreate=cleCreate, contenant=self.contenant)
        dialogDossier.show()

    def supprSousDossier(self, cleCreate):
        self.dialog = DialogCustom(None, 500, 500)
        aux = 'Vous êtes en train de supprimer un nouvelle dossier. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Mise à jour des vidéos concernées par le dossier à supprimer
            query = QSqlQuery()
            tplChamps = ('cleClasseur', 'deleted')
            tplData = (-1, True)
            query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cleClasseur={cleCreate}')
            #  Suppression du dossier
            query = QSqlQuery()
            query.exec(f'DELETE FROM biblioTreeTab WHERE cle={cleCreate}')
            self.contenant.refreshTree()

    def renommerDossier(self, cleCreate):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))

        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        dialogDossier = DialogDossier(self, modif=True, cleCreate=cleCreate, contenant=self.contenant)
        dialogDossier.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowDossier()
    mainWindow.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
# from PyQt5.QtWebEngineWidgets import *
import sys
from PyQt5.QtSql import QSqlDatabase
import sqlite3
from PyQt5.QtSql import *
import os

class TreeNode:
    def __init__(self, node_id, parent_id, data):
        self.cle = node_id
        self.lstChildren = []
        self.data = data
        self.parent_id = parent_id


class DragLabel(QLabel):
    def __init__(self, parent, node):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(350, 25)
        self.setStyleSheet('background-color: transparent')
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.node = node
        self.contenant = None

        self.boolDrag = False
        self.cleCreate = -1
        #
        pixmap = QPixmap('ressources/dossier25.png')
        pixmapLabel = QLabel(self)
        pixmapLabel.setPixmap(pixmap)
        pixmapLabel.move(0, 0)
        #
        textLabel = QLabel(self)
        textLabel.setText(node.data)
        textLabel.setStyleSheet('color: white')
        textLabel.move(30, 0)
        # Installation du drag and drop
        self.setAcceptDrops(True)
        self.installEventFilter(self)
        #  Installation du bouton menu
        self.btnMenu = QPushButton(self)
        self.btnMenu.setText('...')
        self.btnMenu.setFixedSize(25, 25)
        self.btnMenu.setStyleSheet('background-color: transparent; border-radius: 6px; '
                                   'border: 1px solid gray; color: gray')
        self.btnMenu.setCursor(Qt.PointingHandCursor)
        self.btnMenu.setVisible(False)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.btnMenu.setFont(font)
        # Crée un menu contextuel
        self.btnMenu.clicked.connect(self.evt_btnMenu_clicked)
        # textLabel.mousePressEvent = lambda e, label=textLabel: self.mousePressEvent(e, label)

    def evt_btnMenu_clicked(self, event):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))
        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        #  Affichage d'un menu dans un QListWidget dans un QDialog
        #  QDialog
        self.dialMenu = QDialog()
        self.dialMenu.setWindowFlags(Qt.FramelessWindowHint)
        self.dialMenu.setFixedSize(200, 120)
        # self.dialMenu.setStyleSheet('background-color: orange')
        self.dialMenu.setGeometry(x, y, 150, 150)
        self.dialMenu.show()
        lytMenu = QVBoxLayout()
        self.dialMenu.setLayout(lytMenu)
        #  QListWidget
        self.listMenu = QListWidget()
        self.listMenu.addItem('Créer nouveau dossier')
        self.listMenu.addItem('Supprimer dossier')
        self.listMenu.addItem('Renommer dossier')
        self.listMenu.addItem('Annuler...')
        lytMenu.addWidget(self.listMenu)
        self.listMenu.currentItemChanged.connect(self.evt_listMenu_currentItemChanged)

    def evt_listMenu_currentItemChanged(self, current):
        indice = self.listMenu.currentRow()
        if indice == 0:
            # self.parent.parent().parent().createSousDossier(self.cleCreate)
            self.contenant.createSousDossier(self.cleCreate)
        if indice == 1:
            self.contenant.supprSousDossier(self.cleCreate)
        if indice == 2:
            self.contenant.renommerDossier(self.cleCreate)
        if indice == 3:
            self.dialMenu.close()
        self.dialMenu.close()
        # self.parent.parent().setFocus(True)
        self.contenant.setFocus(True)

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            self.btnMenu.setVisible(True)
            self.cleCreate = object.node.cle
        if event.type() == QEvent.Leave:
            self.btnMenu.setVisible(False)
        if event.type() == QEvent.Drop:
            self.setAcceptDrops(True)
            self.cleTarget = object.node.cle
            # print(object.node.cle)
            #  Mise à jour de la base de donnée puis de l'affichage de l'arbre
            query = QSqlQuery()
            tplChamps = ('parent_id')
            tplData = (self.cleTarget)
            # print(self.cleTarget, self.contenant.cleDrag)
            if self.cleTarget != self.contenant.cleDrag: #  cas d'un dossier déplacé sur lui même
                query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle={self.contenant.cleDrag}')
            self.contenant.refreshTree()
        if event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton:
            # self.setAcceptDrops(True)
            self.contenant.cleDrag = object.node.cle
            pass
        if event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.RightButton:
            return True
        return super().eventFilter(object, event)

    def dragEnterEvent(self, e):
        # Événement lorsqu'un fichier est glissé sur le widget
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        return
        files = e.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            print(f"Fichier glissé et déposé : {file_path}")

    def mousePressEvent(self, e, label):
        # return
        # print(label.text())
        mime_data = QMimeData()
        mime_data.setText(self.node.data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.CopyAction)


class DialogDossier(QDialog):
    def __init__(self, parent=None, modif=None, cleCreate=None):
        super().__init__(parent)
        self.parent = parent
        self.modif = modif
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
        self.cmbParent.setCurrentIndex(self.cleDossierCour-1)
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
        self.parent.refreshTree()
        self.close()

    def evt_btnFermer_clicked(self):
        self.close()


class MainWindowTree(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 600)
        # self.setStyleSheet('background-color: #333333')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.listTree = []
        self.cleDossierCour = 0
        self.cleDrag = None

        self.listColor = ['red', 'yellow', 'green', 'blue', 'pink', 'gray', 'orange', 'teal', 'purple', 'indigo']
        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            query = QSqlQuery()
            bOk = query.exec(f'SELECT * FROM biblioTreeTab')

        #  Création de la zone Centrale pour le ScrollArea
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.grpTree = QGroupBox()
        self.grpTree.setStyleSheet('background-color: #333333')
        self.grpTree.setFixedSize(400, 600)
        self.grpTree.move(0, 0)

        self.setAcceptDrops(True)

        #  Menu contextuel
        self.grpTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.grpTree.customContextMenuRequested.connect(self.showMenuContextuel0)

        self.loadListTree()

        # #  Installation d'un QScrollBar
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.grpTree)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0, 0, 0, 0)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        centralLayout = self.setCentralWidget(scrollArea)
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        styleQGroupBox = style
        scrollArea.setStyleSheet(styleQGroupBox)

    def loadListTree(self):
        self.listTree = []
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM biblioTreeTab ORDER BY cle')
        while query.next():
            cle = query.value('cle')
            parent_id = query.value('parent_id')
            data = query.value('data')
            node = TreeNode(cle, parent_id, data)
            self.listTree.append(node)

        for node in self.listTree:
            lstChildren = [itm.cle for itm in self.listTree if itm.parent_id == node.cle]
            node.lstChildren = lstChildren

        #  tri de la liste par ordre de cle
        self.listTree = sorted(self.listTree, key=lambda x: x.cle)
        # for itm in self.listTree:
        #     print(itm.data, itm.cle, itm.lstChildren)

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

        # for itm in listEtage:
        #     print(itm.cle, itm.data, self.listTree.index(itm))

        if len(listEtage) == 0:
            query = QSqlQuery()
            query.exec(f'SELECT data FROM biblioTreeTab')
            if query.next():
                nodeAux = TreeNode(1, -1, query.value('data'))
                listEtage.append(nodeAux)
        try:
            self.indice = 0
            self.displayTree(listEtage[0])
        except:
            pass
        # self.refreshTree()

    def displayTree(self, root, indent=''):
        if True:  # os.path.isdir(root) -> cas répertoires + fichiers
            lblNode = DragLabel(self.grpTree, root)
            lblNode.contenant = self

            # indice = self.listTree.index(root)

            lblNode.move(len(indent)*6 + 10, self.indice*30+20)
            lblNode.posInit = (len(indent)*6 + 10, self.indice*30)
            lblNode.setFixedWidth(lblNode.width() - lblNode.x())
            lblNode.btnMenu.move(lblNode.width()-25, 0)
            items = root.lstChildren
            for item in items:
                nodeChild = [node for node in self.listTree if node.cle == item][0]
                if True:  # os.path.isdir(item_path)  -> cas répertoires + fichiers
                    self.indice += 1
                    self.displayTree(nodeChild, indent + "    ")
                else:
                    print(indent*3 + f"  📄 {item}")

    def showMenuContextuel0(self, pos):
        query = QSqlQuery()
        query.exec('SELECT * FROM biblioTreeTab')
        if query.next():  # cas de la table non vide
            return
        contextMenu = QMenu(self.grpTree)
        contextMenu.setStyleSheet('color: white')
        #
        actCreerSousDossier = QAction('Créer un sous dossier', self)
        actCreerSousDossier.triggered.connect(self.createSousDossier)
        contextMenu.addAction(actCreerSousDossier)

        contextMenu.exec_(self.grpTree.mapToGlobal(pos))

    def renommerDossier(self, cleCreate):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))
        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        print(x, y)
        dialogDossier = DialogDossier(self, modif=True, cleCreate=cleCreate)
        dialogDossier.show()

    def createSousDossier(self, cleCreate):
        dialogDossier = DialogDossier(self, modif=False, cleCreate=cleCreate)
        dialogDossier.show()

    def supprSousDossier(self, cleCreate):
        reply = QMessageBox.question(self, 'Question', 'Voulez-vous supprimer le sous dossier ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(f'DELETE FROM biblioTreeTab WHERE cle={cleCreate}')
            self.refreshTree()


    def refreshTree(self):
        self.grpTree.close()

        self.grpTree = QGroupBox(self)
        self.grpTree.setStyleSheet('background-color: #333333')
        self.grpTree.setGeometry(0, 0, 400, 600)

        self.loadListTree()
        self.grpTree.show()


    def buildTree(self, root, offsetV, indent=''):
        if True: # os.path.isdir(root_path)
            lblNode = QLabel(self)
            lblNode.setFixedSize(30, 30)
            # lblNode.setStyleSheet('background-color: orange')
            lblNode.setText(root.data)
            lblNode.move(len(indent) * 10, offsetV)
            print(indent + f"📁 {root.data+str(len(indent))}")
            items = root.lstChildren
            for item in items:
                item_path = item
                if True:  # os.path.isdir(item_path)
                    offsetV += 35
                    self.buildTree(self.listTree[item-1], offsetV, indent + "    ")
                else:
                    print(indent + f"  📄 {item}")




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindowTree()
    window.show()
    sys.exit(app.exec_())




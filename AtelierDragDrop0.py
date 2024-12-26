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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dragCour = None
        self.listWidget = []
        # ***************************************************************
        # ******  Initialisation Database
        # ***************************************************************
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/VideoLearnerX.db')
        if db.open():
            query = QSqlQuery()
            bOk = query.exec(f'SELECT * FROM biblioTreeTab')

        self.initUI()
        self.loadListTree()

    def initUI(self):
        self.setGeometry(100, 100, 400, 600)

    def refreshTree(self):
        #  Effacer l'arbre
        for obj in self.listWidget:
            obj.deleteLater()

        self.loadListTree()

    def loadListTree(self):
        self.listTree = []
        self.listWidget = []
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
        # print('***************************************************')

        if len(listEtage) == 0:
            query = QSqlQuery()
            query.exec(f'SELECT data FROM biblioTreeTab')
            if query.next():
                nodeAux = TreeNode(1, -1, query.value('data'))
                listEtage.append(nodeAux)
        try:
            self.indice = 0
            self.listWidget = []
            self.displayTree(listEtage[0])
        except:
            pass
        # self.refreshTree()

    def displayTree(self, root, indent=''):
        if True:  # os.path.isdir(root) -> cas répertoires + fichiers
            # lblNode = DragLabel(self.grpTrree, root)

            lblNode = DraggableWidget(self, root)
            self.listWidget.append(lblNode)
            lblNode.contenant = self
            # indice = self.listTree.index(root)
            lblNode.move(len(indent)*6 + 10, self.indice*40+20)

            lblNode.posInit = (len(indent)*6 + 10, self.indice*30)
            # lblNode.setFixedWidth(lblNode.width() - lblNode.x())
            # lblNode.btnMenu.move(lblNode.width()-25, 0)
            items = root.lstChildren
            for item in items:
                nodeChild = [node for node in self.listTree if node.cle == item][0]
                if True:  # os.path.isdir(item_path)  -> cas répertoires + fichiers
                    self.indice += 1
                    self.displayTree(nodeChild, indent + "    ")
                else:
                    print(indent*3 + f"  📄 {item}")


class DraggableWidget(QLabel):
    def __init__(self, parent, node):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setStyleSheet('background-color: green; color: white')
        self.installEventFilter(self)
        self.parent = parent
        self.node = node
        self.setText(node.data)

        #  Rendre le widget glissable
        self.setAcceptDrops(True)

    def eventFilter(self, object, event):
        if event.type() == QEvent.Drop:
            cleTarget = object.node.cle
            cleDrag = self.parent.dragCour.node.cle
            #  Mise à jour de la base de données puis l'affichage de l'arbre modifié
            query = QSqlQuery()
            tplChamps = ('parent_id')
            tplData = (cleTarget)
            if cleDrag != cleTarget: #  cas du dossier déplacé sur lui-même
                query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle = {cleDrag}')
            self.parent.refreshTree()
        return super().eventFilter(object, event)

    def mousePressEvent(self, event):
        self.parent.dragCour = self
        # print(self.parent.dragCour.text())
        #  Commencer le processus de glissement
        mimeData = QMimeData()
        mimeData.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    # def dropEvent(self, event):
    #     print(event.pos())
    #     print(self.parent.dragCour.text())
    #     self.parent.dragCour.setText('OK')


# class TargetWidget(QLabel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.setFixedSize(200, 100)
#         self.setStyleSheet('background-color: orange; color: white')
#         self.setText('Drop')
#         self.initUI()
#
#     def initUI(self):
#         self.setAcceptDrops(True)
#
#     def dragEnterEvent(self, event):
#         event.acceptProposedAction()
#
#     def dropEvent(self, event):
#         print(self.parent.dragCour.text())
#         self.parent.dragCour.setText('OK')
#         return
#         print(type(self.parent))
#         # text = event.mimeData().text()
#         #


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
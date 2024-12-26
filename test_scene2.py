#  MosaiQ v0.1
import sys
from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem

#  Paramètres de configuration
#  Couleur de fond de la scène
COULEUR_FOND = 'white'

#  Couleur utilisée pour le contour des carrés
COULEUR_CONTOUR = 'black'

#  Plage (min, max) pour les composantes RGB de la couleur des carrés
PLAGE_COULEURS = (50, 250)

#  pourcentage utilisé pour éclairer les carrés survolés
FACTEUR_ECLAIRCISSEMENT = 150


class CarreMosaiQ(QGraphicsRectItem):
    _pen = QPen(QColor(COULEUR_CONTOUR))
    _pen.setCosmetic(True)

    def __init__(self, x, y, c):
        QGraphicsRectItem.__init__(self, 0, 0, c, c)
        self.setPos(x, y)
        self.setPen(CarreMosaiQ._pen)
        couleur = QColor(*(randint(*PLAGE_COULEURS) for _ in 'RGB'))
        self.brush = QBrush(couleur)
        self.setBrush(self.brush)
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        couleur = self.brush.color().lighter(FACTEUR_ECLAIRCISSEMENT)
        self.setBrush(QBrush(couleur))

    def hoverLeaveEvent(self, event):
        self.setBrush(self.brush)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton:
            self.fragmente()
        else:
            QGraphicsRectItem.mousePressEvent(self, mouseEvent)

    def fragmente(self):
        c = self.rect().width() / 2
        x = self.x()
        y = self.y()
        scene = self.scene()
        scene.removeItem(self)
        for (dx, dy) in ((0, 0), (c, 0), (0, c), (c, c)):
            scene.addItem(CarreMosaiQ(x+dx, y+dy, c))


class SceneMosaiQ(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        size = 2.0**32
        self.carreMosaiQUnivers = CarreMosaiQ(0, 0, size)
        self.addItem(self.carreMosaiQUnivers)


class VueMosaiQ(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor(COULEUR_FOND))
        self.setWindowTitle('MosaiQ')
        self.resize(800, 600)
        self.fitInView(scene.carreMosaiQUnivers, Qt.KeepAspectRatio)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        self.zoom(event.angleDelta().y()/100.0)

    def zoom(self, facteur):
        if facteur < 0.0:
            facteur = -1.0 / facteur
        self.scale(facteur, facteur)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sceneMosaiQ = SceneMosaiQ()
    vueMosaiQ = VueMosaiQ(sceneMosaiQ)
    vueMosaiQ.show()
    sys.exit(app.exec_())
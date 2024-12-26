from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, \
    QGraphicsItem, QGraphicsEllipseItem

import sys
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from random import random

app = QApplication(sys.argv)
#  ***********************************************************
#  Définition de la scène
scene = QGraphicsScene()
#  Rectangle
rectGris = QGraphicsRectItem(0., 0., 200., 150.)
rectGris.setBrush(QBrush(Qt.lightGray))
#  Texte
texte = QGraphicsTextItem('Tous en scène !')
dy = rectGris.sceneBoundingRect().height() - texte.sceneBoundingRect().height()
texte.setPos(rectGris.x(), rectGris.y() + dy)
texte.setDefaultTextColor(QColor('blue'))
texte.setZValue(1)
#  Smiley
d = 48.  # diametre smiley
ox = 4.  # largeur oeil
oy = 6.  # hauteur oeil
smiley = QGraphicsEllipseItem(-d/2, -d/2, d, d)
smiley.setBrush(QBrush(Qt.yellow))
yeux = [QGraphicsEllipseItem(-ox/2., -oy/2., ox, oy, parent=smiley) for _ in range(2)]
yeux[0].setPos(-d/6., -d/8)
yeux[1].setPos(+d/6., -d/8)
brush = QBrush(Qt.black)
for oeil in yeux:
    oeil.setBrush(brush)
smiley.setPos(rectGris.mapToScene(rectGris.rect().center()))

smiley.setScale(1.5)
smiley.setRotation(20.)
smiley.setFlag(QGraphicsItem.ItemIsMovable)

scene.addItem(rectGris)
scene.addItem(texte)
scene.addItem(smiley)

#  ***********************************************************
#  Définition de la vues
vue = QGraphicsView(scene)
vue.resize(800, 600)
vue.fitInView(rectGris, Qt.KeepAspectRatio)
vue.setRenderHints(QPainter.Antialiasing)
vue.show()
#
vue2 = QGraphicsView(scene)
vue2.setRenderHints(QPainter.Antialiasing)
vue2.resize(300, 400)
vue2.rotate(-20)
vue2.show()
#
vuesAux = []
for _ in range(4):
    vueAux = QGraphicsView(scene)
    vuesAux.append(vueAux)
    vueAux.setRenderHints(QPainter.Antialiasing)
    vueAux.resize(400, 300)
    vueAux.rotate(360*random())
    f = 4*random()
    vueAux.scale(f, f)
    vueAux.show()

sys.exit((app.exec_()))
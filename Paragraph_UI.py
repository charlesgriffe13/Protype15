# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Paragraph_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainParagraph(object):
    def setupUi(self, mainParagraph):
        mainParagraph.setObjectName("mainParagraph")
        mainParagraph.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainParagraph)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lytTop = QtWidgets.QHBoxLayout()
        self.lytTop.setObjectName("lytTop")
        self.verticalLayout.addLayout(self.lytTop)
        self.lytNote = QtWidgets.QVBoxLayout()
        self.lytNote.setObjectName("lytNote")
        self.verticalLayout.addLayout(self.lytNote)
        mainParagraph.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainParagraph)
        QtCore.QMetaObject.connectSlotsByName(mainParagraph)

    def retranslateUi(self, mainParagraph):
        _translate = QtCore.QCoreApplication.translate
        mainParagraph.setWindowTitle(_translate("mainParagraph", "MainWindow"))

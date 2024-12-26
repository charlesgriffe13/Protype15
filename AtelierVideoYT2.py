# import sys
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWebEngineWidgets import QWebEngineView
#
# app = QApplication(sys.argv)
# url = 'http://stackoverflow.com'
# url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'
# wv = QWebEngineView()
#
# wv.load(QUrl(url))
# print(str(QUrl(url)))
# wv.show()
# app.exec_()

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import *

import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.page().fullScreenRequested.connect(lambda request: request.accept())
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        #  &t=2m10s -> avancer jusqu'au time code 2 minutes 10 secondes
        #  remplacer watch?v= par /v/
        url = "https://www.youtube.com/watch?v=S8_JZNooKfk"

        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()
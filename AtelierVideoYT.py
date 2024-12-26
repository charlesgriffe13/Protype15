import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")
        self.setGeometry(100, 100, 800, 500)

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)

        # Code for 1 Youtube video and its QtWidget
        # ======================================================================================

        self.centralwid = QtWidgets.QWidget(self)
        self.centralwid.setGeometry(QtCore.QRect(60, 40, 760, 464))
        self.centralwid.setObjectName("centralwid")
        self.label_loading_browsers = QtWidgets.QLabel(self.centralwid)
        # ===================== HERE IS THE CODE FOR IFRAM YOUTUBE ============================
        self.vlayout = QtWidgets.QVBoxLayout()
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        self.webview.page().fullScreenRequested.connect(lambda request: request.accept())
        baseUrl = "local"
        htmlString = """
                        <iframe width="700" height="424" src="https://www.youtube.com/embed/g8NVwN0_mks?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>
                                """
        htmlStringx = """
                                <iframe width="700" height="424" src="https://www.youtube.com/embed/5hrd5Ek54VA?start=700&autoplay=1" frameborder="0" allowfullscreen></iframe>
                                        """
        # https: // www.youtube.com / watch?v = vkIbns5LDow & list = RDvkIbns5LDow & start_radio = 1
        self.webview.setHtml(htmlStringx, QUrl(baseUrl))
        self.vlayout.addWidget(self.webview)
        self.centralwid.setLayout(self.vlayout)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
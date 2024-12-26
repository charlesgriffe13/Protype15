import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Télécharger")
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text()
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension='mp4', progressive=True).first()
            video.download()
            self.message_label.setText("Téléchargement terminé !")
        except Exception as e:
            self.message_label.setText(f"Erreur : {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())

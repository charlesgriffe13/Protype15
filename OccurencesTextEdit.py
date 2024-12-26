from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyHighlighter(QTextEdit):
    def __init__(self, parent=None):
        super(MyHighlighter, self).__init__(parent)
        # Setup the text editor
        text = """In this text I want to highlight this word and only this word.\n""" +\
        """Any other word shouldn't be highlighted"""
        self.setText(text)
        cursor = self.textCursor()
        # Setup the desired format for matches
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor('#66cccc')))

        # Setup the regex engine
        pattern = "word"
        regex = QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.toPlainText(), pos)
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.toPlainText(), pos)

if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    styleAux = open('fEUILLEDESTYLE.txt', 'r')
    custom = styleAux.read()
    # print(custom)
    a.setStyleSheet(custom)
    t = MyHighlighter()
    t.show()
    sys.exit(a.exec_())
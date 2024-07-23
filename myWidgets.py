from PyQt5.QtWidgets import QListWidget,QMessageBox, QComboBox,QStylePainter, QStyleOptionComboBox, QStyle,QLineEdit
from PyQt5.QtGui import QValidator
from PyQt5.QtCore import Qt
import os

#Custom List allowing drag and drop and constraining number of elements in list
class CustomListWidget(QListWidget):
    def __init__(self, parent=None, type_restriction=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.maxFileList = 10
        self.type_restriction= type_restriction
    
    #Events
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            if len(event.mimeData().urls()) <= self.maxFileList: #TODO:add exception when droping IFC in IDS or viceversa
                for url in event.mimeData().urls():
                    filepath=str(url.toLocalFile())
                    itemInList= len(self.findItems(filepath, Qt.MatchExactly))
                    if url.isLocalFile() and itemInList ==0 and filepath.lower().endswith(self.type_restriction): #urls.isLocalFile exclude urls from websites / set restrictions to drop
                        links.append(filepath)
                        self.maxFileList-=1
                    else:
                        event.ignore()
                self.addItems(links)
            else:
                event.ignore()
                self.msgError= QMessageBox()
                self.msgError.setIcon(QMessageBox.Warning)
                self.msgError.setWindowTitle("Error")
                self.msgError.setText("You cannot import more than 10 files.")
                self.msgError.show()
    
    def getItemsDict(self)->dict:
        #generates an array wiht elements in list
        self.items=[]
        for x in range(self.count()):
            self.items.append(self.item(x).text())
        return self.items

#Custom Line edit constraining text to only capital letters
class UppercaseValidator(QValidator):
    def validate(self, string, pos):
        return (QValidator.Acceptable, string.upper(), pos)

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(UppercaseValidator())

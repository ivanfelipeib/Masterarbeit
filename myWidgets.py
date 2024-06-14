from PyQt5.QtWidgets import QListWidget,QMessageBox, QComboBox,QStylePainter, QStyleOptionComboBox, QStyle
# from PySide2 import QtGui
from PyQt5.QtCore import Qt
import os

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.maxFileList = 10
    
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
                    if url.isLocalFile() and itemInList ==0: #urls.isLocalFile exclude urls from websites
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
                self.msgError.setText("Sie können nicht mehr als 10 IFC-Dateien importieren")
                self.msgError.show()
    
    def getItems(self):
        #generates an array wiht elements in list
        self.items=[]
        for x in range(self.count()):
            self.items.append(os.path.basename(self.item(x).text()))
        return self.items


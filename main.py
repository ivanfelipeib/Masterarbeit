from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QMdiArea, QListView, QMdiSubWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt

from pathlib import Path
import sys

DIRECTORY_GUI= "GUI_Windows"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Load UI file
        root_dir = Path(__file__).resolve().parent
        filepath= root_dir / DIRECTORY_GUI / "main.ui"
        uic.loadUi(filepath, self)

        #Define Widgets
        self.btn_manage_ifc= self.findChild(QPushButton,"btn_manage_ifc")
        self.btn_manage_ids= self.findChild(QPushButton,"btn_manage_ids")
        self.btn_check= self.findChild(QPushButton,"btn_check")
        self.mdi_main= self.findChild(QMdiArea,"mdi_main")

        #Events
        self.btn_manage_ifc.clicked.connect(self.loadMdi)
        # self.btn_manage_ifc.clicked.connect(self.clickAddIfc)
        # self.btn_manage_ifc.clicked.connect(self.clickAddIfc)

        #Show the App
        self.show()

    def loadMdi(self):
        window= ManageIfcWindow()
        self.mdi_main.addSubWindow(window)
        window.showMaximized()
        self.mdi_main.currentSubWindow().setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
        

class ManageIfcWindow(QMainWindow):
    def __init__(self):
        super(ManageIfcWindow, self).__init__()

        #Load UI file
        root_dir = Path(__file__).resolve().parent
        filepath= root_dir / DIRECTORY_GUI / "ifc_manage.ui"
        uic.loadUi(filepath, self)

        #Define Widgets
        self.list_ifc= self.findChild(QListView,"list_IFC_management")
        self.btn_import_ifc= self.findChild(QPushButton,"btn_import_ifc")
        self.btn_delete_ifc= self.findChild(QPushButton,"btn_delete_ifc")

        #Events
        # self.btn_manage_ifc.clicked.connect(self.clickAddIfc)
        # self.btn_manage_ifc.clicked.connect(self.clickAddIfc)
        # self.btn_manage_ifc.clicked.connect(self.clickAddIfc)


#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()   
from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QMdiArea, QListView, QMdiSubWindow, QComboBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

from pathlib import Path
import sys

DIRECTORY_GUI= "GUI_Windows"
#Method for loading .ui files
def load_ui(filepath, window):
    root_dir = Path(__file__).resolve().parent
    filepath = root_dir / DIRECTORY_GUI / filepath
    uic.loadUi(filepath, window)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load UI file
        load_ui("main.ui", self)

        # Define Widgets
        self.btn_manage_ifc = self.findChild(QPushButton, "btn_manage_ifc")
        self.btn_manage_ids = self.findChild(QPushButton, "btn_manage_ids")
        self.btn_check = self.findChild(QPushButton, "btn_check")
        self.mdi_main = self.findChild(QMdiArea, "mdi_main")

        # Map buttons to their respective load methods and windows
        self.button_window_map = {
            self.btn_manage_ifc: (ManageIfcWindow, True),
            self.btn_manage_ids: (ManageIdsWindow, True),
            self.btn_check: (CheckWindow, False)
        }

        # Connect buttons to the handler
        for button, (window_class, is_mdi) in self.button_window_map.items():
            if is_mdi:
                button.clicked.connect(lambda checked, wc=window_class: self.loadSubWindow(wc))
            else:
                button.clicked.connect(lambda checked, wc=window_class: self.loadWindow(wc))

        # Show the App
        self.show()

    def loadSubWindow(self, window_class):
        window = window_class()
        sub_window = QMdiSubWindow()
        sub_window.setWidget(window)
        sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi_main.addSubWindow(sub_window)
        sub_window.showMaximized()

    def loadWindow(self, window_class):
        self.window = window_class()
        self.window.show()
        self.close()

class ManageIfcWindow(QMainWindow):
    def __init__(self):
        super(ManageIfcWindow, self).__init__()
        load_ui("ifc_manage.ui", self)    

class ManageIdsWindow(QMainWindow):
    def __init__(self):
        super(ManageIdsWindow, self).__init__()
        load_ui("ids_manage.ui", self)

class IdsEditorWindow(QMainWindow):
    def __init__(self):
        super(IdsEditorWindow, self).__init__()
        load_ui("idsEditor_main.ui", self)

class CheckWindow(QMainWindow):
    def __init__(self):
        super(CheckWindow, self).__init__()
        load_ui("check.ui", self)
    
    # Map buttons to their respective load methods and windows
        self.button_window_map = {
            self.btn_edit_ids: IdsEditorWindow,
            self.btn_new_ids: IdsEditorWindow,
            }
        
        # # Connect buttons to the handler
        # for button, (window_class, is_mdi) in self.button_window_map.items():
        #     if is_mdi:
        #         button.clicked.connect(lambda checked, wc=window_class: self.loadSubWindow(wc))
        #     else:
        #         button.clicked.connect(lambda checked, wc=window_class: self.loadWindow(wc))

#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()   
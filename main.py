from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QMdiArea, QListView, QMdiSubWindow, QComboBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

from pathlib import Path
import sys

DIRECTORY_GUI= "GUI_Windows"
#Method for loading .ui files

class Ops():
    @staticmethod
    def load_ui(filename, window):
        root_dir = Path(__file__).resolve().parent
        filepath = root_dir / DIRECTORY_GUI / filename
        uic.loadUi(filepath, window)

    @staticmethod
    def loadWidgets(window,widget_setup):
        window.widgets = {}
        if widget_setup:
            for widget_name, widget_type in widget_setup.items():
                window.widgets[widget_name] = window.findChild(widget_type, widget_name)
    
    @staticmethod
    def loadSubWindow(self, window_class, mdi_area_name):
        window = window_class()
        sub_window = QMdiSubWindow()
        sub_window.setWidget(window)
        sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        mdi_area = self.widgets[mdi_area_name]
        mdi_area.addSubWindow(sub_window)
        sub_window.showMaximized()

    @staticmethod
    def loadWindow(self, window_class):
        self.window = window_class()
        self.window.show()
        self.close()
    
    @staticmethod
    def clickAndLoad(self):
        for button, (window_class, mdi_area_name) in self.button_window_map.items():
            if mdi_area_name:
                button.clicked.connect(lambda checked, wc=window_class, name=mdi_area_name: Ops.loadSubWindow(self, wc, name))
            else:
                button.clicked.connect(lambda checked, wc=window_class: Ops.loadWindow(self, wc))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load UI file
        Ops.load_ui("main.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_manage_ifc": QPushButton,
            "btn_manage_ids": QPushButton,
            "btn_check": QPushButton,
            "mdi_main": QMdiArea
        }

        # Map buttons to their respective load methods and windows ("name"->load in mdi/ false->load independent window)
        self.button_window_map = {
            self.btn_manage_ifc: (ManageIfcWindow, "mdi_main"),
            self.btn_manage_ids: (ManageIdsWindow, "mdi_main"),
            self.btn_check: (CheckWindow, False)
            }
        
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )       
        # Connect buttons to the load function
        Ops.clickAndLoad(self)
        # Show the App
        self.show()

class ManageIfcWindow(QMainWindow):
    def __init__(self):
        super(ManageIfcWindow, self).__init__()
        Ops.load_ui("ifc_manage.ui", self)    

class ManageIdsWindow(QMainWindow):
    def __init__(self):
        super(ManageIdsWindow, self).__init__()

        # Load UI file
        Ops.load_ui("ids_manage.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_import_ids": QPushButton,
            "btn_delete_ids": QPushButton,
            "btn_ids_edit": QPushButton,
            "btn_ids_new": QPushButton,
            "list_ids_mgmnt": QListView
        }

        # Map buttons to their respective load methods and windows ("name""->load in mdi/ false->load independent window)
        self.button_window_map = {
            self.btn_import_ids: (IdsInfoWindow, False), #TODO: WIndow with explorer to select files. Up to 10
            self.btn_delete_ids: (IdsSpecListWindow, False), #TODO: Delete elements form list
            self.btn_ids_edit: (IdsEditorWindow, False), #TODO: When element selected, open IdsEditor Window populated with data from IDS, No selection than msgBox error
            self.btn_ids_new: (IdsEditorWindow, False), 
            }
        
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )       
        # Connect buttons to the load function
        Ops.clickAndLoad(self)
        # Show the App
        self.show()

class IdsInfoWindow(QMainWindow):
    def __init__(self):
        super(IdsInfoWindow, self).__init__()
        Ops.load_ui("idsEditor_general_info.ui", self)

class IdsSpecListWindow(QMainWindow):
    def __init__(self):
        super(IdsSpecListWindow, self).__init__()
        Ops.load_ui("idsEditor_spec_list.ui", self)

class IdsSpecEditorWindow(QMainWindow):
    def __init__(self):
        super(IdsSpecEditorWindow, self).__init__()
        Ops.load_ui("idsEditor_spec_editor.ui", self)

class IdsEditorAuditWindow(QMainWindow):
    def __init__(self):
        super(IdsEditorAuditWindow, self).__init__()
        Ops.load_ui("idsEditor_audit.ui", self)

class IdsEditorWindow(QMainWindow):
    def __init__(self):
        super(IdsEditorWindow, self).__init__()

        # Load UI file
        Ops.load_ui("idsEditor_main.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_ids_info": QPushButton,
            "btn_ids_specifications": QPushButton,
            "btn_ids_audit": QPushButton,
            "mdi_list": QMdiArea,
            "mdi_editor": QMdiArea
        }

        # Map buttons to their respective load methods and windows ("name""->load in mdi/ false->load independent window)
        self.button_window_map = {
            self.btn_ids_info: (IdsInfoWindow, "mdi_list"),
            self.btn_ids_specifications: (IdsSpecListWindow, "mdi_list"),#TODO: Button Specifications should load 2 MDI when user hits edit in ManageIdsWindow 
            self.btn_ids_audit: (IdsEditorAuditWindow, "mdi_editor")
            }
        
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )       
        # Connect buttons to the load function
        Ops.clickAndLoad(self)
        # Show the App
        self.show()

class CheckWindow(QMainWindow):
    def __init__(self):
        super(CheckWindow, self).__init__()

        # Load UI file
        Ops.load_ui("check.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_check_ifc": QPushButton,
            "btn_check_ifc_ids": QPushButton,
            "btn_report": QPushButton,
            "btn_back": QPushButton,
            "comboBox_ifc": QComboBox,
            "comboBox_ids": QComboBox
        }

        # Map buttons to their respective load methods and windows ("name""->load in mdi/ false->load independent window)
        self.button_window_map = {
            self.btn_check_ifc: (ManageIfcWindow, False),
            self.btn_check_ifc_ids: (ManageIdsWindow, False),
            self.btn_report: (CheckWindow, False),
            self.btn_back: (MainWindow, False),
            }
        
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )       
        # Connect buttons to the load function
        Ops.clickAndLoad(self)
        # Show the App
        self.show()

#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()   
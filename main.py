from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow
from PyQt5.QtCore import Qt, pyqtSignal
from myWidgets import CustomListWidget
from Ops import Ops
import sys
        
class ManageIfcWindow(QMainWindow):
    back_to_main_signal= pyqtSignal()

    def __init__(self, parent=None):
        super(ManageIfcWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("ifc_manage.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_import_ifc": QPushButton,
            "btn_delete_ifc": QPushButton,
            "list_ifc": CustomListWidget,
        }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )

        self.btn_import_ifc.clicked.connect(self.clickImport)
        self.btn_delete_ifc.clicked.connect(self.clickDelete)
    
    def clickImport(self):
        #Adds filepath from selected element to a list
        self.filter="IFC-Dateien (*.ifc)"
        self.title= "Öffnen"
        self.fileDialog = QFileDialog()
        self.tuple_names= self.fileDialog.getOpenFileNames(self, self.title, "", self.filter)
        
        if len(self.tuple_names[0]) <= self.list_ifc.maxFileList and self.tuple_names:
            self.file_names= self.tuple_names[0]
            for name in self.file_names:
                #Checks whether name already in fileList or not and add element if not 
                if len(self.list_ifc.findItems(name, Qt.MatchExactly)) == 0:
                    self.list_ifc.addItem(name)
                    self.list_ifc.maxFileList-=1
        else:
            self.msgError= QMessageBox()
            self.msgError.setIcon(QMessageBox.Warning)
            self.msgError.setWindowTitle("Error")
            self.msgError.setText("Sie können nicht mehr als 10 IFC-Dateien importieren")
            self.msgError.show()
    
    def clickDelete(self):
        #Grabs selected row or current row in List and deletes it
        row= self.list_ifc.currentRow()
        self.list_ifc.takeItem(row)
        #Updates maxFileList value
        self.list_ifc.maxFileList+=1



class ManageIdsWindow(QMainWindow):
    back_to_main_signal= pyqtSignal()
    def __init__(self, parent=None):
        super(ManageIdsWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("ids_manage.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_import_ids": QPushButton,
            "btn_delete_ids": QPushButton,
            "btn_ids_edit": QPushButton,
            "btn_ids_new": QPushButton,
            "list_ids_mgmnt": CustomListWidget
        }

        # Map buttons to their respective load methods and windows ("name""->load in mdi/ false->load independent window)
        self.button_window_map = {
            self.btn_ids_edit: (IdsEditorWindow, False), #TODO: When element selected, open IdsEditor Window populated with data from IDS, No selection than msgBox error
            self.btn_ids_new: (IdsEditorWindow, False), 
            }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )       
        # Connect buttons to the load function
        Ops.clickAndLoad(self)

        #Filepaths import
        self.btn_import_ids.clicked.connect(self.clickImport)
        self.btn_delete_ids.clicked.connect(self.clickDelete)
    
    def clickImport(self):
        #Adds filepath from selected element to a list
        self.filter="IDS-Dateien (*.ids)"
        self.title= "Öffnen"
        self.fileDialog = QFileDialog()
        self.tuple_names= self.fileDialog.getOpenFileNames(self, self.title, "", self.filter)
        
        if len(self.tuple_names[0]) <= self.list_ids_mgmnt.maxFileList and self.tuple_names:
            self.file_names= self.tuple_names[0]
            for name in self.file_names:
                #Checks whether name already in fileList or not and add element if not 
                if len(self.list_ids_mgmnt.findItems(name, Qt.MatchExactly)) == 0:
                    self.list_ids_mgmnt.addItem(name)
                    self.list_ids_mgmnt.maxFileList-=1
        else:
            self.msgError= QMessageBox()
            self.msgError.setIcon(QMessageBox.Warning)
            self.msgError.setWindowTitle("Error")
            self.msgError.setText("Sie können nicht mehr als 10 IFC-Dateien importieren")
            self.msgError.show()
    
    def clickDelete(self):
        #Grabs selected row or current row in List and deletes it
        row= self.list_ids_mgmnt.currentRow()
        self.list_ids_mgmnt.takeItem(row)
        #Updates maxFileList value
        self.list_ids_mgmnt.maxFileList+=1
        
class CheckWindow(QMainWindow):
    back_to_main_signal= pyqtSignal()

    def __init__(self, parent=None):
        super(CheckWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("check.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_check_ifc": QPushButton,
            "btn_check_ifc_ids": QPushButton,
            "btn_report": QPushButton,
            "btn_back": QPushButton,
            "comboBox_ifc": QComboBox,
            "comboBox_ids": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        self.btn_back.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.back_to_main_signal.emit()
        self.hide()

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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load UI file
        Ops.load_ui("main.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_manage_ifc": QPushButton,
            "btn_manage_ids": QPushButton,
            "btn_check": QPushButton,
            "mdi_main": QMdiArea
        }
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance of Subwindows
        self.ifc_window=None
        self.ids_window=None
        self.check_window= None   

        #Conect handler
        self.btn_manage_ifc.clicked.connect(self.openIfcWindow)
        self.btn_manage_ids.clicked.connect(self.openIdsWindow)
        self.btn_check.clicked.connect(self.openCheckWindow)
    
    def openIfcWindow(self):
        if self.ifc_window is None or self.ifc_window.isClosed:
            sub_window = QMdiSubWindow()
            self.ifc_window = ManageIfcWindow()
            self.ifc_window.back_to_main_signal.connect(self.clearMdiArea)
            sub_window.setWidget(self.ifc_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
            # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in OpenIfcWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.mdi_main.addSubWindow(sub_window)
            self.ifc_window.isClosed = False
            sub_window.showMaximized()
        else:
            self.ifc_window.showMaximized()
    
    def openIdsWindow(self):
        if self.ids_window is None or self.ids_window.isClosed:
            sub_window = QMdiSubWindow()
            self.ids_window = ManageIdsWindow()
            self.ids_window.back_to_main_signal.connect(self.clearMdiArea)
            sub_window.setWidget(self.ids_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
             # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in OpenIdsWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.mdi_main.addSubWindow(sub_window)
            self.ids_window.isClosed = False
            sub_window.showMaximized()
        else:
            self.ids_window.showMaximized()

    def openCheckWindow(self): 
        if self.check_window is None:
            self.check_window = CheckWindow()
            self.check_window.back_to_main_signal.connect(self.clearMdiArea)
            self.check_window.back_to_main_signal.connect(self.show_main_window)
        self.hide()  # Hide the main window
        self.check_window.show()
        self.check_window.raise_()
        self.check_window.activateWindow()
    
    def show_main_window(self):
        self.show()

    def clearMdiArea(self):
        self.mdi_main.closeAllSubWindows() #TODO:add argument in clearMdiArea with name of mdi. NoneType error triggered??

#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
UIWindow.show()
app.exec_()   
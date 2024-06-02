from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow
from PyQt5.QtCore import Qt, pyqtSignal
from myWidgets import CustomListWidget
from Ops import Ops
import sys

class IdsEditorWindow(QMainWindow):
    back_to_manage_ids= pyqtSignal()

    def __init__(self, parent= None):
        super(IdsEditorWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_main.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_ids_info": QPushButton,
            "btn_ids_specifications": QPushButton,
            "btn_ids_audit": QPushButton,
            "btn_back": QPushButton,
            "mdi": QMdiArea
        }
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance of Subwindows
        self.info_window=None
        self.spec_list_window=None
        self.spec_editor_window= None
        self.audit_window= None

        # Connect handlers
        handlers = {
            "btn_ids_info": self.openInfoWindow,
            "btn_ids_specifications": self.openSpecListWindow,
            "btn_ids_audit": self.openAuditWindow,
            "btn_back": self.backIdsList
        }
        Ops.connectHandlers(self, handlers)

    
    def openInfoWindow(self):
        if self.info_window is None or self.info_window.isClosed:
            sub_window = QMdiSubWindow()
            self.info_window = IdsInfoWindow()
            sub_window.setWidget(self.info_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
            # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in openInfoWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.mdi.addSubWindow(sub_window)
            self.info_window.isClosed = False
            sub_window.showMaximized()
        else:
            self.info_window.showMaximized()

    def openSpecListWindow(self):
        if self.spec_list_window is None or self.spec_list_window.isClosed:
            sub_window = QMdiSubWindow()
            self.spec_list_window = IdsSpecListWindow()
            self.spec_list_window.open_spec_editor.connect(self.openSpecEditorWindow)
            sub_window.setWidget(self.spec_list_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
            # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in openSpecListWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.total_height = self.mdi.height()
            self.spec_list_window.setGeometry(0, 0, self.mdi.width(), self.total_height // 3)
            self.mdi.addSubWindow(sub_window)
            self.spec_list_window.isClosed = False
            sub_window.showMaximized()
        else:
            self.spec_list_window.showMaximized()

    def openAuditWindow(self):
        if self.audit_window is None or self.audit_window.isClosed:
            sub_window = QMdiSubWindow()
            self.audit_window = IdsEditorAuditWindow()
            sub_window.setWidget(self.audit_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
            # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in openSpecListWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.mdi.setMaximumHeight(self.height())
            self.mdi.addSubWindow(sub_window)
            self.audit_window.isClosed = False
            sub_window.showMaximized()
        else:
            self.audit_window.showMaximized()
    
    def openSpecEditorWindow(self):
        if self.spec_editor_window is None or self.spec_editor_window.isClosed:
            sub_window = QMdiSubWindow()
            self.spec_editor_window = IdsSpecEditorWindow()
            sub_window.setWidget(self.spec_editor_window)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
            # mdi_area = self.widgets[mdi_area_name] #TODO:add argument in openSpecListWindow with name of mdi. NoneType error triggered??
            # mdi_area.addSubWindow(sub_window)
            self.total_height = self.mdi.height()
            self.spec_list_window.setGeometry(0, 0, self.mdi.width(), self.total_height // 3)
            self.spec_editor_window.setGeometry(0, self.total_height // 3, self.mdi.width(), 2 * self.total_height // 3)
            self.mdi.addSubWindow(sub_window)
            self.spec_editor_window.isClosed = False
            sub_window.show()
            self.spec_editor_window.show()
        else:
            self.spec_list_window.setGeometry(0, 0, self.mdi.width(), self.total_height // 3)
            self.spec_editor_window.setGeometry(0, self.total_height // 3, self.mdi.width(), 2 * self.total_height // 3)
            self.spec_list_window.show()
            self.spec_editor_window.show()


    def backIdsList(self):
        self.back_to_manage_ids.emit()
        self.hide()

    def setGeometriesMdiArea(self, window1):
        total_height = self.mdi.height()
        window1.setGeometry(0, 0, self.mdi.width(), total_height // 3)
        #window2.setGeometry(0, total_height // 3, self.mdi.width(), 2 * total_height // 3)   

class ManageIfcWindow(QMainWindow):
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

        # Connect handlers
        handlers = {
            "btn_import_ifc": self.clickImport,
            "btn_delete_ifc": self.clickDelete
        }
        Ops.connectHandlers(self, handlers)
    
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
    def __init__(self, parent=None):
        super(ManageIdsWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("ids_manage.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_import_ids": QPushButton,
            "btn_delete_ids": QPushButton,
            "btn_ids_edit": QPushButton,
            "btn_ids_new": QPushButton,
            "list_ids_mgmnt": CustomListWidget
        }
        Ops.loadWidgets(self, main_widget_setup )

        #Create instance of Subwindows
        self.idsEditor_window=None

        # Connect handlers
        handlers = {
            "btn_import_ids": self.clickImport,
            "btn_delete_ids": self.clickDelete,
            "btn_ids_edit": self.clickExistingEditorWindow,
            "btn_ids_new": self.clickNewEditorWindow,
        }
        Ops.connectHandlers(self, handlers)
                
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
    
    def clickNewEditorWindow(self): 
        self.idsEditor_window = IdsEditorWindow()
        self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds)
        self.hide()  # Hide the main window
        self.idsEditor_window.show()
        self.idsEditor_window.raise_()
        self.idsEditor_window.activateWindow()
    
    def clickExistingEditorWindow(self): #TODO: Clear IDS Instance and populate it with data from selected IDS
        if self.idsEditor_window is None:
            self.idsEditor_window = IdsEditorWindow()
            self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds)
        self.hide()  # Hide the main window
        self.idsEditor_window.show()
        self.idsEditor_window.raise_()
        self.idsEditor_window.activateWindow()
    
    def showManageIds(self):
        self.show()
        
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

        # Connect handlers
        handlers = {
            #"btn_check_ifc": self.clickImport, TODO: Implement methods for commented buttons
            #"btn_check_ifc_ids": self.clickDelete,
            #"btn_report": self.clickExistingEditorWindow,
            "btn_back": self.back_to_main,
        }
        Ops.connectHandlers(self, handlers)

    def back_to_main(self):
        self.back_to_main_signal.emit()
        self.hide()

class IdsInfoWindow(QMainWindow):
    def __init__(self):
        super(IdsInfoWindow, self).__init__()
        Ops.load_ui("idsEditor_general_info.ui", self)

class IdsSpecListWindow(QMainWindow):
    open_spec_editor= pyqtSignal()

    def __init__(self, parent= None):
        super(IdsSpecListWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_spec_list.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_new_spec": QPushButton,
            "btn_delete_spec": QPushButton,
            "list_ids_spec": CustomListWidget
        }
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance of Subwindows
        self.spec_editor_window=None

        # Connect handlers
        handlers = {
            "btn_new_spec": self.clickNew,
            "btn_delete_spec": self.clickDelete
        }
        Ops.connectHandlers(self, handlers)

    def clickNew(self):
        self.open_spec_editor.emit()
    
    def clickDelete(self):
        #Grabs selected row or current row in List and deletes it
        row= self.list_ids_spec.currentRow()
        self.list_ids_spec.takeItem(row)
        #Updates maxFileList value
        self.list_ids_spec.maxFileList+=1

class IdsSpecEditorWindow(QMainWindow):
    def __init__(self):
        super(IdsSpecEditorWindow, self).__init__()
        Ops.load_ui("idsEditor_spec_editor.ui", self)

class IdsEditorAuditWindow(QMainWindow):
    def __init__(self):
        super(IdsEditorAuditWindow, self).__init__()
        Ops.load_ui("idsEditor_audit.ui", self)

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

        # Connect handlers
        handlers = {
            "btn_manage_ifc": self.openIfcWindow,
            "btn_manage_ids": self.openIdsWindow,
            "btn_check": self.openCheckWindow
        }
        Ops.connectHandlers(self, handlers)   
    
    def openIfcWindow(self):
        self.ifc_window = Ops.openSubWindow(self.mdi_main, ManageIfcWindow, self.ifc_window, None)
    
    def openIdsWindow(self):
        self.ids_window = Ops.openSubWindow(self.mdi_main, ManageIdsWindow, self.ids_window, None)

    def openCheckWindow(self):
        def setup_signals(window_instance):
            window_instance.back_to_main_signal.connect(self.clearMdiArea)
            window_instance.back_to_main_signal.connect(self.show_main_window)
        self.check_window = Ops.openWindow(CheckWindow, self.check_window, setup_signals)

       #Populates Comboboxes in new CheckWindow()   #TODO: Add exception when no manage_ifc or ´manage_ids exist, error triggered
        if self.check_window.comboBox_ifc.count() == 0 and self.check_window.comboBox_ids.count() == 0:
            self.check_window.comboBox_ifc.clear()
            self.check_window.comboBox_ids.clear()
            self.check_window.comboBox_ifc.addItems(CustomListWidget.getItems(self.ifc_window.list_ifc))
            self.check_window.comboBox_ids.addItems(CustomListWidget.getItems(self.ids_window.list_ids_mgmnt))

            # Hide the main window show check window
            self.hide()  
            self.check_window.show()
            self.check_window.raise_()
            self.check_window.activateWindow()
        else:
            Ops.msgError(self,"Error","You have not uploaded any files yet")

    def show_main_window(self):
        self.show()

    def clearMdiArea(self):
        self.mdi_main.closeAllSubWindows() #TODO:add argument in clearMdiArea with name of mdi. NoneType error triggered??

#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
UIWindow.show()
app.exec_()   
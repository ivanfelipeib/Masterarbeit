from PyQt5.QtWidgets import QTableWidget, QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow, QLineEdit, QPlainTextEdit,QDateEdit, QTextBrowser
from PyQt5.QtCore import Qt, pyqtSignal
from myWidgets import CustomListWidget
from Ops import Ops
from idsOps import IdsOps
import filters 

class IdsEditorAuditWindow(QMainWindow):
    def __init__(self, parent= None):
        super(IdsEditorAuditWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_audit.ui", self)

        # Define and load Widgets
        main_widget_setup = {
            "textBrowser_audit": QTextBrowser,
            "btn_save": QPushButton,
            "btn_export": QPushButton
        }
        Ops.loadWidgets(self, main_widget_setup)

        
        # Connect handlers
        handlers = {
            "btn_save": self.clickNew,
            "btn_export": self.clickDelete
        }
        Ops.connectHandlers(self, handlers)

    def save(self):
        pass#TODO:Configure both buttons in class IdsEditorAuditWindow
    
    def export(self):
        pass

class IdsInfoWindow(QMainWindow):
    def __init__(self, parent= None):
        super(IdsInfoWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_info.ui", self)

        # Define and load Widgets
        main_widget_setup = {
            "txt_title": QLineEdit,
            "txt_copyright": QLineEdit,
            "txt_version": QLineEdit,
            "txt_author": QLineEdit,
            "date": QDateEdit,
            "txt_description": QPlainTextEdit,
            "txt_purpose": QPlainTextEdit,
            "txt_milestone": QPlainTextEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

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
    def __init__(self, parent=None):
        super(IdsSpecEditorWindow, self).__init__(parent)
        #Load UI
        Ops.load_ui("idsEditor_spec_editor.ui", self)

        # Define Widgets
        main_widget_setup = {
            #Tab Description
            "txt_name": QLineEdit,
            "text_description": QPlainTextEdit,
            "txt_instructions": QPlainTextEdit,
            #Tab Applicability
            "combo_mandatory": QComboBox,
            "combo_add_filter": QComboBox,
            "list_filters": CustomListWidget,
            "mdi_filter": QMdiArea,
            "btn_delete_filter": QPushButton,
            "btn_save_filter": QPushButton,
            #Tab Requirements
            "combo_add_requirement": QComboBox,
            "list_requirements": CustomListWidget,
            "mdi_requirement": QMdiArea,
            "btn_delete_requirement": QPushButton,
            "btn_save_requirement": QPushButton,
            #General
            "btn_save_specification": QPushButton
        }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance for subwindow
        self.opened_window= None

        # Set subwindow in mdiArea when currentText change in ComboBox 
        self.combo_add_filter.currentTextChanged.connect(self.openFilterSubWindow)
        self.combo_add_requirement.currentTextChanged.connect(self.openRequirementSubWindow)
        self.btn_save_requirement.clicked.connect(self.save_requirements_data)
        self.btn_save_filter.clicked.connect(self.save_filters_data)
        self.btn_delete_filter.clicked.connect(self.clickDeleteFilter)
        self.btn_delete_requirement.clicked.connect(self.clickDeleteRequirement)
        self.btn_save_specification.clicked.connect(self.saveSpecification)
    
    def openFilterSubWindow(self, text):
        mdi_area = self.mdi_filter
        mdi_area.closeAllSubWindows()

        match text:
            case "Add filter by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None)
            case "Add filter by part of":
                #self.by_part_of_window = Ops.openSubWindow(mdi_area, filters.byPartOf, self.by_part_of_window, setup_signals=None)
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None)
            case "Add filter by attribute":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None)
            case "Add filter by property":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None)
            case "Add filter by classification":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None)
            case "Add filter by material":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None)
            case _:
                Ops.msgError(self,"Error","Text in ComboBox does not match any type of filter")

    def openRequirementSubWindow(self, text):
        mdi_area = self.mdi_requirement
        mdi_area.closeAllSubWindows()

        match text:
            case "Add requirement by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None)
            case "Add requirement by part of":
                #self.by_part_of_window = Ops.openSubWindow(mdi_area, filters.byPartOf, self.by_part_of_window, setup_signals=None)
                self.opened_window= Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None)
            case "Add requirement by attribute":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None)
            case "Add requirement by property":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None)
            case "Add requirement by classification":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None)
            case "Add requirement by material":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None)
            case _:
                Ops.msgError(self,"Error","Text in ComboBox does not match any type of requirements")

    def save_requirements_data(self):
        current_text = self.combo_add_requirement.currentText()
        data = self.opened_window.getData()
        self.list_requirements.addItem(data)
        self.opened_window.close()

    def save_filters_data(self):
        current_text = self.combo_add_filter.currentText()
        data = self.opened_window.getData()
        self.list_filters.addItem(data)
        self.opened_window.close()
 
    def clickDeleteRequirement(self, Type):
        #Grabs selected row or current row in List and deletes it
        row= self.list_requirements.currentRow()
        self.list_requirements.takeItem(row)
        #Updates maxFileList value
        self.list_requirements.maxFileList+=1

    def clickDeleteFilter(self, Type):
        #Grabs selected row or current row in List and deletes it
        row= self.list_filters.currentRow()
        self.list_filters.takeItem(row)
        #Updates maxFileList value
        self.list_filters.maxFileList+=1

    def saveSpecification(self):
        self.close()
        #TODO: finish this section, Save specification
        # description_data = {
        #     "Name": self.txt_name.text(),
        #     "Description": self.text_description.text(),
        #     "Instructions": self.txt_instructions.text()
        # }

        # applicability_data = []
        # for i in range(self.list.count()):
        #     applicability_data.append(self.list_requirements.item(i).text())

        # requirements_data = []
        # for i in range(self.list_filters.count()):
        #     requirements_data.append(self.list_filters.item(i).text())

        # spec_data = {
        #     "Description": description_data,
        #     "Applicability": applicability_data,
        #     "Requirements": requirements_data
        # }

        # self.spec_list_window.add_specification(spec_data)       

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
            "mdi_list": QMdiArea,
            "mdi_editor": QMdiArea
        }
        Ops.loadWidgets(self, main_widget_setup)
        #Hide mdi_editor as default when opening new IdsEditor
        self.mdi_editor.hide()

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
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.info_window = Ops.openSubWindow(self.mdi_list, IdsInfoWindow, self.info_window, None)

    def openSpecListWindow(self):
        def setup_signals(window_instance):
            window_instance.open_spec_editor.connect(self.openSpecEditorWindow) #Connect with signal in IdsSpecEditorWindow Button:New

        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.spec_list_window = Ops.openSubWindow(self.mdi_list, IdsSpecListWindow, self.spec_list_window, setup_signals)

    def openAuditWindow(self):
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.audit_window = Ops.openSubWindow(self.mdi_list, IdsEditorAuditWindow, self.audit_window, None)
        self.setIdsInfo
     
    def openSpecEditorWindow(self):
        hint = self.mdi_list.minimumSizeHint()
        self.mdi_list.resize(hint)
        self.mdi_editor.showMaximized()
        self.spec_editor_window = Ops.openSubWindow(self.mdi_editor, IdsSpecEditorWindow, None, None)

    def setIdsInfo(self):
     #Create ids intance and pass ids_info to ids()
        ids_info = {
            "title": self.info_window.txt_title.text(),
            "copyright": self.info_window.txt_copyright.text(),
            "version": self.info_window.txt_version.text(),
            "description": self.info_window.txt_description.text(),
            "author": self.info_window.txt_author.text(),
            "date": self.info_window.date.date.toString(),#TODO:Proof if that returns a valid string from Date
            "purpose": self.info_window.txt_purpose.text(),
            "milestone": self.info_window.txt_milestone.text()
        }
        IdsOps.createIds(ids_info)

    def backIdsList(self):
        self.back_to_manage_ids.emit()
        self.hide()

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
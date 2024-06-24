from PyQt5.QtWidgets import QTableWidget, QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow, QLineEdit, QPlainTextEdit,QDateEdit, QTextBrowser
from PyQt5.QtCore import Qt, pyqtSignal, QVariant
from myWidgets import CustomListWidget
from Ops import Ops
from idsOps import IdsOps
import filters 
import uuid
import shutil
import constants

class IdsEditorAuditWindow(QMainWindow):
    def __init__(self, parent= None):
        super(IdsEditorAuditWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_audit.ui", self)

        # Define and load Widgets
        main_widget_setup = {
            "textBrowser_audit": QTextBrowser,
            "btn_export": QPushButton
        }
        Ops.loadWidgets(self, main_widget_setup)

        
        # Connect handlers
        handlers = {
            "btn_export": self.export
        }
        Ops.connectHandlers(self, handlers)
    
    def export(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        destination_file, _ = QFileDialog.getSaveFileName(self, "Select destination filepath", "", "All Files (*)", options=options)
        if destination_file:
            print(f"Destination file path: {destination_file}")
            try:
                shutil.copy(constants.TEMP_IDS_DIR, destination_file)
                QMessageBox.information(self, "Success", f"File exported to {destination_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export file: {e}")

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
    open_spec_editor= pyqtSignal() #Signal when clicking on New Specification go to method OpenSpecEditor method in IdsEditorWindow class

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

        #Create dictionary of specifications' names(Key) and Specification instances (Values) to handele list_ids_spec
        self.dic_specifications = {}

        # Connect handlers
        handlers = {
            "btn_new_spec": self.clickNew,
            "btn_delete_spec": self.clickDelete
        }
        Ops.connectHandlers(self, handlers)
      

    def clickNew(self):
        self.open_spec_editor.emit()
    
    def clickDelete(self):
        index = self.list_ids_spec.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            spec = self.dic_specifications.pop(item)  # Remove the entry and get the associated object
            self.list_ids_spec.model().removeRow(index.row())
            del spec
        self.list_ids_spec.maxFileList+=1
        print(self.dic_specifications)

    
    def updateSpecList(self):
        #Save specification in List in SpecListWindow
        my_spec = self.spec_editor_window.my_spec
        item= my_spec.name
        self.dic_specifications[item]=my_spec
        self.list_ids_spec.addItem(item)
        print(self.dic_specifications)
       
class IdsSpecEditorWindow(QMainWindow):
    add_spec_to_list= pyqtSignal() #Signal when clicking on Save Specification

    def __init__(self, my_ids, my_spec, parent=None):
        super(IdsSpecEditorWindow, self).__init__(parent)
        #Load UI
        Ops.load_ui("idsEditor_spec_editor.ui", self)

        # Define an load Widgets
        main_widget_setup = {
            #Tab Description
            "txt_name": QLineEdit,
            "combo_ifc_version": QComboBox,
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
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance for subwindow and ids
        self.opened_window= None
        self.my_ids= my_ids
        #If no spec was passed from SpecList a new instance is created:
        self.my_spec= my_spec
        if self.my_spec is None:
            self.my_spec=IdsOps.createSpec()
        else: 
            pass
        #Set dictionaries to storage entries in lists and related facet (Key, Value).
        self.dic_requirements={}
        self.dic_filters={}
    
        # Set subwindow in mdiArea when currentText change in ComboBox 
        self.combo_add_filter.currentTextChanged.connect(self.openFilterSubWindow)
        self.combo_add_requirement.currentTextChanged.connect(self.openRequirementSubWindow)
        #Connect buttons with handlers
        handlers = {
            "btn_save_requirement": self.save_requirements_data,
            "btn_save_filter": self.save_filters_data,
            "btn_delete_filter": self.clickDeleteFilter,
            "btn_delete_requirement": self.clickDeleteRequirement,
            "btn_save_specification": self.saveSpecification
        }
        Ops.connectHandlers(self, handlers)
    
    def openFilterSubWindow(self, text):
        mdi_area = self.mdi_filter
        mdi_area.closeAllSubWindows()

        match text:
            case "Add filter by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None)
            case "Add filter by part of":
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
        
        if text != "Add filter by class":
            self.opened_window.combo_optionality.hide()
            self.opened_window.lbl_optionality.hide()
        else: pass

    def openRequirementSubWindow(self, text):
        mdi_area = self.mdi_requirement
        mdi_area.closeAllSubWindows()

        match text:
            case "Add requirement by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None)
            case "Add requirement by part of":
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
        
        if text != "Add requirement by class":
            self.opened_window.combo_optionality.show()
            self.opened_window.lbl_optionality.show()
        else: pass

    def save_requirements_data(self):
        current_text = self.combo_add_requirement.currentText()
        dict_data = self.opened_window.getData()
        facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data)
        item= facet.to_string(clause_type= "requirement", specification=self.my_spec, requirement=facet)#TODO: Fork repository from building smart to solve incoompatibility class Entity and to_string() method. Imported forked library as module
        self.dic_requirements[item]= facet
        self.list_requirements.addItem(item)
        self.opened_window.close()

    def save_filters_data(self):
        current_text = self.combo_add_filter.currentText()
        dict_data = self.opened_window.getData()
        cardinality = self.combo_mandatory.currentText()
        print(cardinality)
        facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data, is_filter= True, cardinality_filter= cardinality)
        item= facet.to_string(clause_type= "applicability", specification=self.my_spec, requirement=None)
        self.dic_filters[item]= facet
        self.list_filters.addItem(item)
        self.opened_window.close()

    def clickDeleteRequirement(self):
        index = self.list_requirements.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            facet = self.dic_requirements.pop(item)  # Remove the entry and get the associated object
            self.list_requirements.model().removeRow(index.row())
            del facet
        self.list_requirements.maxFileList+=1

    def clickDeleteFilter(self):
        index = self.list_filters.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            facet = self.dic_filters.pop(item)  # Remove the entry and get the associated object
            self.list_filters.model().removeRow(index.row())
            del facet
        self.list_filters.maxFileList+=1

    def saveSpecification(self):
        #add Specification Info to Specification instance
        spec_info = {
            "name": self.txt_name.text(),
            "ifcVersion": self.combo_ifc_version.currentText(),
            "identifier": str(uuid.uuid4()),
            "description": self.txt_description.toPlainText(),
            "instructions": self.txt_instructions.toPlainText(),
        }
        self.my_spec=IdsOps.addSpecInfo(spec_info)
        #Add Applicability and Requirments to specification instance
        self.my_spec.applicability = list(self.dic_filters.values())
        self.my_spec.requirements = list(self.dic_requirements.values())
        # Set cardinality of Applicability section
        optionality = self.combo_mandatory.currentText()
        self.my_spec.set_usage(usage=optionality) 
        #Add populated specification to Specification list. See openSpecEditor method in class IdsEditorWindow
        self.add_spec_to_list.emit()
        self.close()
        print(self.my_spec.name)

class IdsEditorWindow(QMainWindow):
    back_to_manage_ids= pyqtSignal()
    add_ids_to_list= pyqtSignal() #signal activated when clicking on "Save IDS" button in IdsEditorWindow

    def __init__(self, my_ids, parent= None ):
        super(IdsEditorWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("idsEditor_main.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_ids_info": QPushButton,
            "btn_ids_specifications": QPushButton,
            "btn_ids_audit": QPushButton,
            "btn_ids_save": QPushButton,
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
        self.audit_window= None

        #If no ids was passed from IdsManagerWindow a new instance is created and flag reamins False:
        self.flag_load_data = False
        self.my_ids= my_ids
        if self.my_ids is None:
            self.my_ids=IdsOps.createIds()
        else:
            self.flag_load_data=True
            pass

        # Connect handlers
        handlers = {
            "btn_ids_info": self.openInfoWindow,
            "btn_ids_specifications": self.openSpecListWindow,
            "btn_ids_audit": self.openAuditWindow,
            "btn_ids_save": self.saveIds,
            "btn_back": self.backIdsList
        }
        Ops.connectHandlers(self, handlers)


    def openInfoWindow(self):
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.info_window = Ops.openSubWindow(self.mdi_list, IdsInfoWindow, self.info_window, None)
        if self.flag_load_data:
            self.loadInfo()
        else:
            pass

    def openSpecListWindow(self):
        def setup_signals(window_instance):
            window_instance.open_spec_editor.connect(self.openSpecEditorWindow) #Connect signal in IdsSpecListWindow Button:New, with method
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.spec_list_window = Ops.openSubWindow(self.mdi_list, IdsSpecListWindow, self.spec_list_window, setup_signals)
     
    def openSpecEditorWindow(self):
        def setup_signals(window_instance):
            window_instance.add_spec_to_list.connect(self.spec_list_window.updateSpecList) #Connect signal in IdsSpecEditorWindow Button:Save Specification, with method
        hint = self.mdi_list.minimumSizeHint()
        self.mdi_list.resize(hint)
        self.mdi_editor.showMaximized()
        self.spec_list_window.spec_editor_window = Ops.openSubWindow(self.mdi_editor, IdsSpecEditorWindow, None, setup_signals=setup_signals, my_ids_instance= self.my_ids)

    def openAuditWindow(self):
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.audit_window = Ops.openSubWindow(self.mdi_list, IdsEditorAuditWindow, self.audit_window, None)
        self.generateIdsFile() #generate IDS file in temp_files folder each time Audit button is clicked
        self.runAudit() #Audit Report of IDS file
        
    def generateIdsFile(self):
        self.my_ids= IdsOps.createIds() 
        self.addIdsInfo()
        self.addIdsSpecifications()
        self.idsToXML()

    def idsToXML(self):
        filepath= constants.TEMP_IDS_DIR 
        self.my_ids.filepath= filepath
        self.my_ids.to_xml(filepath) #Convert IDS in xml structure and save it in filepath

    def runAudit(self):
        filepathLog= constants.TEMP_LOG_DIR
        IdsOps.auditIds() #run c# script to run IDS Audit
        with open(filepathLog, 'r') as file:
                content = file.read()
                self.audit_window.textBrowser_audit.setText(content)

    def addIdsInfo(self):
        self.ids_info = {
            "title": self.info_window.txt_title.text(),
            "copyright": self.info_window.txt_copyright.text(),
            "version": self.info_window.txt_version.text(),
            "description": self.info_window.txt_description.toPlainText(),
            "author": self.info_window.txt_author.text(),
            "date": Ops.dateToIsoFormat(self.info_window.date),
            "purpose": self.info_window.txt_purpose.toPlainText(),
            "milestone": self.info_window.txt_milestone.toPlainText()
        }
        self.my_ids=IdsOps.addIdsInfo(self.my_ids, self.ids_info)
    
    def addIdsSpecifications(self):
        specifications= list(self.spec_list_window.dic_specifications.values())
        for element in specifications:
            self.my_ids.specifications.append(element)
    
    def saveIds(self):
        self.generateIdsFile()
        self.add_ids_to_list.emit() #Activate signal in class ManageIdsWindow method updateIdsList to pass ids.Ids() Object
        self.close()
    
    def loadInfo(self):
        
    
    def backIdsList(self):
        self.back_to_manage_ids.emit()
        self.close()

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

        #Set dictionary to storage entries in ids lists(Key) and corresponding ids instance (value)
        self.dic_ids={}

        # Connect handlers 
        handlers = {
            "btn_import_ids": self.clickImport,
            "btn_delete_ids": self.clickDelete,
            "btn_ids_edit": self.clickEdit,
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
        self.idsEditor_window = IdsEditorWindow(my_ids=None) #Pass my_ids as None when clicking on New
        self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds) #Connect signal of "Back to IDS Manager" button
        self.idsEditor_window.add_ids_to_list.connect(self.updateIdsList)# Connect signal of "Save IDS" button
        self.hide()  # Hide the main window
        self.idsEditor_window.show()
        self.idsEditor_window.raise_()
        self.idsEditor_window.activateWindow()

    def clickEdit(self):
        ids_as_dict=self.parseImportedIds()
        my_ids= IdsOps.parseDictToIds(ids_as_dict)
        self.idsEditor_window = IdsEditorWindow(my_ids=my_ids) #Pass parsed IDS to new IDSEditorWindow
        self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds) #Connect signal of "Back to IDS Manager" button
        self.idsEditor_window.add_ids_to_list.connect(self.updateIdsList)# Connect signal of "Save IDS" button
        self.hide()  # Hide the main window
        self.idsEditor_window.show()
        self.idsEditor_window.raise_()
        self.idsEditor_window.activateWindow()


    def setFilepathIds(self, my_ids):
        self.filter="IDS files (*.ids)"
        self.title= "Save IDS file"
        self.fileDialog = QFileDialog()
        self.fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        self.file_path, _ = self.fileDialog.getSaveFileName(None, self.title, "", self.filter)
        if self.file_path:
            if len(self.list_ids_mgmnt.findItems(self.file_path, Qt.MatchExactly)) == 0:
                    #Save IDS File
                    my_ids.filepath=self.file_path
                    my_ids.to_xml(self.file_path)
                    print(f"File saved in: {self.file_path}")
                    #TODO: Reverse process, parse Element to dictionary
                    #TODO: parse dictionary to ids instance
                    #TODO: add instance to dictionary and display in IDS Editor

            else: print(f"filepath already in list. {self.file_path}")
        else:
            print("No file selected to save")

    def updateIdsList(self):
        my_ids = self.idsEditor_window.my_ids
        self.setFilepathIds(my_ids)
        item= my_ids.filepath
        self.dic_ids[item]=my_ids #Key= Filepath, Value= ids.Ids() instance
        self.list_ids_mgmnt.addItem(item)
        print(self.dic_ids)
    
    def deleteIds(self): #TODO:Connect this method with button delete, but first populate dic_ids with imported ids files
        index = self.list_ids_mgmnt.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            ids = self.dic_ids.pop(item)  # Remove the entry and get the associated object
            self.list_ids_mgmnt.model().removeRow(index.row())
            del ids
        self.list_ids_mgmnt.maxFileList+=1
        print(self.dic_ids)
    
    def parseImportedIds(self):
        selected_item= self.list_ids_mgmnt.selectedItems()
        if selected_item:
            file_path=selected_item.text()
            ids_parsed_dic=IdsOps.parseXmlToDict(file_path)
            return ids_parsed_dic
        else:
            self.selected_label.setText('No element from IDS List was selected')

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

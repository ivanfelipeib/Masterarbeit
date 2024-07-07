from PyQt5.QtWidgets import QTableWidget, QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow, QLineEdit, QPlainTextEdit,QDateEdit, QTextBrowser
from PyQt5.QtCore import Qt, pyqtSignal, QVariant
from myWidgets import CustomListWidget
from Operations.Ops import Ops
from Operations.idsOps import IdsOps
from Operations.ifcOps import IfcOps
from ifctester import ids
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
    def __init__(self, parent= None, my_ids= None, my_spec= None, my_facet=None):
        super(IdsInfoWindow, self).__init__(parent)
        
        self.my_ids=my_ids 

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

        #Load data if ids was passed
        if self.my_ids:
            self.loadData(self.my_ids)
        else:
            pass
    
    def loadData(self, ids_instance:ids.Ids):
        idsToLoad=ids_instance
        self.txt_title.setText(idsToLoad.info["title"])
        self.txt_copyright.setText(idsToLoad.info["copyright"])
        self.txt_version.setText(idsToLoad.info["version"])
        self.txt_author.setText(idsToLoad.info["author"])
        #self.date TODO: Search method to set date from string
        self.txt_description.setPlainText(idsToLoad.info["description"])
        self.txt_purpose.setPlainText(idsToLoad.info["purpose"])
        self.txt_milestone.setPlainText(idsToLoad.info["milestone"])
        



class IdsSpecListWindow(QMainWindow):
    open_spec_editor= pyqtSignal() # emit signal when clicking on New Specification, go to method OpenSpecEditor in class IdsEditorWindow

    def __init__(self, parent= None, my_ids:ids.Ids = None, my_spec:ids.Specification = None, my_facet:ids.Facet=None):
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

        #Define Subwindows
        self.spec_editor_window=None
        #Define ids and spec
        self.my_ids = my_ids
        self.my_spec = my_spec

        #Create dictionary of specifications' names(Key) and Specification instances (Values) to handel list_ids_spec
        self.dic_specifications = {}

        # Connect handlers
        handlers = {
            "btn_new_spec": self.clickNew,
            "btn_delete_spec": self.clickDelete,
            "btn_edit_spec": self.clickEdit
        }
        Ops.connectHandlers(self, handlers)

        #Load specifications if ids was passed
        if self.my_ids:
            self.loadSpec(self.my_ids)
        else:
            print(f"No Ids was passed to {self}")
            pass
    
    def loadSpec(self, ids_instance:ids.Ids):
        idsToLoad=ids_instance
        specifications = idsToLoad.specifications
        for spec in specifications:
            item= spec.name
            self.dic_specifications[item]=spec
            self.list_ids_spec.addItem(item)

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

    def clickEdit(self):
        index = self.list_ids_spec.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            self.my_spec = self.dic_specifications[item]
        self.open_spec_editor.emit()
        pass
    
    def updateSpecList(self):
        #Save specification in List in SpecListWindow
        my_spec = self.spec_editor_window.my_spec
        item= my_spec.name

        # Check if the item already exists in the dictionary, Find and remove the existing item from the list widget 
        # TODO:uuid not supported by IDS schema, which approach for replacing elements in list, Just string in list??
        if item in self.dic_specifications:
            matching_items = self.list_ids_spec.findItems(item, Qt.MatchExactly)
            for match in matching_items:
                row = self.list_ids_spec.row(match)
                self.list_ids_spec.takeItem(row)

        self.dic_specifications[item]=my_spec
        self.list_ids_spec.addItem(item)
        print(self.dic_specifications)
       
class IdsSpecEditorWindow(QMainWindow):
    add_spec_to_list= pyqtSignal() #Signal when clicking on Save Specification

    def __init__(self, parent=None, my_ids=None, my_spec=None, my_facet=None):
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
            "btn_edit_filter": QPushButton,
            #Tab Requirements
            "combo_add_requirement": QComboBox,
            "list_requirements": CustomListWidget,
            "mdi_requirement": QMdiArea,
            "btn_delete_requirement": QPushButton,
            "btn_save_requirement": QPushButton,
            "btn_edit_requirement": QPushButton,
            #General
            "btn_save_specification": QPushButton
        }
        Ops.loadWidgets(self, main_widget_setup)

        #Create instance for subwindow and specification
        self.opened_window= None
        self.my_spec= my_spec
        #Set dictionaries to storage entries in lists (Key= facet string, Value= facet).
        self.dic_requirements={}
        self.dic_filters={}
        #Set element to handle facet in edition
        self.facet_in_edition=None

        #If no spec was passed from SpecList a new instance is created:
        if self.my_spec is None:
            self.my_spec=IdsOps.createSpec()
        else: # If spec was passed, load information
            self.loadInfo()
            self.loadFiltersList()
            self.loadRequirementsList()
            self.loadCardinality()
    
        # Set subwindow in mdiArea when currentText change in ComboBox 
        self.combo_add_filter.currentTextChanged.connect(self.openFilterSubWindow)
        self.combo_add_requirement.currentTextChanged.connect(self.openRequirementSubWindow)

        #Connect buttons with handlers
        handlers = {
            "btn_save_requirement": self.save_requirements_data,
            "btn_save_filter": self.save_filters_data,
            "btn_edit_filter": self.loadFilSubWindow,
            "btn_edit_requirement": self.loadReqSubWindow,
            "btn_delete_filter": self.clickDeleteFilter,
            "btn_delete_requirement": self.clickDeleteRequirement,
            "btn_save_specification": self.saveSpecification
        }
        Ops.connectHandlers(self, handlers)

        #Connect buttons with methods that do take arguments
        # self.btn_edit_filter.clicked.connect(lambda: self.loadFilSubWindow('parameter1', 'parameter2'))
        # self.btn_edit_requirement.clicked.connect(lambda: self.loadReqSubWindow('parameter1', 'parameter2'))
    
    def openFilterSubWindow(self, text, facet_to_load = None):
        mdi_area = self.mdi_filter
        mdi_area.closeAllSubWindows()
        facet_to_load=facet_to_load

        match text:
            case "Add filter by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by part of":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by attribute":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by property":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by classification":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by material":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case _:
                Ops.msgError(self, "Error","Text in ComboBox does not match any type of filter")
        
        if text != "Add filter by class":
            self.opened_window.combo_optionality.hide()
            self.opened_window.lbl_optionality.hide()
        else: pass

    def openRequirementSubWindow(self, text, facet_to_load=None):
        mdi_area = self.mdi_requirement
        mdi_area.closeAllSubWindows()
        facet_to_load=facet_to_load

        match text:
            case "Add requirement by class":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by part of":
                self.opened_window= Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by attribute":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by property":
                self.opened_window =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by classification":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by material":
                self.opened_window = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case _:
                Ops.msgError(self, "Error","Text in ComboBox does not match any type of requirements")
        
        if text != "Add requirement by class":
            self.opened_window.combo_optionality.show()
            self.opened_window.lbl_optionality.show()
        else: pass

    def save_requirements_data(self):
        #Create new facet
        current_text = self.combo_add_requirement.currentText()
        dict_data = self.opened_window.getData()
        facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data)
        item= facet.to_string(clause_type= "requirement", specification=self.my_spec, requirement=facet)#TODO: Fork repository from building smart to solve incoompatibility class Entity and to_string() method. Imported forked library as module
        
        #if there was and element in edition, delete element from dictionary and list
        if self.facet_in_edition:
            del self.dic_requirements[self.facet_in_edition]
            Ops.deleteItemInList(self,"list_requirements", self.facet_in_edition)
            self.facet_in_edition= None

        #Add newfacet to dictionary and list
        self.dic_requirements[item]= facet
        self.list_requirements.addItem(item)
        self.opened_window.close()

    def save_filters_data(self):
        #Create new facet
        current_text = self.combo_add_filter.currentText()
        dict_data = self.opened_window.getData()
        cardinality = self.combo_mandatory.currentText()
        facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data, is_filter= True, cardinality_filter= cardinality)
        item= facet.to_string(clause_type= "applicability", specification=self.my_spec, requirement=None)

        #if there was and element in edition, delete element from dictionary and list
        if self.facet_in_edition:
            del self.dic_filters[self.facet_in_edition]
            Ops.deleteItemInList(self,"list_filters", self.facet_in_edition)
            self.facet_in_edition= None

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
    
    def loadRequirementsList(self):
        for requirement_load in self.my_spec.requirements:
            item= requirement_load.to_string(clause_type= "requirement", specification=self.my_spec, requirement=requirement_load)
            self.dic_requirements[item]= requirement_load
            self.list_requirements.addItem(item)
            print(self.dic_requirements)

    def loadFiltersList(self):
        for filter_load in self.my_spec.applicability:
            item= filter_load.to_string(clause_type= "applicability", specification=self.my_spec, requirement=None)
            self.dic_filters[item]= filter_load
            self.list_filters.addItem(item)
            print(self.dic_filters)

    def loadInfo(self):
        self.txt_name.setText(self.my_spec.name)
        self.txt_description.setPlainText(self.my_spec.description)
        self.txt_instructions.setPlainText(self.my_spec.instructions)
        ifc_version=self.my_spec.ifcVersion
        Ops.setTextComboBox(self,"combo_ifc_version", ifc_version)
    
    def loadReqSubWindow(self):
        index = self.list_requirements.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            self.facet_in_edition = item #Store item in edition to delete it from the list and add updated item
            req_selected = self.dic_requirements[item]
            facet_class = type(req_selected).__name__.lower() #retrieve class as a lowercase string
            text = "Add requirement by "+ facet_class
            Ops.setTextComboBox(self, "combo_add_requirement", text)#Set value of combobox with type of requirements to the corresponding type of selected requirement
        self.openRequirementSubWindow(text, req_selected)

    def loadFilSubWindow(self):
        index = self.list_filters.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            self.facet_in_edition = item #Store item in edition to delete it from the list and add updated item
            filter_selected = self.dic_filters[item]
            facet_class = type(filter_selected).__name__.lower() #retrieve class as a lowercase string
            text = "Add filter by "+ facet_class
            Ops.setTextComboBox(self, "combo_add_filter", text) #Set value of combobox with type of filters to the corresponding type of selected filter
        self.openFilterSubWindow(text, filter_selected)
    
    def loadCardinality(self):
        #Set cardinality according with IDS documentation https://github.com/buildingSMART/IDS/blob/development/Documentation/specifications.md
        min_ocurrs_val=self.my_spec.minOccurs
        max_ocurrs_val=self.my_spec.maxOccurs
        
        if min_ocurrs_val == 1 and max_ocurrs_val == "unbounded":
            cardinality= "required"
            index = self.combo_mandatory.findText(cardinality)
        elif min_ocurrs_val == 0 and max_ocurrs_val == "unbounded":
            cardinality= "optional"
            index = self.combo_mandatory.findText(cardinality)
        elif min_ocurrs_val == 0 and max_ocurrs_val == 0:
            cardinality= "prohibited"
            index = self.combo_mandatory.findText(cardinality)
        else:
            Ops.msgError(self, "Cardinality Error","The cardinality of the imported IDS file cannot be read, it might be corrupt.")
        
        #Set combobox value depending on cardinality
        if index == -1:  # Value not found
            Ops.msgError(self, "Cardinality Error","The cardinality found does not match elements in comboBox")
        else:
            self.combo_mandatory.setCurrentIndex(index)
            print(f"Value '{cardinality}' set successfully in the combo box for{self.my_spec}")

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
        #Add populated specification to Specification list. Emit signal to method openSpecEditor in class IdsEditorWindow
        self.add_spec_to_list.emit()
        self.close()
        print(self.my_spec.name)

class IdsEditorWindow(QMainWindow):
    back_to_manage_ids= pyqtSignal()
    add_ids_to_list= pyqtSignal() #signal activated when clicking on "Save IDS" button in IdsEditorWindow

    def __init__(self, parent= None, my_ids=None ):
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
        # if self.my_ids is None:
        #     self.my_ids=IdsOps.createIds()
        # else:
        #     self.flag_load_data=True
        #     pass

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
        my_ids= self.my_ids
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.info_window = Ops.openSubWindow(self.mdi_list, IdsInfoWindow, self.info_window, None, my_ids_instance=my_ids)

        # if self.flag_load_data:
        #     self.loadInfo() #TODO: Get rid of this flag and the associated method as well
        # else:
        #     pass

    def openSpecListWindow(self):
        def setup_signals(window_instance):
            window_instance.open_spec_editor.connect(self.openSpecEditorWindow) #Receive signal emmited from IdsSpecListWindow Button:New / Button:Edit
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.spec_list_window = Ops.openSubWindow(self.mdi_list, IdsSpecListWindow, self.spec_list_window, setup_signals, my_ids_instance=self.my_ids)
     
    def openSpecEditorWindow(self):
        def setup_signals(window_instance):
            window_instance.add_spec_to_list.connect(self.spec_list_window.updateSpecList) #Receive signal emmited from IdsSpecEditorWindow Button:Save Specification
        hint = self.mdi_list.minimumSizeHint()
        self.mdi_list.resize(hint)
        self.mdi_editor.showMaximized()
        my_spec= self.spec_list_window.my_spec #retrieve my_spec from selected spec in SpecListWindow and pass it to new SpecEditorWindow 
        self.spec_list_window.spec_editor_window = Ops.openSubWindow(self.mdi_editor, IdsSpecEditorWindow, None, setup_signals=setup_signals, my_spec_instance= my_spec)

    def openAuditWindow(self):
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.audit_window = Ops.openSubWindow(self.mdi_list, IdsEditorAuditWindow, self.audit_window, None)
        self.generateIdsFile() #generate IDS file in temp_files folder each time Audit button is clicked
        self.runAudit() #Audit Report of IDS file
        
    def generateIdsFile(self):
        self.my_ids= IdsOps.createIds() #TODO: Add try catch, to handle when user clicks automatically in audit before clicking on info and specifications
        self.addIdsInfo()
        self.addIdsSpecifications()
        self.idsToXML()

    def idsToXML(self):
        filepath= constants.TEMP_IDS_DIR 
        self.my_ids.filepath= filepath
        self.my_ids.to_xml(filepath) #Convert IDS in xml structure and save it in filepath

    def runAudit(self):
        IdsOps.auditIds() #run c# script to run IDS Audit
        filepathLog= constants.TEMP_LOG_DIR
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
        self.add_ids_to_list.emit() #Emit signal to class ManageIdsWindow method updateIdsList to pass ids.Ids() Object
        self.close()
    
    def loadInfo(self):
        #TODO:Get rid of this method and check it does not affect something else
        pass
    
    def backIdsList(self):
        self.back_to_manage_ids.emit()
        self.close()

class IfcInfoWindow(QMainWindow):
    def __init__(self, parent=None, ifc_file_path:str="ifc_model.ifc"):
        super(IfcInfoWindow, self).__init__(parent)

        self.ifc_file_path=ifc_file_path
        self.my_IfcOps = IfcOps(self.ifc_file_path) #Instantiate class IfcOps
        self.my_model= self.my_IfcOps.model
        self.my_schema= self.my_model.schema

        # Load UI file
        Ops.load_ui("ifc_info_checker.ui",self)

        # Define Widgets
        main_widget_setup = {
            #Basic Information
            "txt_base_point": QLineEdit,
            "txt_coordinate_sys": QLineEdit,
            "txt_ifc_schema": QLineEdit,
            "txt_software": QLineEdit,
            "txt_num_elements": QLineEdit,
            "txt_list_attributes": QLineEdit,
            #Project-related Information
            "txt_prj_description": QLineEdit,
            "txt_section": QLineEdit,
            "txt_client": QLineEdit,
            "txt_author": QLineEdit,
            #Custom Query
            "combo_entity": QComboBox,
            "combo_instance": QComboBox,
            "combo_attribute": QComboBox,
            "combo_psets": QComboBox,
            "combo_props": QComboBox,
            "txt_value_att": QLineEdit,
            "txt_value_prop": QLineEdit,
            "btn_search": QPushButton,
            "btn_clear": QPushButton
        }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )

        # Connect handlers
        handlers = {
            #"btn_search": self.searchElements,
            "btn_clear": self.clearComboBxs
        }
        Ops.connectHandlers(self, handlers)
        
        #Connects Handlers for comboboxes
        self.combo_entity.currentIndexChanged.connect(self.updateInstances)
        self.combo_instance.currentIndexChanged.connect(self.updatePsets)
        self.combo_instance.currentIndexChanged.connect(self.updateAttributes)
        self.combo_psets.currentIndexChanged.connect(self.updateProps)
        self.combo_props.currentIndexChanged.connect(self.updateResultProp)
        self.combo_attribute.currentIndexChanged.connect(self.updateResultAtt)

        #Load Info for corresponding schema
        if self.my_schema=="IFC4":
            self.loadIfc4Info()
        elif self.my_schema == "IFC2X3":
            self.loadIfc2X3Info()
        else:
            print("IFC Schema not supported")
        self.loadEntities()

    def loadIfc4Info(self):
        #Basic Information
        self.txt_base_point.setText(str(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_BASE_POINT)))
        self.txt_coordinate_sys.setText("Descrip.: "+IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_CRS_DESCRIPTION)+
                                         " / Code: "+
                                        IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_CRS_NAME))
        self.txt_ifc_schema.setText(self.my_schema)
        self.txt_software.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_AUTHOR_SOFTWARE))
        self.txt_num_elements.setText("TODO")#TODO
        self.txt_list_attributes.setText("TODO")#TODO
        #Project-related Information
        self.txt_prj_description.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_DESCRIPTION)))
        self.txt_section.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_PHASE)))
        self.txt_client.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_ORG)))
        self.txt_author.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_LAST_NAME)+
                                 " , "+
                                 IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_FIRST_NAME))
    
    def loadIfc2X3Info(self):
        #Basic Information
        self.txt_base_point.setText(str(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_BASE_POINT)))
        self.txt_coordinate_sys.setText("IFC2X3 Schema does not incorportate IfcCoordinateReferenceSystem")
        self.txt_ifc_schema.setText(self.my_schema)
        self.txt_software.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_AUTHOR_SOFTWARE))
        self.txt_num_elements.setText("TODO")#TODO
        self.txt_list_attributes.setText("TODO")#TODO
        #Project-related Information
        self.txt_prj_description.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_DESCRIPTION)))
        self.txt_section.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_PHASE)))
        self.txt_client.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_ORG)))
        self.txt_author.setText("Last Name: "+IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_LAST_NAME)+
                                 " , First Name: "+
                                 IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_FIRST_NAME))
      
    def loadEntities(self):
        self.combo_entity.clear()
        entities = set()
        for entity in self.my_model.by_type('IfcRoot'):
            if hasattr(entity, 'IsDefinedBy'): #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcobject.htm Assignment of property sets : IsDefinedBy - a definition relationship IfcRelDefinesByProperties that assignes property set definitions to the object occurrence.
                entities.add(entity.is_a())
        self.combo_entity.addItems(sorted(entities))

    def updateInstances(self):
        self.combo_instance.clear()
        entity_type = self.combo_entity.currentText()
        if entity_type:
            instances = self.my_model.by_type(entity_type)
            instance_ids = [str(instance.get_info()["GlobalId"]) for instance in instances]
            self.combo_instance.addItems(instance_ids)

    def updatePsets(self):
        self.combo_psets.clear()
        instance_id = self.combo_instance.currentText()
        if instance_id:
            instance = self.my_model.by_guid(instance_id)
            # Iterate through the IsDefinedBy relationships
            self.psets_dict={}
            for definition in instance.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcPropertySet'):
                        props_dict={}
                        for prop in property_set.HasProperties:
                            prop_value = '<not handled>'
                            if prop.is_a('IfcPropertySingleValue'):
                                prop_value = str(prop.NominalValue.wrappedValue)
                                props_dict[prop.Name]= prop_value
                        self.psets_dict[property_set.Name] = props_dict

            self.combo_psets.addItems(self.psets_dict.keys())
    
    def updateProps(self):
        self.combo_props.clear()
        pset_name = self.combo_psets.currentText()
        if pset_name:
            props_names = [prop for prop in self.psets_dict[pset_name].keys()]
            self.combo_props.addItems(props_names)

    def updateResultProp(self):
        pset_name = self.combo_psets.currentText()
        prop_name= self.combo_props.currentText()
        if prop_name and pset_name:
            value = self.psets_dict[pset_name][prop_name]
            self.txt_value_prop.setText(str(value))

    def updateAttributes(self):
        self.combo_attribute.clear()
        instance_id = self.combo_instance.currentText()
        if instance_id:
            instance = self.my_model.by_guid(instance_id)
            attributes = [attr for attr in instance.get_info(recursive=True).keys()]
            self.combo_attribute.addItems(attributes)

    def updateResultAtt(self):
        instance_id = self.combo_instance.currentText()
        attribute = self.combo_attribute.currentText()
        if instance_id and attribute:
            instance = self.my_model.by_guid(instance_id)
            value = getattr(instance, attribute, None)
            self.txt_value_att.setText(str(value))


    def clearComboBxs(self):
        pass

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
            "btn_delete_ifc": self.clickDelete,
            "btn_check_ifc": self.checkIfc
        }
        Ops.connectHandlers(self, handlers)

        #Set instance of IfcCheckerWindow
        self.ifc_checker_window=None
    
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
    
    def checkIfc(self):
        ifc_file_path= self.list_ifc.currentIndex().data()
        if ifc_file_path:
            self.ifc_checker_window=Ops.openWindow(IfcInfoWindow,window_instance=None,setup_signals=None, ifc_file_path=ifc_file_path)
            self.ifc_checker_window.show()
        pass

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
        xml_as_dict=self.parseXmlToDict()
        my_ids= IdsOps.parseDictToIds(xml_as_dict)
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
            else: print(f"filepath already in list. {self.file_path}")
        else:
            print("No file selected to save")

    def updateIdsList(self):
        my_ids = self.idsEditor_window.my_ids
        self.setFilepathIds(my_ids)
        item= my_ids.filepath
         # Check if the item already exists in the dictionary, Find and remove the existing item from the list widget 
        # TODO:uuid not supported by IDS schema, which approach for replacing elements in list, Just string translation?
        if item in self.dic_ids:
            matching_items = self.list_ids_mgmnt.findItems(item, Qt.MatchExactly)
            for match in matching_items:
                row = self.list_ids_mgmnt.row(match)
                self.list_ids_mgmnt.takeItem(row)

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
    
    def parseXmlToDict(self):
        file_path= self.list_ids_mgmnt.currentIndex().data()
        if file_path:
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
            Ops.msgError(self, "Error","You have not uploaded any files yet")

    def show_main_window(self):
        self.show()

    def clearMdiArea(self):
        self.mdi_main.closeAllSubWindows() #TODO:add argument in clearMdiArea with name of mdi. NoneType error triggered??

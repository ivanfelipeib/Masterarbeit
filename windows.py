from PyQt5.QtWidgets import (QTableWidget, QMainWindow,QApplication, QPushButton, QMdiArea, QComboBox,
                             QFileDialog, QMessageBox, QMdiSubWindow,QLineEdit, QPlainTextEdit,QDateEdit,
                             QTextBrowser, QDialog, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal, QVariant, QDate
from PyQt5.QtGui import QCursor
from myWidgets import CustomListWidget
from Operations.Ops import Ops
from Operations.idsOps import IdsOps
from Operations.ifcOps import IfcOps
from ifctester import ids
import os
import filters 
import uuid
import shutil
import constants
import pandas as pd

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
        destination_file, _ = QFileDialog.getSaveFileName(self, "Select destination filepath", "", "Text files (*.txt)", options=options)
        if destination_file:
            print(f"Destination file path: {destination_file}")
            try:
                shutil.copy(constants.TEMP_LOG_DIR, destination_file) #copy file from Temp folder to selected filepath
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

        if self.my_ids: #Load data if ids was passed
            self.loadData(self.my_ids)
        else: #Load default values
            self.txt_author.setText("This field requires an email address e.g. author@mail.com")
            self.txt_version.setText("1.0")
            current_date = QDate.currentDate()
            self.date.setDisplayFormat("dd/MM/yyyy")
            self.date.setDate(current_date)
            
    
    def loadData(self, ids_instance:ids.Ids):
        self.txt_title.setText(ids_instance.info.get("title", ""))
        self.txt_copyright.setText(ids_instance.info.get("copyright", ""))
        self.txt_version.setText(ids_instance.info.get("version", ""))
        self.txt_author.setText(ids_instance.info.get("author", ""))
        self.txt_description.setPlainText(ids_instance.info.get("description", ""))
        self.txt_purpose.setPlainText(ids_instance.info.get("purpose", ""))
        self.txt_milestone.setPlainText(ids_instance.info.get("milestone", ""))

        date=Ops.stringToDateFormat(ids_instance.info.get("date", ""))
        self.date.setDisplayFormat("dd/MM/yyyy")
        self.date.setDate(date)

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
        #Define ids, spec and spec_in_edition
        self.my_ids = my_ids
        self.my_spec = my_spec
        self.spec_in_edition=None

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
    
    def loadSpec(self, ids_instance:ids.Ids):
        idsToLoad=ids_instance
        specifications = idsToLoad.specifications
        for spec in specifications:
            item= spec.name
            self.dic_specifications[item]=spec
            self.list_ids_spec.addItem(item)

    def clickNew(self):
        self.my_spec=None
        self.open_spec_editor.emit()
    
    def clickDelete(self):
        if Ops.checkIfElementSelected(self, self.list_ids_spec):
            index = self.list_ids_spec.selectedIndexes()[0]  # Assuming single selection
            item = index.data()
            if index.isValid() and item != self.spec_in_edition:
                spec = self.dic_specifications.pop(item)  # Remove the entry and get the associated object
                self.list_ids_spec.model().removeRow(index.row())
                del spec
                self.list_ids_spec.maxFileList+=1
            else:
                Ops.msgError(self, "Error", "Item in edition cannot be deleted")
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to delete.") 

    def clickEdit(self):
        if Ops.checkIfElementSelected(self, self.list_ids_spec):
            index = self.list_ids_spec.selectedIndexes()[0]  # Assuming single selection
            if index.isValid():
                item = index.data()
                self.spec_in_edition=item
                self.my_spec = self.dic_specifications[item]
            self.list_ids_spec.clearSelection()
            self.open_spec_editor.emit()
        else:
           Ops.msgError(self, "Selection Error", "There is no item selected to edit.") 
    
    def updateSpecList(self):
        #Save specification in List in SpecListWindow
        self.spec_in_edition=None
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
        self.opened_filter=None
        self.opened_requirement=None
        self.my_spec= my_spec
        #Set dictionaries to storage entries in lists (Key= facet string, Value= facet).
        self.dic_requirements={}
        self.dic_filters={}
        #Set elements to handle facet in edition
        self.filter_in_edition=None
        self.requirement_in_edition=None

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
            "btn_edit_filter": self.loadFilterSubWindow,
            "btn_edit_requirement": self.loadReqSubWindow,
            "btn_delete_filter": self.clickDeleteFilter,
            "btn_delete_requirement": self.clickDeleteRequirement,
            "btn_save_specification": self.saveSpecification
        }
        Ops.connectHandlers(self, handlers)

    def openFilterSubWindow(self, text, facet_to_load = None):
        mdi_area = self.mdi_filter
        mdi_area.closeAllSubWindows()
        facet_to_load=facet_to_load

        match text:
            case "Add filter by class":
                self.opened_filter =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by part of":
                self.opened_filter = Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by attribute":
                self.opened_filter = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by property":
                self.opened_filter =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by classification":
                self.opened_filter = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add filter by material":
                self.opened_filter = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case _:
                Ops.msgError(self, "Error","Text in ComboBox does not match any type of filter")
        
        if text != "Add filter by class": # In Applicability section, there's one cardinality for all facets. Individual cardinality comboBox hide
            self.opened_filter.combo_optionality.hide()
            self.opened_filter.lbl_optionality.hide()
        else: pass

    def openRequirementSubWindow(self, text, facet_to_load=None):
        mdi_area = self.mdi_requirement
        mdi_area.closeAllSubWindows()
        facet_to_load=facet_to_load

        match text:
            case "Add requirement by class":
                self.opened_requirement =  Ops.openSubWindow(mdi_area, filters.byClass, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by part of":
                self.opened_requirement= Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by attribute":
                self.opened_requirement = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by property":
                self.opened_requirement =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by classification":
                self.opened_requirement = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case "Add requirement by material":
                self.opened_requirement = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None,my_facet_instance=facet_to_load)
            case _:
                Ops.msgError(self, "Error","Text in ComboBox does not match any type of requirements")
        
    def save_requirements_data(self):
        if not self.mdi_requirement.subWindowList() or not self.opened_requirement:
            Ops.msgError(self, "Error", "There is no requirement in edition. Please select a requirement type from the dropdown list.")
        else:
            dict_data = self.opened_requirement.getData() #access windows in filter.py and calls getData depending on window

            if not IdsOps.checkExistingEntityFacet(self.dic_requirements) or IdsOps.getExistingEntityFacet(self.dic_requirements) == self.requirement_in_edition:#Raised error if entity facet already exist in requirements
                if dict_data["info_required"]: #If True required information was provided in filter
                    dict_data.pop('info_required', None) #Delete flag from dictionary since check of required info has been made
                    #Create new facet
                    current_text = self.combo_add_requirement.currentText()
                    facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data)
                    if isinstance(facet, ids.Entity):
                        item= IdsOps.entityToString(facet, "requirement") # special to_string for Entity type, since ifcOpensShell failed / Entity facet in requirements MUST be required not prohibited or optional https://github.com/buildingSMART/IDS/blob/development/Documentation/facet-configurations.md
                    else:
                        item= facet.to_string(clause_type= "requirement", specification=self.my_spec, requirement=facet)
                    
                    #if there was and element in edition, delete old element from dictionary and list for adding edited element
                    if self.requirement_in_edition:
                        del self.dic_requirements[self.requirement_in_edition]
                        Ops.deleteItemInList(self,"list_requirements", self.requirement_in_edition)
                        self.requirement_in_edition= None

                    #Add newfacet to dictionary and list
                    self.dic_requirements[item]= facet
                    self.list_requirements.addItem(item)
                    self.opened_requirement.close()
                    self.opened_requirement = None
                    self.mdi_requirement.closeAllSubWindows()
                else:
                    Ops.msgError(self, "Missing Information", "All the fields marked as required must be provided. Required information is marked with (*)")
            else:
                Ops.msgError(self, "Existing entity facet", "An entity facet already exists. Only one entity facet is allowed.")

    def save_filters_data(self):
        if not self.mdi_filter.subWindowList() or not self.opened_filter:
            Ops.msgError(self, "Error", "There is no filter in edition. Please select a filter type from the dropdown list.")
        else:
            dict_data = self.opened_filter.getData()
            if not IdsOps.checkExistingEntityFacet(self.dic_filters) or IdsOps.getExistingEntityFacet(self.dic_filters) == self.filter_in_edition: #Raised error if entity facet already exist ina applicability
                if dict_data["info_required"]:#If required information was provided in requirement add requirement in list
                    dict_data.pop('info_required', None) #Delete flag from dictionary since check of required info has been made
                    #Create new facet
                    current_text = self.combo_add_filter.currentText()
                    cardinality = self.combo_mandatory.currentText()
                    facet= IdsOps.createFacet(spec_type= current_text, dict_data= dict_data, is_filter= True, cardinality_filter= cardinality)
                    if isinstance(facet, ids.Entity):
                        item= IdsOps.entityToString(facet,"applicability")
                    else:
                        item= facet.to_string(clause_type= "applicability", specification=self.my_spec, requirement=None)

                    #if there was and element in edition, delete element from dictionary and list
                    if self.filter_in_edition:
                        del self.dic_filters[self.filter_in_edition]
                        Ops.deleteItemInList(self,"list_filters", self.filter_in_edition)
                        self.filter_in_edition= None

                    self.dic_filters[item]= facet
                    self.list_filters.addItem(item)
                    self.opened_filter.close()
                    self.opened_filter = None
                    self.mdi_filter.closeAllSubWindows()
                else:
                    Ops.msgError(self, "Missing Information", "All the fields marked as required must be provided. Required information is marked with (*)")
            else:
                Ops.msgError(self, "Existing entity facet", "An entity facet already exists. Only one entity facet is allowed.")

    def clickDeleteRequirement(self):
        if Ops.checkIfElementSelected(self, self.list_requirements):
            index = self.list_requirements.selectedIndexes()[0]  # Assuming single selection
            item = index.data()
            if index.isValid()and item != self.requirement_in_edition:
                facet = self.dic_requirements.pop(item)  # Remove the entry and get the associated object
                self.list_requirements.model().removeRow(index.row())
                del facet
                self.list_requirements.maxFileList+=1
            else:
                Ops.msgError(self, "Error", "Item in edition cannot be deleted")
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to delete.")

    def clickDeleteFilter(self):
        if Ops.checkIfElementSelected(self, self.list_filters):
            index = self.list_filters.selectedIndexes()[0]  # Assuming single selection
            item = index.data()
            if index.isValid() and item != self.filter_in_edition:
                facet = self.dic_filters.pop(item)  # Remove the entry and get the associated object
                self.list_filters.model().removeRow(index.row())
                del facet
                self.list_filters.maxFileList+=1
            else:
                Ops.msgError(self, "Error", "Item in edition cannot be deleted")
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to delete.")
    
    def loadRequirementsList(self):
        for requirement_load in self.my_spec.requirements:
            if isinstance(requirement_load,ids.Entity):
                item= IdsOps.entityToString(requirement_load, "requirement")
                self.dic_requirements[item]= requirement_load
                self.list_requirements.addItem(item)
                print(self.dic_requirements)
            else:
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
        if isinstance(ifc_version,list): #IDS Version may come as [IFC2X3], in this case access element in list
            ifc_version=ifc_version[0]
        Ops.setTextComboBox(self,"combo_ifc_version", ifc_version)
    
    def loadReqSubWindow(self):
        if Ops.checkIfElementSelected(self, self.list_requirements):
            index = self.list_requirements.selectedIndexes()[0]  # Assuming single selection
            if index.isValid():
                item = index.data()
                self.requirement_in_edition = item #Store item(facet) in edition to delete it from the list and add updated item
                req_selected = self.dic_requirements[item]
                facet_class = type(req_selected).__name__.lower() #retrieve class as a lowercase string
                #handle facet name to match element in ComboBox(combo_add_requirement)
                if facet_class=="entity":
                    facet_class = "class"
                elif facet_class=="partof":
                    facet_class = "part of"
                text = "Add requirement by "+ facet_class
                Ops.setTextComboBox(self, "combo_add_requirement", text)#Set value of combobox with type of requirements to the corresponding type of selected requirement
            self.openRequirementSubWindow(text, req_selected)
            self.list_requirements.clearSelection()
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected for editing.")

    def loadFilterSubWindow(self):
        if Ops.checkIfElementSelected(self, self.list_filters):
            index = self.list_filters.selectedIndexes()[0]  # Assuming single selection
            if index.isValid():
                item = index.data()
                self.filter_in_edition = item #Store item in edition to delete it from the list and add updated item
                filter_selected = self.dic_filters[item]
                facet_class = type(filter_selected).__name__.lower() #retrieve class as a lowercase string
                if facet_class=="entity":
                    facet_class = "class"
                text = "Add filter by "+ facet_class
                Ops.setTextComboBox(self, "combo_add_filter", text) #Set value of combobox with type of filters to the corresponding type of selected filter
            self.openFilterSubWindow(text, filter_selected)
            self.list_filters.clearSelection()
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected for editing.") 
    
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
        if self.txt_name.text() and self.list_filters.count() > 0:
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
        else:
            Ops.msgError(self,"Specification Error", "Please check that the required information marked with (*) has been provided. A specification must have at least one item in the applicability section")

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
        #Hide buttons when loading Window to ensure the progressive filling of the IDS attributes (Back Btn and Ids Info Button visible)
        self.btn_ids_specifications.hide()
        self.btn_ids_audit.hide()
        self.btn_ids_save.hide()

        #Create instance of Subwindows
        self.info_window=None
        self.spec_list_window=None
        self.audit_window= None

        self.my_ids= my_ids # Instantiate ids, None as default in constructor if no ids was passed
        
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

        Ops.msgError(self, "Warning", "To proceed with the IDS authoring process, all the fields marked as required must be provided. Required information is marked with *.")
        self.btn_ids_specifications.show()

    def openSpecListWindow(self):
        def setup_signals(window_instance):
            window_instance.open_spec_editor.connect(self.openSpecEditorWindow) #Connect signal emmited from IdsSpecListWindow Button:New / Button:Edit
        self.mdi_editor.hide()
        self.mdi_list.resize(800,832)
        self.spec_list_window = Ops.openSubWindow(self.mdi_list, IdsSpecListWindow, self.spec_list_window, setup_signals, my_ids_instance=self.my_ids)
        self.btn_ids_audit.show()
     
    def openSpecEditorWindow(self):
        def setup_signals(window_instance):
            window_instance.add_spec_to_list.connect(self.spec_list_window.updateSpecList) #Receive signal emmited from IdsSpecEditorWindow Button:Save Specification
        hint = self.mdi_list.minimumSizeHint()
        self.mdi_list.resize(hint)
        self.mdi_editor.showMaximized()
        my_spec= self.spec_list_window.my_spec #retrieve my_spec from selected spec in SpecListWindow and pass it to new SpecEditorWindow 
        self.spec_list_window.spec_editor_window = Ops.openSubWindow(self.mdi_editor, IdsSpecEditorWindow, None, setup_signals=setup_signals, my_spec_instance= my_spec)

    def openAuditWindow(self):
        if not self.info_window.txt_title.text() or not self.info_window.txt_version.text() or not self.info_window.txt_author.text():
            Ops.msgError(self, "IDS Information: missing information", "To proceed with the IDS audit process, all the fields marked as required must be provided. Required information in marked with *.")
        elif not Ops.isValidEmail(self.info_window.txt_author.text()):
            Ops.msgError(self, "IDS Information: Email required", "Field author requires a valid email address")
        elif self.spec_list_window.list_ids_spec.count() == 0:
            Ops.msgError(self, "IDS Specifications:", "The current IDS file has no specifications, add at least one specification before proceeding with the IDS audit process")
        else:
            self.mdi_editor.hide()
            self.mdi_list.resize(800,832)
            self.audit_window = Ops.openSubWindow(self.mdi_list, IdsEditorAuditWindow, self.audit_window, None)
            self.generateIdsFile() #generate IDS file in temp_files folder each time Audit button is clicked
            self.runAudit() 
            self.btn_ids_save.show()

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
        IdsOps.auditIds() #run c# script to run IDS Audit
        filepathLog= constants.TEMP_LOG_DIR

        IdsOps.idsQualityReport(self.my_ids,filepathLog) #acces base report from c# Script and structure quality report

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
        if not self.info_window.txt_title.text() or not self.info_window.txt_version.text() or not self.info_window.txt_author.text():
            Ops.msgError(self, "IDS Information: missing information", "IDS cannot be saved, required information is missing. All the fields marked as required must be provided, required information is marked with *.")
        elif not Ops.isValidEmail(self.info_window.txt_author.text()):
            Ops.msgError(self, "IDS Information: Email required", "Field author requires a valid email address")
        elif self.spec_list_window.list_ids_spec.count() == 0:
            Ops.msgError(self, "IDS Specifications:", "The current IDS file has no specifications, add at least one specification before proceeding.")
        else:
            self.generateIdsFile()
            self.setFilePathIds()
    
    def setFilePathIds(self):
        self.filter="IDS files (*.ids)"
        self.title= "Save IDS file"
        self.fileDialog = QFileDialog()
        self.fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        self.file_path, _ = self.fileDialog.getSaveFileName(None, self.title, "", self.filter)
        if self.file_path:
            self.add_ids_to_list.emit() #Emit signal to class ManageIdsWindow method updateIdsList to pass ids.Ids() Object
            self.close()
        else:
            Ops.msgError(self,"Error", "The process was interrupted, the IDS file has not been saved")

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
        self.flag_psets=False #True if instance in customquery has Psets
        self.nested_entity=None #Handle nested entities in custom search

        # Load UI file
        Ops.load_ui("ifc_info_checker.ui",self)

        # Define Widgets
        main_widget_setup = {
            "lbl_ifc_title": QLabel,
            #Basic Information
            "txt_base_point": QLineEdit,
            "txt_coordinate_sys": QLineEdit,
            "txt_latitude": QLineEdit,
            "txt_longitude": QLineEdit,
            "txt_ifc_schema": QLineEdit,
            "txt_software": QLineEdit,
            "txt_objects_number": QLineEdit,
            #Project-related Information
            "txt_prj_description": QLineEdit,
            "txt_phase": QLineEdit,
            "txt_organization": QLineEdit,
            "txt_author": QLineEdit,
            #Custom Query
            "combo_entity": QComboBox,
            "combo_instance": QComboBox,
            "combo_instance_name": QComboBox,
            "combo_attribute": QComboBox,
            "combo_psets": QComboBox,
            "combo_props": QComboBox,
            "txt_value_att": QLineEdit,
            "txt_value_prop": QLineEdit,
            "btn_report": QPushButton
        }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )

        #Connects Handlers for comboboxes
        self.combo_entity.currentIndexChanged.connect(self.updateInstancesIds)
        self.combo_instance.currentIndexChanged.connect(self.updatePsets)
        self.combo_instance.currentIndexChanged.connect(self.updateAttributes)
        self.combo_psets.currentIndexChanged.connect(self.updateProps)
        self.combo_props.currentIndexChanged.connect(self.updateResultProp)
        self.combo_attribute.currentIndexChanged.connect(self.updateResultAtt)
        self.txt_value_att.mousePressEvent = self.handleLink
        self.btn_report.clicked.connect(self.generateExcelRepot)

        #Load Info for corresponding schema
        if self.my_schema=="IFC4":
            self.loadIfc4Info()
            self.loadEntities()
        elif self.my_schema == "IFC2X3":
            self.loadIfc2X3Info()
            self.loadEntities()
        else:
            Ops.msgError(self,"IFC Schema not supported", "The file is not supported. Make sure you are using a file with schemas IFC4 or IFC2x3")
            self.close()
        

    def loadIfc4Info(self):
        #Title
        self.lbl_ifc_title.setText(f"IFC File: {os.path.basename(self.ifc_file_path)}")
        #Basic Information
        self.txt_base_point.setText(str(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_BASE_POINT)))
        self.txt_coordinate_sys.setText("Descrip.: "+IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_CRS_DESCRIPTION)+
                                         " / Code: "+
                                        IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_CRS_NAME))
        self.txt_latitude.setText(Ops.formatLatLong(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_REF_LATITUDE)))
        self.txt_longitude.setText(Ops.formatLatLong(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_REF_LONGITUDE)))
        self.txt_ifc_schema.setText(self.my_schema)
        self.txt_software.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_AUTHOR_SOFTWARE))
        self.txt_objects_number.setText(IfcOps.numberElementbyEntity(self.my_IfcOps,"IfcElement")) #IfcElement for physically existing objects / IfcProduct for hat can be spatially located in a building model

        #Project-related Information
        self.txt_prj_description.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_DESCRIPTION)))
        self.txt_phase.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_PHASE)))
        self.txt_organization.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_ORG)))
        self.txt_author.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_LAST_NAME)+
                                 " , "+
                                 IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_FIRST_NAME))
    
    def loadIfc2X3Info(self):
        #Title
        self.lbl_ifc_title.setText(f"IFC File: {os.path.basename(self.ifc_file_path)}")
        #Basic Information
        self.txt_base_point.setText(str(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_BASE_POINT)))
        self.txt_coordinate_sys.setText("IFC2X3 Schema does not incorportate IfcCoordinateReferenceSystem")
        self.txt_latitude.setText(Ops.formatLatLong(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_REF_LATITUDE)))
        self.txt_longitude.setText(Ops.formatLatLong(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_REF_LONGITUDE)))
        self.txt_ifc_schema.setText(self.my_schema)
        self.txt_software.setText(IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_AUTHOR_SOFTWARE))
        self.txt_objects_number.setText(IfcOps.numberElementbyEntity(self.my_IfcOps,"IfcElement")) #IfcElement for physically existing objects / IfcProduct for hat can be spatially located in a building model
  
        #Project-related Information
        self.txt_prj_description.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_DESCRIPTION)))
        self.txt_phase.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_PHASE)))
        self.txt_organization.setText((IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_ORG)))
        self.txt_author.setText("Last Name: "+IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_LAST_NAME)+
                                 " , First Name: "+
                                 IfcOps.getInfoFromEntity(self.my_IfcOps,constants.IFC_PROJ_OWNER_AUTHOR_FIRST_NAME))
      
    def loadEntities(self):
        self.combo_entity.clear()
        entities = set()
        for entity in self.my_model.by_type('IfcElement'): #Includes IfcElement (Elements are physically existent objects, although they might be void elements, such as holes) https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/schema/ifcproductextension/lexical/ifcelement.htm
            entities.add(entity.is_a())
        self.combo_entity.addItems(sorted(entities))
        
    def updateInstancesIds(self):
        self.combo_instance.clear()
        entity_type = self.combo_entity.currentText()
        if entity_type:
            instances = self.my_model.by_type(entity_type)
            instance_ids = [str(instance.get_info()["GlobalId"])+" - "+str(instance.get_info()["Name"]) for instance in instances]
            self.combo_instance.addItems(instance_ids)

    def updatePsets(self):
        self.combo_psets.clear()
        instance_id= self.combo_instance.currentText().split(" - ")[0]
        if instance_id:
            instance = self.my_model.by_guid(instance_id)
            if self.my_schema=="IFC4":
                if hasattr(instance, 'IsDefinedBy'): #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcobject.htm Assignment of property sets : IsDefinedBy - a definition relationship IfcRelDefinesByProperties that assignes property set definitions to the object occurrence.
                    self.flag_psets=True
                    self.psets_dict={}

                    for definition in instance.IsDefinedBy: #Assignment of property sets in IFcObject through IsDefinedBy
                        #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD1/HTML/schema/ifckernel/lexical/ifcreldefinesbyproperties.htm
                        if definition.is_a('IfcRelDefinesByProperties'): 
                            property_set = definition.RelatingPropertyDefinition
                            if property_set.is_a('IfcPropertySet') and property_set.HasProperties is not None:
                                props_dict={}
                                for prop in property_set.HasProperties:
                                    prop_value = '<not handled>'
                                    if prop.is_a('IfcPropertySingleValue'):
                                        prop_value = str(prop.NominalValue.wrappedValue)
                                        props_dict[prop.Name]= prop_value
                                    elif prop.is_a('IfcPropertyListValue'):
                                        prop_value = str(prop)
                                        props_dict[prop.Name]= prop_value
                                    elif prop.is_a('IfcPropertyEnumeratedValue'):
                                        prop_value = str(prop)
                                        props_dict[prop.Name]= prop_value
                                self.psets_dict[property_set.Name] = props_dict

                    for definition in instance.IsTypedBy: #Assignment of a type in IFcObject through IsDefinedBy (from IFC SChema IFC4 onwards)
                        #https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifckernel/lexical/ifcreldefinesbytype.htm
                        if definition.is_a('IfcRelDefinesByType'): 
                            object_type = definition.RelatingType
                            if object_type.is_a('IfcTypeObject') and object_type.HasPropertySets is not None:
                                for property_set in object_type.HasPropertySets:
                                    props_dict={}
                                    for prop in property_set.HasProperties:
                                        prop_value = '<not handled>'
                                        if prop.is_a('IfcPropertySingleValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                        elif prop.is_a('IfcPropertyListValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                        elif prop.is_a('IfcPropertyEnumeratedValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                    self.psets_dict[property_set.Name +" (Type)"] = props_dict

                    self.combo_psets.addItems(self.psets_dict.keys())

            elif self.my_schema=="IFC2X3":
                if hasattr(instance, 'IsDefinedBy'): #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcobject.htm Assignment of property sets : IsDefinedBy - a definition relationship IfcRelDefinesByProperties that assignes property set definitions to the object occurrence.
                    self.flag_psets=True
                    # Iterate through the IsDefinedBy relationships
                    self.psets_dict={}
                    for definition in instance.IsDefinedBy: #Assignment of property sets in IFcObject through IsDefinedBy
                        # Add PSets and Props allocated in object itself
                        #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD1/HTML/schema/ifckernel/lexical/ifcreldefinesbyproperties.htm
                        if definition.is_a('IfcRelDefinesByProperties'): 
                            property_set = definition.RelatingPropertyDefinition
                            if property_set.is_a('IfcPropertySet') and property_set.HasProperties is not None:
                                props_dict={}
                                for prop in property_set.HasProperties:
                                    prop_value = '<not handled>'
                                    if prop.is_a('IfcPropertySingleValue'):
                                        prop_value = str(prop.NominalValue.wrappedValue)
                                        props_dict[prop.Name]= prop_value
                                    elif prop.is_a('IfcPropertyListValue'):
                                        prop_value = str(prop.NominalValue.wrappedValue)
                                        props_dict[prop.Name]= prop_value
                                    elif prop.is_a('IfcPropertyEnumeratedValue'):
                                        prop_value = str(prop.NominalValue.wrappedValue)
                                        props_dict[prop.Name]= prop_value
                                self.psets_dict[property_set.Name] = props_dict

                        # Add PSets and Props allocated within the object type definition 
                        #https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifckernel/lexical/ifcreldefinesbytype.htm
                        if definition.is_a('IfcRelDefinesByType'): 
                            object_type = definition.RelatingType
                            if object_type.is_a('IfcTypeObject') and object_type.HasPropertySets is not None:
                                for property_set in object_type.HasPropertySets:
                                    props_dict={}
                                    for prop in property_set.HasProperties:
                                        prop_value = '<not handled>'
                                        if prop.is_a('IfcPropertySingleValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                        elif prop.is_a('IfcPropertyListValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                        elif prop.is_a('IfcPropertyEnumeratedValue'):
                                            prop_value = str(prop.NominalValue.wrappedValue)
                                            props_dict[prop.Name]= prop_value
                                    self.psets_dict[property_set.Name +" (Type)"] = props_dict

                    self.combo_psets.addItems(self.psets_dict.keys())
            else:
                self.flag_psets=False
                value= f"Selected element does not have associated PSets"
                self.combo_psets.addItem(value)
                self.txt_value_prop.setText("")
                self.psets_dict={}
    
    def updateProps(self):
        self.combo_props.clear()
        pset_name = self.combo_psets.currentText()
        if pset_name and self.flag_psets: # If flag_psets is True, retrieve props otherwise not
            props_names = [prop for prop in self.psets_dict[pset_name].keys()]
            self.combo_props.addItems(props_names)

    def updateResultProp(self):
        pset_name = self.combo_psets.currentText()
        prop_name= self.combo_props.currentText()
        if prop_name and pset_name and self.flag_psets:
            value = self.psets_dict[pset_name][prop_name]
            self.txt_value_prop.setText(str(value))

    def updateAttributes(self):
        self.combo_attribute.clear()
        instance_id = self.combo_instance.currentText().split(" - ")[0]
        if instance_id:
            instance = self.my_model.by_guid(instance_id)
            self.attributes = [attr for attr in instance.get_info(recursive=True).keys()]
            self.combo_attribute.addItems(self.attributes)

    def updateResultAtt(self):
        instance_id = self.combo_instance.currentText().split(" - ")[0]
        attribute = self.combo_attribute.currentText()
        if instance_id and attribute:
            instance = self.my_model.by_guid(instance_id)
            #value = getattr(instance, attribute, None)
            value = instance.get_info(recursive=True)[attribute]
            if isinstance(value, dict):
                self.txt_value_att.setText(f"{instance.Name} has nested information")
                self.txt_value_att.setCursor(QCursor(Qt.PointingHandCursor))
                self.txt_value_att.setStyleSheet("QLineEdit { color: blue; }")
                self.nested_entity=value
            else:
                self.txt_value_att.setCursor(QCursor(Qt.ArrowCursor))
                self.txt_value_att.setStyleSheet("")
                self.txt_value_att.setText(str(value))
                self.nested_entity=None
    
    def showNestedEntity(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nested Entity Contents")
        
        plainTextEdit = QPlainTextEdit(dialog)
        formatted_text = Ops.formatDictionary(self.nested_entity)
        plainTextEdit.setPlainText(formatted_text)
        plainTextEdit.setReadOnly(True)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(plainTextEdit)
        dialog.setLayout(layout)
        
        dialog.exec_()
    
    def handleLink(self, event):
        if self.nested_entity and isinstance(self.nested_entity, dict):
            self.showNestedEntity()
    
    def generateDataDict(self):
        entity = self.combo_entity.currentText()
        element = self.combo_instance.currentText()
        basic_info={"base_point":self.txt_base_point.text(),
                    "coord_system": self.txt_coordinate_sys.text(),
                    "latitude": self.txt_latitude.text(),
                     "longitude": self.txt_longitude.text(),
                     "ifc_schema": self.txt_ifc_schema.text(),
                     "software": self.txt_software.text(),
                     "objects_num": self.txt_objects_number.text()
                     }
        project_info={"description":self.txt_prj_description.text(),
                      "phase":self.txt_phase.text(),
                      "organization": self.txt_organization.text(),
                      "author": self.txt_author.text()
                      }
        ifc_info={"File": self.ifc_file_path,
                   "Entity":entity,
                   "Element": element,
                   "Attributes":self.attributes,
                   "PSets": self.psets_dict
                   }
        data={"basic_info":basic_info,
              "project_info": project_info,
              "ifc_info": ifc_info}

        return(data)
    
    def generateExcelRepot(self):
        data=self.generateDataDict()
        filepath=Ops.filePathExport(self)
        IfcOps.generateExcelReport(self, filepath, data)
       

class ManageIfcWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ManageIfcWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("ifc_manage.ui",self)

        # Define Widgets
        main_widget_setup = {
            "btn_import_ifc": QPushButton,
            "btn_delete_ifc": QPushButton,
            "list_ifc": CustomListWidget
        }
        # Load Widgets
        Ops.loadWidgets(self, main_widget_setup )
        self.list_ifc.type_restriction=".ifc" #constrain drag and drop just to ifc files

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
        if Ops.checkIfElementSelected(self, self.list_ifc):
            #Grabs selected row or current row in List and deletes it
            row= self.list_ifc.currentRow()
            self.list_ifc.takeItem(row)
            #Updates maxFileList value
            self.list_ifc.maxFileList+=1
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to delete.")
    
    def checkIfc(self):
        if Ops.checkIfElementSelected(self, self.list_ifc):
            ifc_file_path= self.list_ifc.currentIndex().data()
            if ifc_file_path:
                self.ifc_checker_window=Ops.openWindow(IfcInfoWindow,window_instance=None,setup_signals=None, ifc_file_path=ifc_file_path)
                self.ifc_checker_window.show()
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to check.")

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
        self.list_ids_mgmnt.type_restriction=".ids" #constrain drag and drop just to IDS files

        self.idsEditor_window=None #Create instance of Subwindows
        self.ids_in_edition= None #Instantiate IDS in edition

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
        self.filter="IDS-Files (*.ids)"
        self.title= "Open"
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
            self.msgError.setText("You cannot import more than 10 IFC files")
            self.msgError.show()
    
    def clickDelete(self):
        if Ops.checkIfElementSelected(self, self.list_ids_mgmnt):
            if self.idsEditor_window and not self.idsEditor_window.isVisible():
                self.ids_in_edition=None
            if Ops.checkIfElementSelected(self, self.list_ids_mgmnt):
                selected_indexes = self.list_ids_mgmnt.selectedIndexes()
                selection=selected_indexes[0].data()
                if selection != self.ids_in_edition:
                    #Grabs selected row or current row in List and deletes it
                    row= self.list_ids_mgmnt.currentRow()
                    self.list_ids_mgmnt.takeItem(row)
                    self.list_ids_mgmnt.maxFileList+=1
                else:
                    Ops.msgError(self, "Error", "Item in edition cannot be deleted")
            else:
                Ops.msgError(self, "Selection Error", "There is no item selected to delete.")
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected to delete.")           
    
    def clickNewEditorWindow(self): 
        self.ids_in_edition=None
        self.idsEditor_window = IdsEditorWindow(my_ids=None) #Pass my_ids as None when clicking on New
        self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds) #Connect signal of "Back to IDS Manager" button
        self.idsEditor_window.add_ids_to_list.connect(self.updateIdsList)# Connect signal of "Save IDS" button
        self.hide()  # Hide the main window
        self.idsEditor_window.show()
        self.idsEditor_window.raise_()
        self.idsEditor_window.activateWindow()

    def clickEdit(self):
        if Ops.checkIfElementSelected(self, self.list_ids_mgmnt):
            selected_indexes = self.list_ids_mgmnt.selectedIndexes()
            self.ids_in_edition=selected_indexes[0].data()
            my_ids=self.parseXmlToIds()
            self.idsEditor_window = IdsEditorWindow(my_ids=my_ids) #Pass parsed IDS to new IDSEditorWindow
            self.idsEditor_window.back_to_manage_ids.connect(self.showManageIds) #Connect signal of "Back to IDS Manager" button
            self.idsEditor_window.add_ids_to_list.connect(self.updateIdsList)# Connect signal of "Save IDS" button
            self.list_ids_mgmnt.clearSelection()
            self.hide()  # Hide the main window
            self.idsEditor_window.show()
            self.idsEditor_window.raise_()
            self.idsEditor_window.activateWindow()
        else:
            Ops.msgError(self, "Selection Error", "There is no item selected for editing.")

    def setFilepathIds(self, my_ids):
        # self.filter="IDS files (*.ids)"
        # self.title= "Save IDS file"
        # self.fileDialog = QFileDialog()
        # self.fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        # self.file_path, _ = self.fileDialog.getSaveFileName(None, self.title, "", self.filter)
        self.file_path = self.idsEditor_window.file_path
        if self.file_path:
            if len(self.list_ids_mgmnt.findItems(self.file_path, Qt.MatchExactly)) == 0:
                print(f"File saved in: {self.file_path}")
            else: 
                print(f"filepath already in list, file in {self.file_path} was successfully overwritten.")
            my_ids.filepath=self.file_path
            my_ids.to_xml(self.file_path)
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
    
    def deleteIds(self): 
        index = self.list_ids_mgmnt.selectedIndexes()[0]  # Assuming single selection
        if index.isValid():
            item = index.data()
            ids = self.dic_ids.pop(item)  # Remove the entry and get the associated object
            self.list_ids_mgmnt.model().removeRow(index.row())
            del ids
        self.list_ids_mgmnt.maxFileList+=1
        print(self.dic_ids)
    
    def parseXmlToIds(self):
        file_path= self.list_ids_mgmnt.currentIndex().data()
        if file_path:
            ids_object=IdsOps.parseXmlToIds(file_path)
            ids_as_dict= ids_object.asdict()
            print(ids_as_dict)
            return ids_object
        else:
            Ops.msgError(title="Error", msg='No element from IDS List was selected')

    def showManageIds(self):
        self.show()
        
class CheckWindow(QMainWindow):
    back_to_main_signal= pyqtSignal()

    def __init__(self, parent=None, items_dict:dict=None):
        super(CheckWindow, self).__init__(parent)

        # Load UI file
        Ops.load_ui("check.ui",self)

        # Define and load Widgets
        main_widget_setup = {
            "btn_check": QPushButton,
            "btn_report": QPushButton,
            "btn_back": QPushButton,
            "comboBox_ifc": QComboBox,
            "comboBox_ids": QComboBox,
            "comboBox_report": QComboBox,
            "lbl_notification": QLabel
        }
        Ops.loadWidgets(self, main_widget_setup)

        self.lbl_notification.hide() #hide lbl_notification when loading window first time

        # Connect handlers
        handlers = {
            "btn_check": self.generateReport,
            "btn_back": self.back_to_main
        }
        Ops.connectHandlers(self, handlers)

    def back_to_main(self):
        self.back_to_main_signal.emit()
        self.hide()
    
    def generateReport(self):
        #handle file paths and file names
        ids_file= self.comboBox_ids.currentText()
        ifc_file= self.comboBox_ifc.currentText()
        report_type= self.comboBox_report.currentText()

        ifc_name_with_extension=os.path.basename(ifc_file)
        ifc_name= os.path.splitext(ifc_name_with_extension)[0]
        ifc_name= ifc_name.replace(" ", "_")

        ids_name_with_extension=os.path.basename(ids_file)
        ids_name= os.path.splitext(ids_name_with_extension)[0]
        ids_name= ids_name.replace(" ", "_")


        file_extension= "."+report_type.lower()
        report_name= ifc_name+ "_VS_"+ids_name+"_Report_" + report_type + file_extension

        folder_path= self.openCustomFileDialog()
        if folder_path:
            report_path= folder_path+ f"/{report_name}" 
            #Generate report
            IfcOps.checkIfcWithIds(ifc_file, ids_file, report_type, report_path)
            self.lbl_notification.setText(f"Report was saved in: {report_path}")
            self.lbl_notification.show()
        else:
            Ops.msgError(self, "Error: Folder path", "A folder path must be provided")

    def openCustomFileDialog(self)->str:
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 
                                                       "Select Folder", 
                                                       options=options)
        if folder_path:
            return folder_path
        else:
            return None
            

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

       # Open window and Populates Comboboxes in new CheckWindow()  
        if self.ifc_window and self.ids_window:
            if self.ifc_window.list_ifc.count() != 0 and self.ids_window.list_ids_mgmnt.count() != 0:
                self.check_window = Ops.openWindow(CheckWindow, self.check_window, setup_signals)
                self.check_window.comboBox_ifc.clear()
                self.check_window.comboBox_ids.clear()
                self.check_window.comboBox_ifc.addItems(CustomListWidget.getItemsDict(self.ifc_window.list_ifc))
                self.check_window.comboBox_ids.addItems(CustomListWidget.getItemsDict(self.ids_window.list_ids_mgmnt))

                # Hide the main window show check window
                self.hide()  
                self.check_window.show()
                self.check_window.raise_()
                self.check_window.activateWindow()
            else:
                Ops.msgError(self, "Error","Before proceeding with the check, you must provide at least one IDS file and one IFC file.")
        else:
            Ops.msgError(self, "Error","Before proceeding with the check, you must provide at least one IDS file and one IFC file.")

    def show_main_window(self):
        self.show()

    def clearMdiArea(self):
        self.mdi_main.closeAllSubWindows() 

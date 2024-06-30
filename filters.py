from PyQt5.QtWidgets import QMainWindow,QLineEdit, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow, QLabel
from Ops import Ops
from ifctester import ids


class byAttribute(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet: ids.Attribute=None):
        super(byAttribute, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet
        
        # Load UI file
        Ops.load_ui("by_attribute.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_name": QLineEdit,
            "txt_value": QLineEdit,
            "lbl_optionality": QLabel,
            "combo_optionality": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "name": self.txt_name.text() ,
            "value": self.txt_value.text(),
            "optionality": self.combo_optionality.currentText()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_name.setText(self.my_facet.name) 
        self.txt_value.setText(self.my_facet.value)
        #Set value in combobox_optionality
        optionality= self.my_facet.cardinality
        Ops.setTextComboBox(self, "combo_optionality", optionality)

class byClass(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet: ids.Entity=None):
        super(byClass, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet

        # Load UI file
        Ops.load_ui("by_class.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_name": QLineEdit,
            "txt_type": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "name": self.txt_name.text() ,
            "predef_type": self.txt_type.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_name.setText(self.my_facet.name) 
        self.txt_type.setText(self.my_facet.predefinedType)
        #For class Entity there is no optionality to be provided in IDS Schema

class byClassification(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet:ids.Classification=None):
        super(byClassification, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet

        # Load UI file
        Ops.load_ui("by_classification.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_system": QLineEdit,
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit,
            "lbl_optionality": QLabel,
            "combo_optionality": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "system": self.txt_system.text() ,
            "value": self.txt_value.text(),
            "uri": self.txt_uri.text(),
            "optionality": self.combo_optionality.currentText()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_system.setText(self.my_facet.system) 
        self.txt_value.setText(self.my_facet.value) 
        self.txt_uri.setText(self.my_facet.uri)

        #Set value in combobox_optionality
        optionality= self.my_facet.cardinality
        Ops.setTextComboBox(self, "combo_optionality", optionality)

class byMaterial(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet:ids.Material=None):
        super(byMaterial, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet

        # Load UI file
        Ops.load_ui("by_material.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit,
            "lbl_optionality": QLabel,
            "combo_optionality": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "value": self.txt_value.text(),
            "uri": self.txt_uri.text(),
            "optionality": self.combo_optionality.currentText()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_value.setText(self.my_facet.value) 
        self.txt_uri.setText(self.my_facet.uri) 

        #Set value in combobox_optionality
        optionality= self.my_facet.cardinality
        Ops.setTextComboBox(self, "combo_optionality", optionality)

class byPartOf(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet:ids.PartOf= None):
        super(byPartOf, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet

        # Load UI file
        Ops.load_ui("by_part_of.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_entity": QLineEdit,
            "txt_predef_type": QLineEdit,
            "txt_relation": QLineEdit,
            "lbl_optionality": QLabel,
            "combo_optionality": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "name": self.txt_entity.text(),
            "predef_type": self.txt_predef_type.text(),
            "relation": self.txt_relation.text(),
            "optionality": self.combo_optionality.currentText()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_entity.setText(self.my_facet.name) 
        self.txt_predef_type.setText(self.my_facet.predefinedType)
        self.txt_relation.setText(self.my_facet.relation) 

        #Set value in combobox_optionality
        optionality= self.my_facet.cardinality
        Ops.setTextComboBox(self, "combo_optionality", optionality)

class byProperty(QMainWindow):
    def __init__(self, parent=None, my_ids:ids.Ids=None, my_spec:ids.Specification=None, my_facet:ids.Property=None):
        super(byProperty, self).__init__(parent)

        #Load facet if passed from SpecEditorWindow
        self.my_facet=my_facet

        # Load UI file
        Ops.load_ui("by_property.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_pset": QLineEdit,
            "txt_name": QLineEdit,
            "txt_data_type": QLineEdit,
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit,
            "lbl_optionality": QLabel,
            "combo_optionality": QComboBox
        }
        Ops.loadWidgets(self, main_widget_setup)

        #If facet was passed, load data in Window
        if self.my_facet:
            self.loadData()

    def getData(self):
        dict_data= {
            "name": self.txt_name.text(),
            "pset": self.txt_pset.text(),
            "data_type": self.txt_data_type.text(),
            "value" :self.txt_value.text(),
            "uri" : self.txt_uri.text(),
            "optionality": self.combo_optionality.currentText()
        }
        return Ops.dictEmptyValueToNone(dict_data)
    
    def loadData(self):
        self.txt_name.setText(self.my_facet.baseName) 
        self.txt_pset.setText(self.my_facet.propertySet)
        self.txt_data_type.setText(self.my_facet.dataType)
        self.txt_value.setText(self.my_facet.value) 
        self.txt_uri.setText(self.my_facet.uri) 

        #Set value in combobox_optionality
        optionality= self.my_facet.cardinality
        Ops.setTextComboBox(self, "combo_optionality", optionality)
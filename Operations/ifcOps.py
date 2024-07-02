import ifcopenshell
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCompleter

class IfcOps():
    @staticmethod
    def populateClasses(window, ifc_schema:str = "IFC4", qline_name:str = "Qline_name"):
        qline_edit = window.findChild(QLineEdit, qline_name)
        schema= ifcopenshell.ifcopenshell_wrapper.schema_by_name(ifc_schema) #TODO: Which enum types are availabe IFC 4 raise exception 
        ifc_classes= schema.declared_types()
        print(ifc_classes)
        #Creates and set completer for autoprediction in QLineEdit
        completer = QCompleter(ifc_classes)
        qline_edit.setCompleter(completer)
    
    @staticmethod
    def populateTypesCombo(window, ifc_schema:str="IFC 4", combobox_class_str:str="combobox_class", combobox_type_str:str="combobox_type"):
        combobox_class=getattr(window,combobox_class_str)
        selected_class= combobox_class.currentText()

        combobox_type=getattr(window, combobox_type_str)
        schema= ifcopenshell.ifcopenshell_wrapper.schema_by_name(ifc_schema) #load schema
        ifc_class= schema.entity(selected_class)

        if ifc_class:
            type_names = ifc_class.attributes.keys()
            combobox_type.addItems(type_names)

    @staticmethod
    def populateDataTypesCombo(window, ifc_schema:str="IFC 4", combobox_class_str:str="combobox_class"):
        schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(ifc_schema)
        declared_types = schema.declared_types()

        # Lists to store data types and enumerations
        datatypes_and_enum = []
        enumerations = []

        # Iterate through declared types to categorize them
        for type_name in declared_types:
            schema_type = schema.get(type_name)
            if schema_type.is_select_type() or schema_type.is_enum_type() or schema_type.is_simple_type():
                    datatypes_and_enum.append(type_name)

        return datatypes_and_enum


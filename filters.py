from PyQt5.QtWidgets import QMainWindow,QLineEdit, QPushButton, QMdiArea, QComboBox, QFileDialog, QMessageBox, QMdiSubWindow
from Ops import Ops


class byAttribute(QMainWindow):
    def __init__(self, parent=None):
        super(byAttribute, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_attribute.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_name": QLineEdit,
            "txt_value": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "name": self.txt_name.text() ,
            "value": self.txt_value.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)

class byClass(QMainWindow):
    def __init__(self, parent=None):
        super(byClass, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_class.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_name": QLineEdit,
            "txt_type": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "name": self.txt_name.text() ,
            "predef_type": self.txt_type.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)

class byClassification(QMainWindow):
    def __init__(self, parent=None):
        super(byClassification, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_classification.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_system": QLineEdit,
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "system": self.txt_system.text() ,
            "value": self.txt_value.text(),
            "uri": self.txt_uri.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)

class byMaterial(QMainWindow):
    def __init__(self, parent=None):
        super(byMaterial, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_material.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "value": self.txt_value.text(),
            "uri": self.txt_uri.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)

class byPartOf(QMainWindow):
    def __init__(self, parent=None):
        super(byPartOf, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_part_of.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_entity": QLineEdit,
            "txt_predef_type": QLineEdit,
            "txt_relation": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "name": self.txt_entity.text(),
            "predef_type": self.txt_predef_type.text(),
            "relation": self.txt_relation.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)

class byProperty(QMainWindow):
    def __init__(self, parent=None):
        super(byProperty, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_property.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_pset": QLineEdit,
            "txt_name": QLineEdit,
            "txt_data_type": QLineEdit,
            "txt_value": QLineEdit,
            "txt_uri": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

    def getData(self):
        dict_data= {
            "name": self.txt_name.text(),
            "pset": self.txt_pset.text(),
            "data_type": self.txt_data_type.text(),
            "value" :self.txt_value.text(),
            "uri" : self.txt_uri.text()
        }
        return Ops.dictEmptyValueToNone(dict_data)
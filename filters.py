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
    
        self.name= self.txt_name.text()
        self.value= self.txt_value.text()

    def getData(self):
        return f"name= {self.name}, value={self.value}"

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

        self.name= self.txt_name.text()
        self.type= self.txt_type.text()

    def getData(self):
        return f"name= {self.name}, type={self.type}"

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

        self.system= self.txt_system.text()
        self.value= self.txt_value.text()
        self.uri= self.txt_uri.text()

    def getData(self):
        return f"system= {self.system}, value={self.value}, uri={self.uri} "

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

        self.value= self.txt_value.text()
        self.uri= self.txt_uri.text()

    def getData(self):
        return f"value= {self.value}, uri={self.uri}"

class byPartOf(QMainWindow):
    def __init__(self, parent=None):
        super(byPartOf, self).__init__(parent)

        # Load UI file
        Ops.load_ui("by_part_of.ui",self, filter=True)

        # Define and load Widgets
        main_widget_setup = {
            "txt_entity": QLineEdit,
            "txt_relation": QLineEdit
        }
        Ops.loadWidgets(self, main_widget_setup)

        self.entity= self.txt_entity.text()
        self.relation= self.txt_relation.text()

    def getData(self):
        return f"entity= {self.entity}, relation={self.relation}"

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

        self.pset= self.txt_pset.text()
        self.name= self.txt_name.text()
        self.data_type= self.txt_data_type.text()
        self.value= self.txt_value.text()
        self.uri= self.txt_uri.text()

    def getData(self):
        return f"pset= {self.pset}, name={self.name}, data_type={self.data_type}, value={self.value}, uri={self.uri}"
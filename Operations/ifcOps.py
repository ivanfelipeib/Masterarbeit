import ifcopenshell
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCompleter
from collections import defaultdict
from Operations.Ops import Ops

class IfcOps:
    def __init__(self, ifc_file_path: str = "Folder/ifc_file.ifc"):
        self.model = ifcopenshell.open(ifc_file_path)

    def getInfoFromEntity(self, path):
        # Split the path into keys
        keys = path.split('.')
        my_ifc_entity_class= keys.pop(0)
        
        my_entity = self.model.by_type(my_ifc_entity_class)[0]
        info_dic = my_entity.get_info(recursive=True)
        value= info_dic
        
        try:
            for key in keys:
                if key.isdigit(): #Handle possible integers in path for accessing tuples
                    key= int(key)
                value = value[key]
                if value is None or value == "":
                    value="Value is either None or empty"
            return value
        except (KeyError, IndexError, TypeError):
            return None
    
    def numberElementbyEntity(self, ifc_entity:str)->str:
        elements = self.model.by_type(ifc_entity)
        names=[]
        for element in elements:
            name= element.is_a()
            names.append(name)
        return(str(len(names)))


    





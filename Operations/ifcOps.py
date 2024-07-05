import ifcopenshell
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCompleter
from collections import defaultdict
from Operations.Ops import Ops

class IfcOps:
    def __init__(self, ifc_file_path: str = "Folder/ifc_file.ifc"):
        self.model = ifcopenshell.open(ifc_file_path)

    def get_detailed_info(entity_instance):
        def recursive_info(entity):
            info = {}
            # Add the attributes of the current entity
            current_info = entity.get_info(recursive=False)
            entity_type = entity.is_a()
            for key, value in current_info.items():
                # Add context by including the class name
                contextual_key = f"{entity_type}::{key}" #keys returned include both class name and atribute name. This ensures that attributes with the same name but different contexts are uniquely identifiable.
                info[contextual_key] = value
            
            # Recurse through related objects (attributes that are also entities)
            for key, value in current_info.items():
                if isinstance(value, ifcopenshell.entity_instance):
                    related_info = recursive_info(value)
                    info.update(related_info)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, ifcopenshell.entity_instance):
                            related_info = recursive_info(item)
                            info.update(related_info)
            
            return info

        return recursive_info(entity_instance)

    def get_attribute(self, entity_instance, attribute_name):
        # Fetch detailed information including inherited attributes
        info = self.get_detailed_info(entity_instance)
        
        # Search for the attribute in the info
        for key, value in info.items():
            if key.endswith(f"::{attribute_name}"):
                return value
        raise AttributeError(f"Attribute '{attribute_name}' not found in entity '{entity_instance.is_a()}'")
    
    def get_info(self,ifc_entity)->dict:
        my_entity = self.model.by_type(ifc_entity)[0]
        info = my_entity.get_info(recursive=True)
        return info
    
    def getInfoImproved(self, path):
        # Split the path into keys
        keys = path.split('.')
        my_ifc_entity_class= keys.pop(0)
        
        my_entity = self.model.by_type(my_ifc_entity_class)[0]
        info_dic = my_entity.get_info(recursive=True)
        value= info_dic
        
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return None
    





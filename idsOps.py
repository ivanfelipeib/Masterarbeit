import ifcopenshell
from ifctester import ids, reporter
import uuid 

class IdsOps():
    @staticmethod
    def createIds(dict_info):
        my_ids = ids.Ids(**dict_info)
        return my_ids
    
    @staticmethod
    def createSpecification(dict_spec):
        my_spec= ids.Specification(
            name=dict_spec["name"],
            identifier=dict_spec["identifier"],
            description=dict_spec["description"],
            instructions=dict_spec["instructions"]
            #TODO: get list of facets for applicability and for requirments
        )   
    
    @staticmethod
    def createFacet(type):
        #TODO:Create facets by facet type based in combobox text
        # match type:
        #     case "Add filter by class":
                
        #     case "Add filter by part of":
        #         #self.by_part_of_window = Ops.openSubWindow(mdi_area, filters.byPartOf, self.by_part_of_window, setup_signals=None)
        #         self.opened_window = Ops.openSubWindow(mdi_area, filters.byPartOf, window_instance=None, setup_signals=None)
        #     case "Add filter by attribute":
        #         self.opened_window = Ops.openSubWindow(mdi_area, filters.byAttribute, window_instance=None, setup_signals=None)
        #     case "Add filter by property":
        #         self.opened_window =  Ops.openSubWindow(mdi_area, filters.byProperty, window_instance=None, setup_signals=None)
        #     case "Add filter by classification":
        #         self.opened_window = Ops.openSubWindow(mdi_area, filters.byClassification, window_instance=None, setup_signals=None)
        #     case "Add filter by material":
        #         self.opened_window = Ops.openSubWindow(mdi_area, filters.byMaterial, window_instance=None, setup_signals=None)
        #     case _:
        #         Ops.msgError(self,"Error","Text in ComboBox does not match any type of filter")
        pass
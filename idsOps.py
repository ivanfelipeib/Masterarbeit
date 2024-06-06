import ifcopenshell
from ifctester import ids, reporter

class IdsOps():
    @staticmethod
    def createIds(dict_info):
        my_ids = ids.Ids(**dict_info)
        return my_ids
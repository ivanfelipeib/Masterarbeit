import ifcopenshell
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCompleter
from collections import defaultdict
from Operations.Ops import Ops
import ifctester
from ifctester import reporter
import xlsxwriter
from datetime import datetime


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
    
    def generateExcelReport(self, filepath:str, data:dict):
        current_date = datetime.now().strftime('%d-%m-%Y')
        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        #Add Styles
        header = workbook.add_format({'bold': True, 'font_size': 15, 'underline': 2})
        titles = workbook.add_format({'bold': True, 'font_size': 13, 'underline': 1})
        bold = workbook.add_format({'bold': True})
        underlined = workbook.add_format({'underline': 1})
        #Add fix titles
        worksheet.write(0, 0, "IFC Information Report", header)
        worksheet.write(1, 0, "IFC File", bold)
        worksheet.write(2, 0, "Date of report", bold)

        worksheet.write(4, 0, "Basic Information", titles)
        worksheet.write(5, 0, "IFC Schema",bold)
        worksheet.write(6, 0, "Project Base Point", bold)
        worksheet.write(7, 0, "Coordinate System", bold)
        worksheet.write(8, 0, "Ref.Latitude", bold)
        worksheet.write(9, 0, "Ref.Longitude", bold)
        worksheet.write(10, 0, "Authoring Software", bold)
        worksheet.write(11, 0, "Objects in Model", bold)

        worksheet.write(4, 2, "Project Information", titles)
        worksheet.write(5, 2, "Description", bold)
        worksheet.write(6, 2, "Phase", bold)
        worksheet.write(7, 2, "Organization", bold)
        worksheet.write(8, 2, "Author", bold)

        worksheet.write(13, 0, "Contents of selected IFC Element", titles)
        worksheet.write(14, 0, "Entity", bold)
        worksheet.write(15, 0, "Element", bold)
        worksheet.write(17, 0, "Attributes", titles)
        worksheet.write(17, 2, "Property Sets", titles)
        # Write values
        worksheet.write(1, 1, data["ifc_info"]["File"])
        worksheet.write(2, 1, current_date)
        worksheet.write(5, 1, data["basic_info"]["ifc_schema"])
        worksheet.write(6, 1, data["basic_info"]["base_point"])
        worksheet.write(7, 1, data["basic_info"]["coord_system"])
        worksheet.write(8, 1, data["basic_info"]["latitude"])
        worksheet.write(9, 1, data["basic_info"]["longitude"])
        worksheet.write(10, 1, data["basic_info"]["software"])
        worksheet.write(11, 1, data["basic_info"]["objects_num"])
        worksheet.write(5, 3,data["project_info"]["description"])
        worksheet.write(6, 3,data["project_info"]["phase"])
        worksheet.write(7, 3,data["project_info"]["organization"])
        worksheet.write(8, 3,data["project_info"]["author"])
        worksheet.write(14, 1, data["ifc_info"]["Entity"])
        worksheet.write(15, 1, data["ifc_info"]["Element"])
        
        # Write Attribute
        if "Attributes" in data["ifc_info"]:
            row_start=18
            col_start =0
            attributes=data["ifc_info"]["Attributes"]
            for idx, attr in enumerate(attributes):
                worksheet.write(row_start + idx, col_start, attr)
        # Write PSets
        if "PSets" in data["ifc_info"]:
            psets = data["ifc_info"]["PSets"]
            row_start = 18
            col_start=2
            for key in psets.keys():
                worksheet.write(row_start, col_start, key, bold)
                properties= psets[key]
                for idx, attr in enumerate(properties):
                    worksheet.write(row_start+ 1 + idx, col_start, attr)
                col_start+=1
            last_column=col_start
        else:
            last_column=3 #assuming there is no Property sets in model
        #Adjust column width
        worksheet.set_column(0, last_column,30)
        # Close the workbook
        workbook.close()
        Ops.msgError(self, "Report created", f"Excel file has been created successfully in {filepath}.")

    def checkIfcWithIds(ifc_file_path:str, ids_file_path:str, report_type:str, report_file_path:str):
        my_ifc = ifcopenshell.open(ifc_file_path)
        my_ids = ifctester.open(ids_file_path)  
        my_ids.validate(my_ifc) #validate IFC against IDS
        reporter_obj = None

        match report_type:
            case "HTML":
                reporter_obj = reporter.Html(my_ids)
            case "ODS":
                reporter_obj= reporter.Ods(my_ids)
            case "JSON":
                reporter_obj= reporter.Json(my_ids)
            case "BCF":
                reporter_obj= reporter.Bcf(my_ids)

        if reporter_obj:
            reporter_obj.report()
            reporter_obj.to_file(report_file_path)
        else:
            print("reporter is None")



    





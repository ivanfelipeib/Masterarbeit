import ifcopenshell
from ifctester import ids, reporter
import uuid
import sys
#import os
from pathlib import Path
#import ctypes
#import clr
import subprocess

class IdsOps():
    @staticmethod
    def createIds():
        my_ids= ids.Ids()
        return my_ids

    @staticmethod
    def createSpec():
        my_spec= ids.Specification()
        return my_spec

    @staticmethod
    def addIdsInfo(my_ids : ids.Ids, dict_info: dict) ->ids.Ids:
        my_ids.info["title"] = dict_info["title"]
        my_ids.info["copyright"] = dict_info["copyright"]
        my_ids.info["version"] = dict_info["version"]
        my_ids.info["description"] = dict_info["description"]
        my_ids.info["author"] = dict_info["author"]
        my_ids.info["date"] = dict_info["date"]
        my_ids.info["purpose"] = dict_info["purpose"]
        my_ids.info["milestone"] = dict_info["milestone"]
        return my_ids
    
    @staticmethod
    def addSpecInfo(dict_spec_info):
        my_spec= ids.Specification(
            name=dict_spec_info["name"],
            ifcVersion= dict_spec_info["ifcVersion"],
            identifier= dict_spec_info["identifier"],
            description=dict_spec_info["description"],
            instructions=dict_spec_info["instructions"]
        )
        return my_spec   
    
    @staticmethod
    def createFacet(spec_type, dict_data): #TODO: Include combobox applicability for cardinality
        #TODO:Create facets by facet type based in combobox text
        if  spec_type == "Add filter by class" or spec_type == "Add requirement by class":
            facet= ids.Entity(name = dict_data["name"], predefinedType = dict_data["predef_type"])

        elif spec_type == "Add filter by attribute" or spec_type == "Add requirement by attribute":
            #TODO:Define Cardinality from combobox
            facet= ids.Attribute(name = dict_data["name"], value = dict_data["value"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by classification" or spec_type == "Add requirement by classification":
            #TODO:Define Cardinality from combobox
            facet= ids.Classification(system = dict_data["system"], value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by property" or spec_type == "Add requirement by property":
            #TODO:Define Cardinality from combobox
            facet= ids.Property(propertySet= dict_data["pset"], baseName = dict_data["name"], dataType= dict_data["data_type"], value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by material" or spec_type == "Add requirement by material":
            #TODO:Define Cardinality from combobox
            facet= ids.Material(value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by part of" or spec_type == "Add requirement by part of":
            #TODO:Define Cardinality from combobox
            facet= ids.PartOf(name = dict_data["name"], predefinedType=  dict_data["predef_type"], relation= dict_data["relation"], cardinality = dict_data["optionality"], instructions= None) 
        
        else:
            print("Chosen filter/requirement, does not correspont to a valid facet type")

        return facet

    @staticmethod
    def addFacetApplicability(my_spec, facet):
        my_spec.applicability.append(facet)

    @staticmethod
    def addFacetRequirement(my_spec, facet):
        my_spec.requirements.append(facet)
    
    @staticmethod
    def loadCSharpFile(self):
         # Define the directory and DLL path
        DIRECTORY_IDS_AUDIT_DLL = "IdsAudit/bin/Debug/net8.0/IdsAudit.dll"
        root_dir = Path(__file__).resolve().parent
        filepath = root_dir / DIRECTORY_IDS_AUDIT_DLL
        #filepath = r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\IdsAudit\bin\Debug\net8.0\IdsAudit.dll"
        # Check if the DLL exists at the specified path
        if not filepath.is_file():
            raise FileNotFoundError(f"Cannot find DLL at {filepath}")
        else:
            # Add the directory containing the DLL to the sys.path
            #sys.path.append(str(filepath.parent))
            sys.path.append(r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\IdsAudit\bin\Debug\net8.0")
            import clr
            # Load the C# DLL
            #clr.AddReference(str(filepath))
            clr.AddReference("IdsAudit")

            # Import the namespace and class
            from IdsAuditLib import IdsAudit
            self.IdsAudit = IdsAudit
            print(f"DLL in: {filepath}  was uploaded sucessfully")

    @staticmethod
    def run_audit(self, filepathStr: str, idsVersionStr: str) -> str :
        filePath = filepathStr
        idsVersion = idsVersionStr

        if not filePath or not idsVersion:
            self.logOutput.append("File path and IDS Version must be provided.")
            return

        try:
            # Run the audit
            result = self.IdsAudit.RunAudit(filePath, idsVersion)
            self.logOutput.append(result)
        except Exception as e:
            self.logOutput.append(f"Error: {str(e)}")
    
    def auditIds():
        try:
            # Run the C# console application
            result = subprocess.run(
                [r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\ConsoleIdsAudit\bin\Release\net8.0\ConsoleIdsAudit.exe"],
            )
        except Exception as e:
            print(e)
    



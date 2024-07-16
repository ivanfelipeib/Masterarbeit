from ifctester import ids, reporter
import uuid
from pathlib import Path
from Operations.Ops import Ops
import subprocess
import constants
import xmlschema
import xml.etree.ElementTree as ET

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
    def createFacet(spec_type: str, dict_data: dict, is_filter: bool= False, cardinality_filter: str = "required")-> ids.Facet:

        if  spec_type == "Add filter by class" or spec_type == "Add requirement by class":
            facet= ids.Entity(name = dict_data["name"], predefinedType = dict_data["predef_type"])

        elif spec_type == "Add filter by attribute" or spec_type == "Add requirement by attribute":
            facet= ids.Attribute(name = dict_data["name"], value = dict_data["value"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by classification" or spec_type == "Add requirement by classification":
            facet= ids.Classification(system = dict_data["system"], value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by property" or spec_type == "Add requirement by property":
            facet= ids.Property(propertySet= dict_data["pset"], baseName = dict_data["name"], dataType= dict_data["data_type"], value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by material" or spec_type == "Add requirement by material":
            facet= ids.Material(value = dict_data["value"], uri = dict_data["uri"], cardinality = dict_data["optionality"], instructions= None) 

        elif spec_type == "Add filter by part of" or spec_type == "Add requirement by part of":
            facet= ids.PartOf(name = dict_data["name"], predefinedType=  dict_data["predef_type"], relation= dict_data["relation"], cardinality = dict_data["optionality"], instructions= None) 
        
        else:
            print("Chosen filter/requirement, does not correspont to a valid facet type")

        if is_filter:
            facet.cardinality = cardinality_filter #If facet is a filter, cardinality is defined by comboBox in applicability section
        else: pass

        return facet

    @staticmethod
    def addFacetApplicability(my_spec, facet):
        my_spec.applicability.append(facet)

    @staticmethod
    def addFacetRequirement(my_spec, facet):
        my_spec.requirements.append(facet)
    
    @staticmethod
    def auditIds():
        try:
            # Run the C# console application 'TODO: Handle filepath with constants file
            result = subprocess.run(
                [constants.AUDIT_SCRIPT_DIR],
            )
        except Exception as e:
            print(e)
    
    @staticmethod
    def getIdsVersionXML(file_path: str) -> str:
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            xml_root = tree.getroot()
            
            # Get the schemaLocation attribute
            schema_location = xml_root.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            
            if schema_location:
                # The schemaLocation attribute contains a space-separated list of URIs
                parts = schema_location.split()
                if len(parts) > 1:
                    # Extract the version from the second URI in the list
                    version_uri = parts[1]
                    version = version_uri.rsplit('/', 2)[-2]
                    return version
            return None
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None
    
    @staticmethod
    def parseXmlToDict(xml_path:str = None)->dict:
        try:
            # Extract the version
            version = IdsOps.getIdsVersionXML(xml_path)
            
            if not version:
                raise ValueError("Could not determine the IDS version or the version is unsupported.")
            
            # Determine the appropriate schema path based on the version
            schema_path = ''
            if version == "0.9.7":
                schema_path = constants.IDS_097_SCHEMA
            elif version == "1.0.0":
                schema_path = constants.IDS_SCHEMA
            else:
                raise ValueError("Only IDS Versions 1.0.0 and 0.9.7 are supported")
            
            # Load the XML schema
            schema = xmlschema.XMLSchema(schema_path)
            # Convert XML to dictionary
            data_dict = schema.to_dict(xml_path)
            # Convert IDS Versions to String since IDS Schema defines IFC Version as list an returns in previous step IDs version 1-element lists. 
            specifications = data_dict.get('specifications', {})
            specification_list = specifications.get('specification', [])
            for spec in specification_list:
                if '@ifcVersion' in spec and isinstance(spec['@ifcVersion'], list) and len(spec['@ifcVersion']) == 1:
                    spec['@ifcVersion'] = spec['@ifcVersion'][0]
            return data_dict
    
        except ValueError as e:
            print(f"ValueError: {e}")
        except xmlschema.XMLSchemaException as e:
            print(f"XMLSchemaException: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return {}

    @staticmethod
    def parseDictToIds(ids_as_dict: dict)->ids.Ids:
        my_ids= ids.Ids()
        my_ids.parse(ids_as_dict)
        return my_ids
    
    @staticmethod
    def entityToString(entity_instance:ids.Entity, clause_type:str="requirement")->str:
        entity = entity_instance
        clause = clause_type
        if clause_type == "requirement":
            templates = entity.requirement_templates
        elif clause_type == "applicability":
            templates = entity.applicability_templates
        elif clause_type == "prohibited":
            templates = entity.prohibited_templates
        else:
            return None  # Invalid clause_type

        if entity.predefinedType is None:
            entity_str = templates[1].format(name=getattr(entity, 'name', ''))
        else:
            entity_str = templates[0].format(
                name=getattr(entity, 'name', ''),
                predefinedType=getattr(entity, 'predefinedType', '')
            )
        return entity_str
    
    @staticmethod
    def idsQualityReport(ids_enity:ids, base_report_filepath:str):
        my_ids=ids_enity

        with open(base_report_filepath, 'r') as file:
            existing_content = file.read()

        with open(base_report_filepath,'w') as file:
            header= "IDS QUALITY CHECK REPORT"+"\n"
            subheader= "Date of report: "+ Ops.getDatetime() +"\n"+"\n"
            ids_name= "IDS Name: "+ str(my_ids.info["title"]) +"\n"
            ids_version = "IDS Version: "+ str(my_ids.info["version"])+"\n"
            ids_date= "Created on: "+ str(my_ids.info["date"])+"\n"
            ids_description= "IDS Description: "+ str(my_ids.info["description"])+"\n"+"\n"
            header_quality_check= "Quality check: "+"\n"

            new_text= header + subheader+ ids_name + ids_version + ids_date + ids_description + header_quality_check

            footnote=("\n The warnings and information are for informational purposes and do not constitute a problem in themselves."
                      "On the contrary, the errors found in the quality report must be corrected before the IDS file can be used."
                    "Using a corrupted IDS file will not allow proper verification of the information content of an IFC model. \n"
                    "Please consider this before saving the IDS File you are editing")

            file.write(new_text+existing_content+footnote)

   
        
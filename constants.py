import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTNET_VERSION= "net8.0" #If another version is installed, change constant

#Temp files
TEMP_DIR= os.path.join(BASE_DIR, 'temp_files')
TEMP_IDS_DIR= os.path.join(BASE_DIR, 'temp_files', 'TempIds.ids')
TEMP_LOG_DIR= os.path.join(BASE_DIR, 'temp_files', 'log.txt')

#IdsAuditTool Script
AUDIT_SCRIPT_DIR= os.path.join(BASE_DIR, 'ConsoleIdsAudit', 'bin','Release',DOTNET_VERSION,'ConsoleIdsAudit.exe') #TODO: path for debug, probkems with release

#GUI folders
GUI_DIR= os.path.join(BASE_DIR, 'GUI_Windows')
GUI_FACETS_DIR= os.path.join(BASE_DIR, 'GUI_Windows', 'Filters-Requirements')

#IDS Schema XSD
IDS_SCHEMA= os.path.join(BASE_DIR, 'Others','ids.xsd') #Version IDS 1.0
IDS_097_SCHEMA= os.path.join(BASE_DIR, 'Others','ids_097.xsd') #Version IDS 0.9.7

#IFC SCHEMA PATHS
# # #Project base point
IFC_BASE_POINT= "IfcProject.RepresentationContexts.0.WorldCoordinateSystem.Location.Coordinates" #0 in path to acces the tuple in RepresentationContext
# # #Coordinate Reference System
IFC_CRS_NAME = "IfcCoordinateReferenceSystem.Name"
IFC_CRS_DESCRIPTION = "IfcCoordinateReferenceSystem.Description"
# # #Authoring Software
IFC_AUTHOR_SOFTWARE = "IfcApplication.ApplicationFullName"
# # #Project Description
IFC_PROJ_DESCRIPTION = "IfcProject.Description"
# # #Project phase
IFC_PROJ_PHASE = "IfcProject.Phase"
# # #Project Client
IFC_PROJ_OWNER_ORG = "IfcProject.OwnerHistory.OwningUser.TheOrganization.Name"
# # #Project Author
IFC_PROJ_OWNER_AUTHOR_LAST_NAME ="IfcProject.OwnerHistory.OwningUser.ThePerson.FamilyName"
IFC_PROJ_OWNER_AUTHOR_FIRST_NAME = "IfcProject.OwnerHistory.OwningUser.ThePerson.GivenName"

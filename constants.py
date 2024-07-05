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
# #IFC4
# # #Project base point
IFC4_BASE_POINT= "IfcProject.RepresentationContexts.WorldCoordinateSystem.Location.Coordinates"
# # #Coordinate Reference System
IFC4_CRS_NAME = "IfcCoordinateReferenceSystem.Name"
IFC4_CRS_DESCRIPTION = "IfcCoordinateReferenceSystem.Description"
# # #Authoring Software
IFC4_AUTHOR_SOFTWARE = "IfcApplication.ApplicationFullName"
# # #Project Description
IFC4_PROJ_DESCRIPTION = "IfcProject.Description"
# # #Project phase
IFC4_PROJ_PHASE = "IfcProject.Phase"
# # #Project Client
IFC4_PROJ_OWNER_ORG = "IfcProject.OwnerHistory.OwningUser.TheOrganization.Name"
# # #Project Author
IFC4_PROJ_OWNER_AUTHOR_LAST_NAME ="IfcProject.OwnerHistory.OwningUser.ThePerson.FamilyName"
IFC4_PROJ_OWNER_AUTHOR_FIRST_NAME = "IfcProject.OwnerHistory.OwningUser.ThePerson.GivenName"

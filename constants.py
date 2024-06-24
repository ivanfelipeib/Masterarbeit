import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTNET_VERSION= "net8.0" #If another version is installed, change constant

#Temp files
TEMP_DIR= os.path.join(BASE_DIR, 'temp_files')
TEMP_IDS_DIR= os.path.join(BASE_DIR, 'temp_files', 'TempIds.ids')
TEMP_LOG_DIR= os.path.join(BASE_DIR, 'temp_files', 'log.txt')

#IdsAuditTool Script
AUDIT_SCRIPT_DIR= os.path.join(BASE_DIR, 'ConsoleIdsAudit', 'bin','Release',DOTNET_VERSION,'ConsoleIdsAudit.exe')

#GUI folders
GUI_DIR= os.path.join(BASE_DIR, 'GUI_Windows')
GUI_FACETS_DIR= os.path.join(BASE_DIR, 'GUI_Windows', 'Filters-Requirements')

#IDS Schema
IDS_SCHEMA= os.path.join(BASE_DIR, 'Others','ids.xsd') #Version IDS 1.0
IDS_097_SCHEMA= os.path.join(BASE_DIR, 'Others','ids_097.xsd') #Version IDS 0.9.7



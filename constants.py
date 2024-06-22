import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTNET_VERSION= "net8.0"

#Temp files
TEMP_IDS_DIR= os.path.join(BASE_DIR, 'temp_files', 'TempIds.ids')
TEMP_LOG_DIR= os.path.join(BASE_DIR, 'temp_files', 'log.txt')

#IdsAuditTool Script
AUDIT_SCRIPT_DIR= os.path.join(BASE_DIR, 'ConsoleIdsAudit', 'bin','Release',DOTNET_VERSION,'ConsoleIdsAudit.exe')

# Other Paths and constants


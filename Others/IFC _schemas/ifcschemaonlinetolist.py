# import ifcopenshell
# import ifcopenshell.express
# import ifcopenshell.util

# # Open an empty IFC file (schema will be detected automatically)
# ifc = ifcopenshell.open()

# # Access schema information
# for schema in ifc.schema.declared_schemas:
#   for entity_name in schema.entities:
#     print(entity_name)

import requests
from bs4 import BeautifulSoup

# Target URL (replace with desired IFC4 entity list URL)
url_IFC2X3 = "https://standards.buildingsmart.org/IFC/RELEASE/IFC2x3/TC1/HTML/alphabeticalorder_entities.htm"

# Make a request and check for success
response = requests.get(url_IFC2X3)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, "html.parser")
  # Find elements with text containing "ifc" (adjust if needed)
  entities_IFC2x3 = soup.find_all("a", string=lambda text: text and text.lower().startswith("ifc"))
  entity_list_IFC2X3 = [entity.text.strip() for entity in entities_IFC2x3]
  #print(entity_list)
else:
  print("Error accessing website")


# Target URL (replace with desired IFC4 entity list URL)
url_IFC4 = "https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2/HTML/annex/annex-b/alphabeticalorder_entities.htm"

# Make a request and check for success
response = requests.get(url_IFC4)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, "html.parser")
  # Find elements with text containing "ifc" (adjust if needed)
  entities_IFC4 = soup.find_all("a", string=lambda text: text and text.lower().startswith("ifc"))
  entity_list_IFC4 = [entity.text.strip() for entity in entities_IFC4]
  #print(entity_list_IFC4)
else:
  print("Error accessing website")

print(len(entity_list_IFC2X3))
print(len(entity_list_IFC4))
import sys
import ifcopenshell
from collections import defaultdict

FILEPATH= r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\3- Info Base\2- bS\1- IFC sample files\IFC 4\example project location.ifc"

# Our Main function
model = ifcopenshell.open(FILEPATH)
door = model.by_type("IfcProject")[0]
print((str(door.get_info(recursive=True)["OwnerHistory"]["OwningUser"]["TheOrganization"]["Name"])))
# elementos=door.get_info(recursive=True)
# for attribute, value in elementos.items():
#     print(f"{attribute}: {value}")

# for pset in door:
#      print(pset)
# #Get all attributes and their values
# door_info = door.get_info(recursive=True)

# Print the attributes and their values
#for attribute, value in door_info.items():
    #print(f"{attribute}: {value}")
#print(door_info)
#print(door_info.keys())



###List of entities and repetitions###
# entity_counts = defaultdict(int)

# # Iterate over all entities in the model
# for entity in model:
#     entity_type = entity.is_a()
#     entity_counts[entity_type] += 1

# # Convert the defaultdict to a regular dictionary for easier handling
# entity_counts = dict(entity_counts)

# # Print the entity types and their respective counts
# for entity_type, count in entity_counts.items():
#     print(f"{entity_type}: {count}")








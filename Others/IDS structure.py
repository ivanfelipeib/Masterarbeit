example_dict = {
    "info": {
        "title": "Example IDS",
        "copyright": "Example Copyright",
        "version": "1.0",
        "description": "This is an example IDS.",
        "author": "example@example.com",
        "date": "2024-06-06",
        "purpose": "Example Purpose",
        "milestone": "Initial"
    },
    "specifications": {
        "specification": [
            {
                "@name": "Example Specification",
                "@ifcVersion": ["IFC2X3", "IFC4"],
                "@identifier": "Spec001",
                "@description": "This is an example specification.",
                "@instructions": "Follow these instructions.",
                "applicability": {
                    "@minOccurs": 1,
                    "@maxOccurs": "unbounded",
                    "entity": [
                        {
                            "@name": "IfcWall"
                        }
                    ],
                    "classification": [
                        {
                            "@name": "ClassificationName",
                            "@source": "ClassificationSource"
                        }
                    ]
                },
                "requirements": {
                    "property": [
                        {
                            "@name": "Pset_WallCommon",
                            "@property": "FireRating",
                            "@value": "FR-2h"
                        }
                    ],
                    "material": [
                        {
                            "@name": "Concrete"
                        }
                    ]
                }
            }
        ]
    }
}

entity_facet_dict = {
    "type": "Entity",
    "value": "IfcWall",
    "uri": "http://example.com/entities/ifcwall",
    "cardinality": "required",
    "instructions": "All elements must be of type IfcWall.",
    "predefined_type": "STANDARD",
    "restriction": {
        "base": "string",
        "options": {"enumeration": ["STANDARD", "ELEMENTEDWALL"]}
    }
}

attribute_facet_dict = {
    "type": "Attribute",
    "value": "Height",
    "uri": "http://example.com/attributes/height",
    "cardinality": "required",
    "instructions": "Height attribute is required for all walls.",
    "restriction": {
        "base": "double",
        "options": {
            "minInclusive": "2.5",
            "maxInclusive": "4.0"
        }
    }
}

classification_facet_dict = {
    "type": "Classification",
    "value": "OmniClass",
    "uri": "http://example.com/classifications/omniclass",
    "cardinality": "required",
    "instructions": "All elements must be classified under OmniClass.",
    "restriction": {
        "base": "string",
        "options": {
            "pattern": "[0-9]{2}-[0-9]{2}-[0-9]{2}"
        }
    }
}

part_of_facet_dict = {
    "type": "PartOf",
    "value": "IfcBuildingStorey",
    "uri": "http://example.com/relationships/partofbuildingstorey",
    "cardinality": "required",
    "instructions": "Elements must be part of a building storey.",
    "restriction": {
        "base": "string",
        "options": {
            "enumeration": ["IfcBuildingStorey", "IfcSite"]
        }
    }
}

property_facet_dict = {
    "type": "Property",
    "value": "LoadBearing",
    "uri": "http://example.com/properties/loadbearing",
    "cardinality": "required",
    "instructions": "Ensure all load-bearing elements have this property.",
    "restriction": {
        "base": "boolean",
        "options": {
            "enumeration": ["true", "false"]
        }
    }
}

material_facet_dict = {
    "type": "Material",
    "value": "Concrete",
    "uri": "http://example.com/materials/concrete",
    "cardinality": "required",
    "instructions": "Use concrete for all structural elements."
}
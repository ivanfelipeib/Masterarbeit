import xml.etree.ElementTree as ET

def parse_xsd(xsd_file):
    tree = ET.parse(xsd_file)
    root = tree.getroot()
    return parse_element(root)

def parse_element(element):
    result = {}

    # Process attributes
    for attr_name, attr_value in element.attrib.items():
        result['@' + attr_name] = attr_value

    # Process child elements
    for child in element:
        tag = child.tag.split('}')[-1]  # Get the local tag name (stripping namespace)
        if tag in result:
            # Convert to list if there are multiple elements with same tag
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(parse_element(child))
        else:
            result[tag] = parse_element(child)

    return result


# Example usage
result_dict = parse_xsd(r"C:\Users\iibanez\OneDrive - Schüßler-Plan GmbH\Docs trabajo\4- Masterarbeit\Repo\Others\IFC4.xsd")

# Save dictionary to a text file
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(str(result_dict))
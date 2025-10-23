import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict

xml_path = "X:\XML Parsing\py\bank_clients.xml"
def extract_tables_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    tables = defaultdict(list)

    def parse_element(element, parent_tag=None, parent_id=None):
        # Detect repeated children = possible table
        tag_counts = defaultdict(int)
        for child in element:
            tag_counts[child.tag] += 1
        
        for child in element:
            # Identify "table-like" tags (appearing more than once)
            if tag_counts[child.tag] > 1:
                # Each repeated tag becomes a row in its table
                row = {**child.attrib}
                for sub in child:
                    row[sub.tag] = sub.text
                if parent_id:
                    row[parent_tag + "_id"] = parent_id
                tables[child.tag].append(row)
                parse_element(child, parent_tag=child.tag)
            else:
                # Recurse deeper
                parse_element(child, parent_tag=element.tag, parent_id=element.attrib.get("id"))

    parse_element(root)
    return tables


# === usage ===
xml_file = "bank_clients.xml"
tables = extract_tables_from_xml(xml_file)

for name, rows in tables.items():
    df = pd.DataFrame(rows)
    print(f"\n📘 Table: {name} ({len(df)} rows)")
    print(df.head(5))  # preview first 5 rows

    # Optionally export each table
    df.to_csv(f"{name}.csv", index=False)

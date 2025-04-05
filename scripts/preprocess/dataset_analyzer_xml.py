import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

data_file = Path(r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\siri_et_response.xml")

print(f"\n📄 Analyzing XML file: {data_file.name}\n")

try:
    tree = ET.parse(data_file)
    root = tree.getroot()

    print(f"✅ Root tag: {root.tag}\n")

    # Collect all tags (with namespace stripped)
    all_tags = []
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        all_tags.append(tag)

    tag_counts = Counter(all_tags)
    print("📌 Top-level tags and frequencies:")
    for tag, count in tag_counts.most_common(20):
        print(f"  {tag}: {count}")

    print("\n🔍 Sample elements with attributes:")
    for elem in list(root.iter())[1:6]:
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        print(f"\nTag: {tag}")
        print(f"Text: {elem.text.strip() if elem.text else ''}")
        print(f"Attributes: {elem.attrib}")

except FileNotFoundError:
    print("❌ File not found.")
except ET.ParseError as e:
    print(f"❌ XML Parse Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

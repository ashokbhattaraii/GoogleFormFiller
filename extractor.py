import re
import json

with open("form_raw.html", "r") as f:
    html = f.read()

match = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);\s*</script>', html, re.DOTALL)
if not match:
    print("Could not find FB_PUBLIC_LOAD_DATA_")
    exit(1)

data = json.loads(match.group(1))

# data[1][1] is a list of form items
items = data[1][1]

mapping = {}
page_fields = {}
current_page = 0
page_fields[current_page] = []

for item in items:
    item_type = item[3]
    
    # 8 is page break
    if item_type == 8:
        current_page += 1
        page_fields[current_page] = []
        continue
    
    title = item[1]
    if not title:
        continue
        
    # generate a readable key
    clean_title = re.sub(r'\W+', '_', title)
    # keep it reasonable length
    key = clean_title[:30].strip('_')
    
    if len(item) > 4 and item[4]:
        for sub_item in item[4]:
            entry_id = sub_item[0]
            mapping[key] = f"entry.{entry_id}"
            page_fields[current_page].append(key)

print("MAPPING:")
print(json.dumps(mapping, indent=2))
print("\nPAGE FIELDS:")
print(json.dumps(page_fields, indent=2))

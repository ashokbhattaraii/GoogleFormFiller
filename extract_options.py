import re
import json

with open("form_raw.html", "r") as f:
    html = f.read()

match = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);\s*</script>', html, re.DOTALL)
if not match:
    print("Could not find FB_PUBLIC_LOAD_DATA_")
    exit(1)

data = json.loads(match.group(1))
items = data[1][1]

options_dict = {}

for item in items:
    item_type = item[3]
    if item_type == 8:
        continue
    
    title = item[1]
    if not title:
        continue
        
    clean_title = re.sub(r'\W+', '_', title)
    key = clean_title[:30].strip('_')
    
    if len(item) > 4 and item[4]:
        for sub_item in item[4]:
            # sub_item[1] contains the options for radio/checkbox/dropdown
            if len(sub_item) > 1 and sub_item[1]:
                opts = [opt[0] for opt in sub_item[1] if opt[0]]
                if opts:
                    options_dict[key] = opts

print(json.dumps(options_dict, indent=2))

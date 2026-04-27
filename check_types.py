import re
import json

with open("form_raw.html", "r") as f:
    html = f.read()

match = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);\s*</script>', html, re.DOTALL)
data = json.loads(match.group(1))
items = data[1][1]

for item in items:
    item_type = item[3]
    title = item[1]
    if title:
        print(f"Title: {title[:50]} | Type: {item_type}")

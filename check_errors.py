import re

with open('error_p0.html', 'r') as f:
    content = f.read()

# Find the location of the error message
idx = content.find("प्रश्न परिवर्तन भएको छ")
if idx != -1:
    # Print the 2000 characters before and after to see context
    print(content[max(0, idx - 2000) : min(len(content), idx + 2000)])
else:
    print("Not found")

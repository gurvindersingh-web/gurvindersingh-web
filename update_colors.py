import re

with open('README.md', 'r') as f:
    content = f.read()

replacements = {
    '080808': '0f172a', # very dark background
    '2a2925': '1e293b', # dark border/secondary
    '666459': '334155', # tertiary
    '736f62': '475569', # quaternary
    'a39f8d': '3b82f6', # primary accent (strong blue)
    'd4cebd': '60a5fa', # secondary accent (light blue)
    'eae6df': 'f8fafc', # text (almost white)
    '1e1e1e': '0f172a'  # badge label color
}

# Also handle url encoded hashes like %23d4cebd -> %2360a5fa
url_replacements = {
    '%23d4cebd': '%2360a5fa',
    '%23a39f8d': '%233b82f6',
    '%23666459': '%23334155'
}

for old, new in replacements.items():
    # replace lowercase
    content = re.sub(old, new, content)
    # replace uppercase
    content = re.sub(old.upper(), new.upper(), content)

for old, new in url_replacements.items():
    content = re.sub(old, new, content)
    content = re.sub(old.upper(), new.upper(), content)

with open('README.md', 'w') as f:
    f.write(content)

print("Colors updated successfully.")

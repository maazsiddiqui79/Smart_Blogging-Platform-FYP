import os

path = r'c:\Users\siddi\Desktop\Vibe-Code-Test\FYP\blog\views.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 250 <= i <= 258:
        stripped = line.strip()
        if not stripped:
            new_lines.append('\n')
        elif stripped.startswith('#'):
            new_lines.append('    ' + stripped + '\n')
        elif stripped.startswith('category ='):
            new_lines.append('    ' + stripped + '\n')
        elif stripped.startswith('if '):
            new_lines.append('    ' + stripped + '\n')
        elif stripped.startswith('query ='):
            new_lines.append('    ' + stripped + '\n')
        elif stripped.startswith('blog_list ='):
            new_lines.append('        ' + stripped + '\n')
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed indentation.")

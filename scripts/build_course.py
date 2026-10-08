"""Bundle the editable course as a self-contained offline HTML file."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
course = root / 'course'
html = (course / 'index.html').read_text()
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + (course / 'style.css').read_text() + '</style>')
for filename in ['lessons.js', 'integration.js', 'app.js']:
    source = (course / filename).read_text()
    if '</script' in source.lower():
        raise ValueError('Script source requires HTML escaping')
    html = html.replace(f'<script src="{filename}"></script>', '<script>' + source + '</script>')
(root / '学习手册.html').write_text(html)
print('Built 学习手册.html')

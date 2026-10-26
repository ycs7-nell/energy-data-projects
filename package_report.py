from pathlib import Path
root=Path(__file__).parent
s=(root/'template.html').read_text().replace('__DATA__',(root/'results.json').read_text()).replace('__MANIFEST__',(root/'manifest.json').read_text())
(root/'explorer.html').write_text(s)

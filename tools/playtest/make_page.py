"""Turn the playtest build into the page published as the private playtest artifact.

    npm run playtest        # builds playtest-dist/ with relative paths, then runs this

The artifact host wraps the page in its own <html>/<head>/<body>, so this keeps
the title, styles, game markup and script tag from playtest-dist/index.html and
writes playtest-dist/play.html. Publish play.html with the files under
playtest-dist/ (assets/, sprites/, portraits/, env/, LICENSES.txt) to update
https://claude.ai/artifact/F4Zff8ygkY8qzZFcvbQTuj (private to Lucas).
"""
import re
from pathlib import Path

DIST = Path(__file__).resolve().parents[2] / 'playtest-dist'
src = (DIST / 'index.html').read_text()
head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
script = re.search(r'<script type="module"[^>]*></script>', head).group(0).replace(' crossorigin', '')
css = re.search(r'<link rel="stylesheet"[^>]*>', head).group(0).replace(' crossorigin', '')
page = f'''<title>The Missing Rings</title>
<meta name="description" content="A little wedding adventure for Logan and Angie.">
{css}
<style>:root{{color-scheme:dark;background:#13271f}} body{{background:radial-gradient(ellipse at 50% 20%,#344e3b,#13271f 75%);color:#f6eedb}}</style>
{body.strip()}
{script}
'''
(DIST / 'play.html').write_text(page)
print('Wrote', DIST / 'play.html', 'using', re.search(r'assets/[^"]+\.js', script).group(0))

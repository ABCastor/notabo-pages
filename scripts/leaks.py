from pathlib import Path
import re
import subprocess
import sys

paths = sys.argv[1:] or subprocess.check_output(['git', 'ls-files', '-z'], text=True).split('\0')
allowed = {'ciao@abcastor.com'}
errors = []
for name in filter(None, paths):
    path = Path(name)
    if not path.is_file():
        continue
    text = path.read_text(errors='ignore')
    if re.search(r'/(?:Users|home)/[A-Za-z0-9_.-]+', text):
        errors.append(f'{name}: absolute home path')
    for email in re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text):
        if email not in allowed and not email.endswith('@example.com'):
            errors.append(f'{name}: undocumented email')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('Leak check passed')

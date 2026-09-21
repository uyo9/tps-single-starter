import glob
import json
import os
import re
import subprocess

from PIL import Image

os.chdir(os.environ.get('GITHUB_WORKSPACE'))

os.chdir('pro/statement')

idx = 0
content = open('index.md', 'r', encoding='utf8').read()

pngs = glob.glob('*.png')
jpgs = glob.glob('*.jpg')

for source in pngs:
    target = os.path.splitext(source)[0] + '.jpg'
    while os.path.exists(target):
        idx += 1
        target = 'img{}.jpg'.format(idx if idx > 1 else '')
    new_content = re.sub(r'{\s*' + re.escape(source) + r'\s*}', '{' + target + '}', content)
    if content != new_content:
        content = new_content
        im = Image.open(source)
        print(source, target, im.size)
        cmd = ['convert']
        if im.size[0] > 640:
            cmd.extend(['-resize', '640x'])
        cmd.extend([source, target])

        print(' '.join(cmd))
        subprocess.run(cmd)
        subprocess.run(['rm', source])
        subprocess.run(['git', 'add', source])
        subprocess.run(['git', 'add', target])

for source in jpgs:
    im = Image.open(source)
    print(source, im.size)
    if im.size[0] > 640:
        cmd = ['convert', '-resize', '640x', source, source]
        print(' '.join(cmd))
        subprocess.run(cmd)
        subprocess.run(['git', 'add', source])

open('index.md', 'w', encoding='utf8').write(content)
subprocess.run(['git', 'add', 'index.md'])

os.chdir(os.environ.get('GITHUB_WORKSPACE'))

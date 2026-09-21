import glob
import json
import os

os.chdir(os.environ.get('GITHUB_WORKSPACE'))

output = ''

output += '| 項目 | 狀態 |\n'
output += '| --- | --- |\n'

with open('pro/problem.json', 'r', encoding='utf8') as f:
    problemjson = json.load(f)

with open('pro/subtasks.json', 'r', encoding='utf8') as f:
    subtasksjson = json.load(f)

keys = [
    'name',
    'title',
]
for key in keys:
    text = ''
    if isinstance(problemjson[key], str) and 'TODO' in problemjson[key]:
        icon = ':x:'
    else:
        icon = ':white_check_mark:'
        text = '<br>{}'.format(problemjson[key])
    output += '| {} | [{}](pro/problem.json){} |\n'.format(key, icon, text)

keys = [
    'memory_limit',
    'time_limit',
    'has_checker',
]
for key in keys:
    output += '| {} | {} |\n'.format(key, problemjson[key])

folders = [
    'gen',
    'solution',
    'validator',
]
for folder in folders:
    todos = []
    for file in glob.glob('pro/{}/**'.format(folder), recursive=True):
        if os.path.isdir(file):
            continue
        with open(file, 'r', encoding='utf8') as f:
            try:
                content = f.read()
            except Exception as e:
                print('Ignore {}'.format(file))
                continue
            if 'TODO' in content:
                todos.append(file)
    if len(todos) == 0:
        output += '| {} | [:white_check_mark:](pro/{}) |\n'.format(folder, folder)
    else:
        output += '| {} | [:x:](pro/{})'.format(folder, folder)
        for file in todos:
            output += '<br>[{}]({})'.format(os.path.basename(file), file)
        output += ' |\n'

output += '| subtasks.json<br>global_validators | '
if len(subtasksjson['global_validators']) == 0:
    icon = ':warning:'
    text = ' Not set'
else:
    icon = ':white_check_mark:'
    text = ''
output += '[{}](pro/subtasks.json){} |\n'.format(icon, text)

if os.path.exists('pro/tests/0-01.in'):
    icon = ':white_check_mark:'
else:
    icon = ':x:'
auto = ''
if os.path.exists('pro/gen/DISABLE_AUTO_BUILD'):
    auto = '<br>[Auto build disabled](pro/gen/DISABLE_AUTO_BUILD)'
output += '| tests | [{}](pro/tests){} |\n'.format(icon, auto)

with open('pro/statement/index.md', 'r', encoding='utf8') as f:
    content = f.read()
if 'TODO' in content:
    icon = ':x:'
else:
    icon = ':white_check_mark:'
output += '| statement/index.md | [{}](pro/statement/index.md) |\n'.format(icon)

if os.path.exists('pro/statement/index.pdf'):
    icon = ':white_check_mark:'
else:
    icon = ':x:'
auto = ''
if os.path.exists('pro/statement/DISABLE_AUTO_BUILD'):
    auto = '<br>[Auto build disabled](pro/statement/DISABLE_AUTO_BUILD)'
output += '| statement/index.pdf | [{}](pro/statement/index.pdf){} |\n'.format(icon, auto)

output = output.lstrip()

reportpath = os.environ.get('REPORTPATH')

try:
    with open(reportpath, 'r', encoding='utf8') as f:
        text = f.read()
except FileNotFoundError:
    text = ''

flag1 = '<!-- progress start -->'
flag2 = '<!-- progress end -->'
try:
    idx1 = text.index(flag1)
    idx2 = text.index(flag2)
except ValueError:
    text += '\n## Progress\n{}\n{}\n'.format(flag1, flag2)
    idx1 = text.index(flag1)
    idx2 = text.index(flag2)

text = text[:idx1] + flag1 + '\n\n' + output + '\n' + text[idx2:]
with open(reportpath, 'w', encoding='utf8') as f:
    f.write(text)

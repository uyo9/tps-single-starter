import json
import os

os.chdir(os.environ.get('GITHUB_WORKSPACE'))

with open('pro/subtasks.json', 'r', encoding='utf8') as f:
    subtasks = json.load(f)['subtasks']

all_subtasks = []
for subtask in sorted(subtasks.values(), key=lambda v: v['index']):
    if subtask['index'] == 0:
        continue
    all_subtasks.append((subtask['score'], subtask['text']))

output = '| 子任務 | 分數 | 額外限制 |\n'
output += '| --- | --- | --- |\n'
for i, subtask in enumerate(all_subtasks):
    output += '| {} | {} | {} |\n'.format(i + 1, subtask[0], subtask[1])

reportpath = os.environ.get('REPORTPATH')

try:
    with open(reportpath, 'r', encoding='utf8') as f:
        text = f.read()
except FileNotFoundError:
    text = ''

flag1 = '<!-- subtasks start -->'
flag2 = '<!-- subtasks end -->'
try:
    idx1 = text.index(flag1)
    idx2 = text.index(flag2)
except ValueError:
    text += '\n## Subtasks\n{}\n{}\n'.format(flag1, flag2)
    idx1 = text.index(flag1)
    idx2 = text.index(flag2)

text = text[:idx1] + flag1 + '\n\n' + output + '\n' + text[idx2:]
with open(reportpath, 'w', encoding='utf8') as f:
    f.write(text)

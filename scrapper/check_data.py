from pathlib import Path

pathlist = Path('files').glob('**/*.txt')

for path in pathlist:
    print(str(path))
    lines = []
    with open(str(path), 'r', encoding='utf-8') as file:
        for index, line in enumerate(file):
            line = line.replace(u'\u200b', u'')
            if not line.strip().endswith('.') and not line.strip().endswith(']'):
                print('Line {}'.format(index+1))
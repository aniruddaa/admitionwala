import os
root = r'c:\Users\hp\Desktop\New folder (3)\templates'
print('Scanning', root)
for dirpath, dirnames, filenames in os.walk(root):
    for fn in sorted(filenames):
        path = os.path.join(dirpath, fn)
        try:
            with open(path, encoding='utf-8') as f:
                s = f.read()
        except Exception as e:
            print('Error reading', path, e)
            continue
        open_cnt = s.count('{% block site_header %}')
        close_cnt = s.count('{% endblock site_header %}')
        if open_cnt or close_cnt:
            print(os.path.relpath(path, root), 'open={}, close={}'.format(open_cnt, close_cnt))

print('Done')

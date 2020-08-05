import os


def append_json(json_str, file_name, encoding='utf-8'):
    with open(file_name, 'a', encoding=encoding) as f:
        f.write(json_str)
        f.write('\n')

def write_json(json_str, file_name, encoding='utf-8'):
    with open(file_name, 'w', encoding=encoding) as f:
        f.write(json_str)
        f.write('\n')
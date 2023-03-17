from os import getcwd

from .file_handler import find_file


def get_readme(path: str = getcwd(), name: str = 'README', file_type: str = 'md'):
    file_path = find_file(f'{name}.{file_type}', path, True)
    print(file_path)

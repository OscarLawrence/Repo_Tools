from os import getcwd, listdir, access, W_OK, walk
from os.path import join, dirname, isdir, basename, expanduser
from glob import glob

def is_valid(value, rules):
    for requirement in rules:
        if not requirement(value):
            return False
    return True

def find_file(filename: str, directory: str = getcwd(), recursive: bool = True, requirements: list=[], eager:bool=False, skip_hidden: bool=True):
    if not access(directory, mode=W_OK):
        return None
    if skip_hidden and basename(directory).startswith('.'):
        return None
    files = listdir(directory)
    if filename in files and is_valid(join(directory, filename), requirements):
        return join(directory, filename)
    if recursive:
        for root, _, files in walk(expanduser('~/')):
            found = find_file(filename, root, recursive=False, requirements=requirements, eager=eager)
            if found:
                return found
    return None

def find_files(filename: str, directory:str = getcwd(), recursive: bool = True, requirements: list=[], eager:bool=False):
    files = []
    found = True
    while found:
        found = find_file(filename, directory, recursive, requirements=[*requirements, lambda v: v not in files], eager=eager)
        if found:
            files.append(found)
    return files

def should_exclude(exclude: list, path: str = getcwd()):
    for to_exclude in exclude:
        if to_exclude in path:
            return True
    return False

def get_to_exclude(exclude: list, path: str = getcwd()):
    to_exclude = []
    for ex in exclude:
        to_exclude += glob(join(path, ex))
    return to_exclude

def find(name: str, path: str = getcwd(), walk_down: bool = False, walk_up: bool = False, eager: bool = False, rules: list = [], multi: bool=False, root: str=expanduser('~/'), exclude: list = [], skip_hidden: bool = True, done: list=[]):
    if skip_hidden and not '.*' in exclude:
        exclude.append('.*')
    
    found = [] if multi else None
    # if path in done:
    #     return found
    to_exclude = get_to_exclude(exclude, path)
    files = [f for f in listdir(path)]
    file_path = join(path, name)
    if name in files and not file_path in to_exclude and is_valid(file_path, rules):
        if multi:
            found.append(file_path)
        else:
            return file_path
    done.append(path)
    
    if walk_down:
        dirs = [join(path, p) for p in files if isdir(join(path, p)) and not join(path, p) in to_exclude]
        
        for dir in dirs:
            f = find(name, dir, walk_down=True, walk_up=False, eager=False, rules=rules, multi=multi, root=root, exclude=exclude, skip_hidden=skip_hidden, done=done)
            if multi:
                found += f
            else:
                return f
    if walk_up and dirname(path) != path:
        parent = dirname(path)
        f = find(name, parent, walk_down=eager, walk_up=True, eager=eager, rules=rules, multi=multi, root=root, exclude=exclude, skip_hidden=skip_hidden, done=done)
        if multi:
            found += f
        else:
            return f
    done = []
    return found

def find_old(name:str, dir:str = getcwd(), do_walk: bool=True, eager:bool=False, rules: list = [], multi: bool=False, skip_hidden: bool=True, root: str=expanduser('~/'), exclude: list = []):
    found = [] if multi else None
    if should_exclude(exclude, dir) or skip_hidden and dir.startswith('.') or not access(dir, mode=W_OK):
        return found
    
    files = listdir(dir)
    if name in files and is_valid(join(dir, name), rules):
        if multi:
            found.append(join(dir, name))
        else:
            return join(dir, name)
    if eager or do_walk:
        d = root if eager else dir
        files = listdir(root) if eager else files
        for sub in [f for f in files if isdir(join(d, f)) and not should_exclude(exclude, join(d, f)) and not f.startswith('.') and access(join(d, f), mode=W_OK)]:
            result = find_old(name, join(d, sub), do_walk=True, eager=False, rules=rules, multi=multi, skip_hidden=skip_hidden, root=root, exclude=exclude)
            if multi:
                found += result
            elif result:
                return result
    return found
            
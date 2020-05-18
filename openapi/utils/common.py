from openapi.utils.exception_handle import FileError
from logbook import Logger
import os
import json

log = Logger('utils/common')

def save_file(path, file):
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
            with open(os.path.join(path, "__init__.py"), mode="w", encoding="utf-8"):
                pass
        file.save(os.path.join(path, file.filename))
        return os.path.join(path, file.filename)
    except Exception as e:
        log.error(f'type:{type(e)}, {e}')
        raise FileError(title=f'保存文件{file}异常', detail=f'{e}')

def is_exist_path(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
    except Exception as e:
        os.makedirs(path)
        log.error(f'type:{type(e)}, {e}')


def is_exist_python_path(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
            open(f'{path}/__init__.py', 'w')
    except Exception as e:
        os.makedirs(path)
        open(f'{path}/__init__.py', 'w')
        log.error(f'type:{type(e)}, {e}')

def delete_file(path, file):
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            raise FileError(title='删除的脚本不存在', detail=f'脚本{path}不存在')
    except Exception as e:
        log.error(f'type:{type(e)}, {e}')
        raise FileError(title=f'删除文件{file}异常', detail=f'{e}')

def update_file(path, file):
    try:
        if os.path.exists(path):
            file.save(path)
        else:
            raise FileError(title=f'更新文件不存在', detail=f'更新文件{file.filename}不存在')
    except Exception as e:
        log.error(f'type:{type(e)}, {e}')
        raise FileError(title=f'更新文件{file.filename}异常', detail=f'{e}')

def char_changer(target):
    if isinstance(target, dict):
        return json.dumps(target)
    elif isinstance(target, list):
        return json.dumps(target)
    else:
        return str(target)
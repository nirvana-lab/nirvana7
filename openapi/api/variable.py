# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from openapi.service import  variable
from flask import g

def globalvar(project_id):
    try:
        data = variable.get_global_variable_by_id(project_id)
        return {
            'data': data
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'更新全局变量异常', detail=f'{e}')

def globalupdate(project_id, body):
    try:
        variable.update_global_variable(project_id, body, g.username)
        return {
            'title': '更新全局变量成功',
            'detail': '更新全局变量成功',
        }
    except Exception as e:
        raise DefalutError(title=f'更新全局变量异常', detail=f'{e}')

def list(project_id, file_path, ref):
    try:
        data = variable.get_project_variable_list(project_id, file_path, ref)
        return {
            'data': data
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取项目变量列表异常', detail=f'{e}')

def update(project_id, file_path, ref, body):
    try:
        variable.update_project_variable(project_id, file_path, ref, body, g.username)
        return {
            'title': '更新项目变量成功',
            'detail': '更新项目变量成功'
        }
    except Exception as e:
        raise DefalutError(title=f'更新项目变量异常', detail=f'{e}')
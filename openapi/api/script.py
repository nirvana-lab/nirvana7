# -*- coding: utf-8 -*-
import connexion
from openapi.service import script
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g

def list(project_id):
    try:
        data = script.get_script_list_by_project_id(project_id)
        return {
            'data': data
        }
    except Exception as e:
        raise DefalutError(title=f'获取脚本列表异常', detail=f'{e}')


def create(project_id, body):
    try:
        script.create_script(project_id, body, g.username)
        return {
            'title': '创建脚本成功',
            'detail': '创建脚本成功'
        }
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'创建脚本异常', detail=f'{e}')


def update(script_id, body):
    try:
        script.update_script_content_by_script_id(script_id, body, g.username)
        return {
            'title': '更新脚本成功',
            'detail': '更新脚本成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'更新脚本异常', detail=f'{e}')

def delete(script_id):
    try:
        script.delete_script_by_script_id(script_id, g.username)
        return {
            'title': '删除脚本成功',
            'detail': '删除脚本成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'删除脚本异常', detail=f'{e}')

def content(script_id):
    try:
        data = script.get_content_by_script_id(script_id)
        return {
            'data': data
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取脚本详情异常', detail=f'{e}')

def select(project_id):
    try:
        data = script.get_function_list_and_args(project_id)
        return {
            'data': data
        }
    except Exception as e:
        raise DefalutError(title=f'获取脚本参数列表异常', detail=f'{e}')
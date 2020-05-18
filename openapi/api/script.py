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


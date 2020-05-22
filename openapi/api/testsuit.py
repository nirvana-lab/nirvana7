# -*- coding: utf-8 -*-
import connexion
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g
from openapi.service import testsuit

def create(project_id, body):
    try:
        testsuit.create_testsuit(project_id=project_id, body=body, user=g.username)
        return {
            'title': '创建测试套件成功',
            'detail': '创建测试套件成功'
        }
    except IsExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'创建测试套件异常', detail=f'{e}')

def list(project_id):
    try:
        data = testsuit.get_testsuit_list_by_project_id(project_id)
        return {
            'data': data
        }
    except Exception as e:
        raise DefalutError(title=f'获取测试套件列表异常', detail=f'{e}')

def run(suit_id):
    try:
        report_path = testsuit.run_testsuit_by_suit_id(suit_id, g.username)
        return {
            'data':{
                'report_path': report_path
            }
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'运行测试套件异常', detail=f'{e}')

def update(suit_id, body):
    try:
        testsuit.update_testsuit_content_by_suit_id(suit_id, body, g.username)
        return {
            'title': '更新测试套件成功',
            'detail': '更新测试套件成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'更新测试套件异常', detail=f'{e}')

def content(suit_id):
    try:
        data = testsuit.get_testsuit_content_by_suit_id(suit_id)
        return {
            'data': data
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取测试套件异常', detail=f'{e}')

def delete(suit_id):
    try:
        testsuit.delete_testsuit_by_suit_id(suit_id, g.username)
        return {
            'title': '删除测试套件成功',
            'detail': '删除测试套件成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取测试套件异常', detail=f'{e}')
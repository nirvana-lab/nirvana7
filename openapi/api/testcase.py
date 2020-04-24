# -*- coding: utf-8 -*-
import connexion
from openapi.service import testcase
from openapi.utils.exception_handle import DefalutError, IsExist, IsNotExist
from flask import g

def list(project_id, file_path, ref, method, path):
    try:
        token = connexion.request.headers.get('Authorization')
        case_list = testcase.get_testcase_list_by_method_and_path(project_id, file_path, ref, method, path, token, g.username)
        return {
            'data': case_list
        }
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取测试用例列表异常', detail=f'{e}')


def create(project_id, file_path, method, path, body):
    try:
        testcase.create_testcase(project_id, file_path, method, path, body, user=g.username)
        return {
            'title': '创建测试用例成功',
            'detail': '创建测试用例成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'创建测试用例异常', detail=f'{e}')


def update(case_id, body):
    try:
        testcase.update_testcase(case_id, body, g.username)
        return {
            'title': '更新测试用例成功',
            'detail': '更新测试用例成功'
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'更新测试用例异常', detail=f'{e}')

def run(case_id):

    import pytest
    # result = pytest.main(['/Users/xumin/jo/nirvana7/openapi/specs/test_case.py'])
    # print(result)

    import os
    res = os.popen(f'pytest /Users/xumin/jo/nirvana7/openapi/specs/test_case.py --case={case_id} --capture=no')

    print(f'{res.read()}')




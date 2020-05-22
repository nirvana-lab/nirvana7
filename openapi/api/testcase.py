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

def delete(case_id):
    try:
        testcase.delete_testcase_by_id(case_id, g.username)
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'删除测试用例异常', detail=f'{e}')

def content(case_id):
    try:
        content = testcase.get_content_by_case_id(case_id)
        return {
            'case_id': case_id,
            'content': content
        }
    except IsNotExist as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'获取测试用例内容异常', detail=f'{e}')


def run(case_id, env_id):
    try:
        result = testcase.run_test_case(case_id, env_id)
        return result
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title=f'执行测试用例异常', detail=f'执行id为{case_id}的测试用例异常:{e}')

def all(project_id):
    try:
        data = testcase.get_all_testcase_by_repo_id_and_file_path(project_id)
        return {
            'data': data
        }
    except Exception as e:
        raise DefalutError(title=f'获取测试用例列表异常', detail=f'{e}')
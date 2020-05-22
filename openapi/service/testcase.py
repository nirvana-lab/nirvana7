# -*- coding: utf-8 -*-
from openapi.db.models.gitfile import GitFile
from openapi.db.models.testcase import TestCase
from openapi.db.models.env import Env
from logbook import Logger
from openapi.utils import gitlab_handle,case_handle
from openapi.utils.exception_handle import IsExist, IsNotExist, DefalutError
import yaml
import json
from openapi.config import config
from openapi.utils.common import init_time_stamp

log = Logger('service/testcase')

def get_testcase_list_by_method_and_path(project_id, file_path, ref, method, path, token, user):
    method = method.lower()
    file_name, file_path, ref, blob_id, commit_id, last_commit_id, re_content = gitlab_handle.get_file_content_from_gitlab(project_id, file_path, ref, token)
    if file_name.endswith(('.yml', '.yaml')):
        re_content = yaml.load(re_content)
    elif file_name.endswith('json'):
        re_content = json.loads(re_content)

    pk = _is_repo(project_id, file_name, file_path, ref, blob_id, commit_id, last_commit_id, re_content, user)
    case_list = TestCase.get_case_list_by_git_file_id(pk, method, path)
    return case_list

def create_testcase(project_id, file_path, method, path, body, user):
    file_pk = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    case = body.get('case')
    description = body.get('description')
    setup = body.get('setup')
    parameters = body.get('parameters')
    request_body = body.get('body')
    teardown = body.get('teardown')
    validator = body.get('validator')

    TestCase.create(file_pk, method, path, case, description, setup, parameters, request_body, teardown, validator, user)

def update_testcase(case_id, body, user):
    case = body.get('case')
    description = body.get('description')
    setup = body.get('setup')
    parameters = body.get('parameters')
    request_body = body.get('body')
    teardown = body.get('teardown')
    validator = body.get('validator')
    TestCase.update(case_id, case, description, setup, parameters, request_body, teardown, validator, user)

def delete_testcase_by_id(case_id, user):
    TestCase.delete_case_by_id(case_id, user)

def get_content_by_case_id(case_id):
    content = TestCase.get_case_content_by_id(case_id)
    return content

def _is_repo(project_id, file_name, file_path, ref, blob_id, commit_id, last_commit_id, content, user):
    '''
    根据信息查询gitfile数据库，
    如果文件已经存在，直接返回pk
    如果文件不存在，创建数据，并且返回pk
    '''
    try:
        gitfile_pk = GitFile.get_obj_by_project_id_and_file_path_and_update_content(project_id, file_path, blob_id, commit_id, last_commit_id, content, user)
        return gitfile_pk
    except IsNotExist:
        gitfile_pk = GitFile.create_obj_by_project_id_and_file_path(project_id, file_name, file_path, ref, blob_id, commit_id, last_commit_id, content, user)
        return gitfile_pk
    except DefalutError as e:
        raise DefalutError(title=f'获取文件异常', detail=f'{e.detail}')

def run_test_case(case_id, env_id):

    project_id = Env.get_project_id_by_env_id(env_id)
    from httprunner.api import HttpRunner
    httprunner_log_path = config.NirvanaConfig().httprunner_log_save_path()
    log_name = f'{httprunner_log_path}/{init_time_stamp()}.txt'
    # runner = HttpRunner(log_level="DEBUG", log_file=log_name)
    runner = HttpRunner(log_file=log_name)

    test_case_parse = case_handle.TestCaseParse(case_id, env_id, project_id)
    case = test_case_parse.get_httprunner_test_case_json()
    result = runner.run(case)

    with open(log_name, 'r') as f:
        data = f.read()
    result['console'] = data
    return result

def get_all_testcase_by_repo_id_and_file_path(project_id, file_path):
    gitfile_pk = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    datas = TestCase.get_all_case_by_file_id(gitfile_pk)
    data_dict= {}
    for data in datas:
        tmp_key = f'{data.get("method")}|{data.get("path")}'
        if tmp_key in data_dict.keys():
            data_dict[tmp_key].append({'case': data.get('case'), 'id': data.get('id')})
        else:
            data_dict[tmp_key] = [{'case': data.get('case'), 'id': data.get('id')}]
    return data_dict

import requests
import json
import jsonpath
from openapi.utils.pg_handle import Postgres
import copy
from openapi.db.models.testcase import TestCase
from openapi.db.models.env import Env
from openapi.db.models.gvariable import GlobalVariable
from openapi.db.models.variable import Variable
from openapi.db.models.script import Script
from openapi.utils.exception_handle import IsExist, IsNotExist, DefalutError
from httprunner.loader.load import load_module_functions

def case_init(case_handle, variable_init):
    path = case_handle.get('path')
    method = case_handle.get('method')
    case = case_handle.get('case')
    description = case_handle.get('description')
    host = variable_init.get('host')
    url = f'{host}{path}'
    setup = case_handle.get('setup')
    parameters = case_handle.get('parameters')
    body = case_handle.get('body')
    validator = case_handle.get('validator')
    teardown = case_handle.get('teardown')
    return url, method, case, description, setup, parameters, body, teardown, validator


def params_handle(params, url, variable_dict):
    headers = {}
    query = {}
    for param in params:
        if param.get('in') == 'header':
            headers[param.get('key')] = var_or_func_replace(param.get('value'), variable_dict)
        elif param.get('in') == 'path':
            url = url.replace("{" + param.get('key') + "}", var_or_func_replace(param.get('value'), variable_dict))
        elif param.get('in') == 'query':
            query[param.get('key')] = var_or_func_replace(param.get('value'), variable_dict)
    return url, headers, query


def var_or_func_replace(content, variable_dict):
    if content.startswith("{") and content.endswith("}"):
        return variable_dict[content[1: -1]]
    elif content.startswith("${") and content.endswith(".py}"):
        pass
    else:
        return content


def send_request(method, url, **kwargs):
    request_session = requests.Session()
    resp = request_session.request(method, url, **kwargs)
    return resp

def resp_info(resp):
    status_code = resp.status_code
    response_time = int(resp.elapsed.microseconds / 1000.0)
    ##todo 这里需要做一个判断，是否要把返回的内容做json处理，现在默认都需要处理
    content = json.loads(resp.content)
    return status_code, response_time, content

# def assert_handle()

def get_variable_by_env_id(env_id):
    pg_class = Postgres()
    repo_id = pg_class.get_repo_id_by_env_id(int(env_id))
    global_variable = pg_class.get_global_variable_by_repo_id(repo_id)
    env_variable = pg_class.get_variable_by_env_id(env_id)
    tmp_variable = copy.deepcopy(global_variable)
    tmp_variable.update(env_variable)
    return tmp_variable


class TestCaseParse(object):

    def __init__(self, case_id, env_id, project_id):
        self.case_id = case_id
        self.env_id = env_id
        self.project_id = project_id
        self.host = ''
        self.test_case_dict = {}
        self.case_json = {
            "testcases":[
                {
                    "config": {
                        "name": "nirvana",
                        "variables": []
                    },
                    "teststeps": [
                    ]

                }
            ]
        }

    def _variable_parse(self, global_variable, env_variable):
        tmp_variable = copy.deepcopy(global_variable)
        tmp_variable.update(env_variable)
        tmp_list = []
        for k, v in tmp_variable.items():
            tmp_list.append({k: v})
        return tmp_list

    def set_func(self):
        func_list = Script.list(self.project_id)
        module_dict = {}
        if func_list:
            for func in func_list:
                import_module = __import__(f"openapi.script.{self.project_id}.{func.get('script_file')[:-3]}", fromlist=True)
                tmp_dict = load_module_functions(import_module)
                module_dict.update(tmp_dict)
        self.case_json['project_mapping'] = { 'functions': module_dict}

    def set_variable(self):
        project_id = Env.get_project_id_by_env_id(self.env_id)
        global_variable = GlobalVariable.get_global_variable(project_id)
        env_variable = Variable.get_data_variable_by_env_id(self.env_id)
        if env_variable.get('host'):
            self.host = env_variable.get('host')
        else:
            raise DefalutError(title=f'请在环境变量中设置host', detail=f'在环境id为{self.env_id}的环境变量中没有找到环境变量host')

        variables = self._variable_parse(global_variable, env_variable)
        if variables:
            self.case_json["testcases"][0]["config"]["variables"] = variables

    def set_steps(self):
        test_case = TestCase.get_case_content_by_id(self.case_id)
        tmp_case = {}
        tmp_case['name'] = test_case.get('case')

        #处理url，请求参数，请求头
        url = self.host + test_case.get('path')
        query_string = None
        headers_dict = {}
        for param in test_case.get('parameters'):
            if param.get('in') == 'header':
                headers_dict[param.get('key')] = param.get('value')
            elif param.get('in') == 'path':
                url = url.replace("{" + param.get('key') + "}", param.get('value'))
            elif param.get('in') == 'query':
                query_string = self._query_parse(query_string, param)
        if query_string:
            url = url + query_string
        tmp_case['request'] = {
            'url': url,
            'method': test_case.get('method').upper(),
            'headers': headers_dict
        }

        # 处理body
        request_body = test_case.get('body')
        if request_body:
            request_body = json.loads(request_body)
            tmp_case['request']['json'] = request_body

        # 处理断言
        validate_list = []
        for validate in test_case.get('validator'):
            tmp_dict = {}
            if validate.get('key_type') == 'integer':
                expect_value = int(validate.get('expect_value'))
            elif validate.get('key_type') == 'string':
                expect_value = str(validate.get('expect_value'))
            else:
                expect_value = validate.get('expect_value')

            tmp_dict[validate.get('comparator')] = [validate.get('key'), expect_value]
            validate_list.append(tmp_dict)
        tmp_case['validate'] = validate_list
        self.case_json["testcases"][0]["teststeps"].append(tmp_case)

    def get_httprunner_test_case_json(self):
        self.test_case_dict = TestCase.get_case_content_by_id(self.case_id)
        self.set_func()
        self.set_variable()
        self.set_steps()
        return self.case_json

    def _query_parse(self, query_string, content):
        if query_string:
            query_string = f'{query_string}&{content.get("key")}={content.get("value")}'
        else:
            query_string = f'?{content.get("key")}={content.get("value")}'
        return query_string




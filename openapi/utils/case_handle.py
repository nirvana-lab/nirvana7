import requests
import json
import jsonpath

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

def validate_handle(validators, resp_content):
    for validator in validators:
        print(validator)
        expect_value = eval_expect_value(validator.get('expect_value'))
        actual_value = eval_actual_value(validator.get('key'), resp_content)


def eval_expect_value(expect_value):
    return expect_value

def eval_actual_value(actual_key, resp_content):
    actual_value = jsonpath.jsonpath(resp_content, actual_key)
    if actual_value:
        if len(actual_value) == 1:
            return actual_value[0]
        else:
            return actual_value
    else:
        return actual_value

# def assert_handle()
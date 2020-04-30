# -*- coding: utf-8 -*-
import pytest
from openapi.utils.pg_handle import Postgres
from openapi.utils.case_handle import *
from openapi.utils.common import print_content
import copy

@pytest.fixture()
def case_handle(case_id):
    postgres = Postgres()
    case_content = postgres.get_case_content_by_id(case_id)
    method = case_content[1]
    path = case_content[2]
    case = case_content[3]
    description = case_content[4]
    setup = case_content[10]
    parameters = case_content[11]
    body = case_content[12]
    validator = case_content[13]
    teardown = case_content[14]
    return {
        'method': method,
        'path': path,
        'case': case,
        'description': description,
        'setup': setup,
        'parameters': parameters,
        'body': body,
        'validator': validator,
        'teardown': teardown
    }

@pytest.fixture()
def variable_init(case_id):
    return {
        'host': 'https://gitlab.daocloud.io/api/v4',
        'project_id': '1662',
        'token': 'znNHzjCz_P6mgeUXbee6',
        'ref': 'master'
    }


def test_base(case_handle, variable_init):
    url, method, case, description, setup, parameters, body, teardown, validator = case_init(case_handle, variable_init)
    variable_dict = copy.deepcopy(variable_init)
    url, headers, query = params_handle(parameters, url, variable_dict)

    print_content(f'case: {case}\ndescription: {description}\nurl: {url}\nmethod: {method}', 'case_info')
    print_content(variable_dict, 'variable')
    print_content(headers, 'headers')
    print_content(query, 'query')
    resp = send_request(method, url, headers=headers, params=query)
    status_code, response_time, resp_content = resp_info(resp)
    # print_content(f'status_code: {status_code}\nresponse_time: {response_time}\nresp_content: {resp_content}', 'response_info')

    validate_handle(case_handle.get('validator'), resp_content)
    assert 1 < 2
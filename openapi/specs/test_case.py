import pytest
from openapi.utils.pg_handle import Postgres
from openapi.utils.case_handle import *

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


def test_base(case_handle):
    url, method, case, description, setup, parameters, body, teardown, validator = case_init(case_handle)

    url, headers, query = params_handle(parameters, url)
    print(url)
    print(method)
    print(case)
    print(description)
    assert 1 < 2


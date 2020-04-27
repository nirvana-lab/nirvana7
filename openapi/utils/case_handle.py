def case_init(case_handle):
    path = case_handle.get('path')
    method = case_handle.get('method')
    case = case_handle.get('case')
    description = case_handle.get('description')
    host = 'https://gitlab.daocloud.io/api/v4'
    url = f'{host}{path}'

    setup = case_handle.get('setup')
    parameters = case_handle.get('parameters')
    body = case_handle.get('body')
    validator = case_handle.get('validator')
    teardown = case_handle.get('teardown')
    return url, method, case, description, setup, parameters, body, teardown, validator


def params_handle(params, url):
    headers = {}
    query = {}
    for param in params:
        print(param)
    return "url", "headers", "query"



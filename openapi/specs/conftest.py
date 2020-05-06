import pytest


# def pytest_addoption(parser):
#     parser.addoption("--cmdopt", action="store", default="type1",
#                      help="my option: type1 or type2")



# @pytest.fixture()
# def get_case_id(request):
#     case_list = request.config.getoption("--cmdopt").split(',')
#     return case_list


#
# @pytest.fixture(params=cmdopt)
# def get_case_id(request):
#     print("in dadf")
#     return request.param

def pytest_addoption(parser):
    parser.addoption("--case", action="store",
        help="run all combinations")
    parser.addoption('--env', action="store")

def pytest_generate_tests(metafunc):
    if 'case_id' in metafunc.fixturenames:
        if metafunc.config.getoption('case'):
            list_id = metafunc.config.getoption("--case").split(',')
        else:
            list_id = []
        print(list_id)
        metafunc.parametrize("case_id", list_id)
    if 'env' in metafunc.fixturenames:
        print("44444444")
        print(metafunc.config.getoption('env'))
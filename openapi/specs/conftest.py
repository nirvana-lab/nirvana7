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

def pytest_generate_tests(metafunc):
    if 'case_id' in metafunc.fixturenames:
        # print(metafunc.config.getoption("--test"))
        # print(type(metafunc.config.getoption("--test")))
        if metafunc.config.getoption('case'):
            list_id = metafunc.config.getoption("--case").split(',')
            print(list_id)
        else:
            list_id = [1, 2]
        metafunc.parametrize("case_id", list_id)
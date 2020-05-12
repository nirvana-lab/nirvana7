import pytest

def pytest_addoption(parser):
    parser.addoption("--case", action="store",
        help="run all combinations")
    parser.addoption("--env", action="store",
        help="run all combinations")
def pytest_generate_tests(metafunc):
    if 'case_id' in metafunc.fixturenames:
        if metafunc.config.getoption('case'):
            list_id = metafunc.config.getoption("--case").split(',')
        else:
            list_id = []
        metafunc.parametrize("case_id", list_id)
        metafunc.parametrize('env_id', [metafunc.config.getoption('env')])
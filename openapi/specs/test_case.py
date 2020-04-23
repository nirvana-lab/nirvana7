import pytest
from copy import deepcopy

@pytest.fixture()
def case_handle(param1):
    if param1 == '1':
        return 1
    else:
        return 6

def test_compute(case_handle):
    assert int(case_handle) < 4
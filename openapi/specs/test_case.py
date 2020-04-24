import pytest
from openapi.db.models import testcase
from copy import deepcopy

@pytest.fixture()
def case_handle(case_id):
    print(case_id)
    if case_id == '1':
        return 1
    else:
        return 6

def test_compute(case_handle):
    assert int(case_handle) < 4
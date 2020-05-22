# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger
from openapi.db.models.gitfile import GitFile

log = Logger('db/testcase')

class TestCase(db.Entity):

    _table_ = 'testcase'

    id = PrimaryKey(int, auto=True)
    method = Required(str)
    path = Required(str)
    case = Required(str)
    description = Optional(str)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    user = Required(str)
    info = Optional(Json)
    setup = Optional(Json)
    parameters = Optional(Json)
    body = Optional(str)
    validator = Optional(Json)
    teardown = Optional(Json)
    gitfile = Required(GitFile)

    @classmethod
    @db_session
    def create(cls, file_id, method, path, case, description, setup, parameters, body, teardown, validator, user):
        TestCase(method=method, path=path, case=case, description=description, setup=setup, parameters=parameters,
                 body=body, teardown=teardown, validator=validator, user=user, gitfile=file_id)

    @classmethod
    @db_session
    def update(cls, case_id, case, description, setup, parameters, body, teardown, validator, user):
        obj = get(n for n in TestCase if n.id == case_id and n.delete_at == None)
        if obj:
            obj.case = case
            obj.description = description
            obj.setup = setup
            obj.parameters = parameters
            obj.body = body
            obj.teardown = teardown
            obj.validator = validator
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='测试用例不存在', detail=f'id为{case_id}的测试用例不存在')

    @classmethod
    @db_session
    def get_case_list_by_git_file_id(cls, file_id, method, path):
        case_list = []
        objs = select(n for n in TestCase if n.gitfile.id == file_id and n.delete_at == None and
                      n.method == method and n.path == path)
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'case': obj.case,
                'description': obj.description
            }
            case_list.append(tmp_dict)
        return case_list

    @classmethod
    @db_session
    def get_case_content_by_id(cls, case_id):
        obj = get(n for n in TestCase if n.id == case_id and n.delete_at == None)
        if obj:
            return {
                'case': obj.case,
                'method': obj.method,
                'path': obj.path,
                'description': obj.description,
                'setup': obj.setup,
                'parameters': obj.parameters,
                'body': obj.body,
                'teardown': obj.teardown,
                'validator': obj.validator,
            }
        else:
            raise IsNotExist(title='测试用例不存在', detail=f'id为{case_id}的测试用例不存在')


    @classmethod
    @db_session
    def delete_case_by_id(cls, case_id, user):
        obj = get(n for n in TestCase if n.id == case_id and n.delete_at == None)
        if obj:
           obj.delete_at = datetime.datetime.utcnow()
           obj.user = user
        else:
            raise IsNotExist(title='测试用例不存在', detail=f'id为{case_id}的测试用例不存在')

    @classmethod
    @db_session
    def get_all_case_by_file_id(cls, file_id):
        data = []
        objs = select(n for n in TestCase if n.gitfile.id == file_id)
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'method': obj.method,
                'path': obj.path,
                'case': obj.case
            }
            data.append(tmp_dict)
        return data

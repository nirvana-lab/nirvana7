# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from logbook import Logger
from openapi.utils.exception_handle import IsExist, IsNotExist

log = Logger('db/gvariable')

class GlobalVariable(db.Entity):

    _table_ = 'global_variable'

    id = PrimaryKey(int, auto=True)
    project_id = Required(str)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    metadata = Required(Json, index=True)
    data = Required(Json, index=True)
    user = Required(str)
    info = Optional(Json)

    @classmethod
    @db_session
    def update_global_variable(cls, project_id, metadata, data, user):
        obj = get(n for n in GlobalVariable if n.project_id == project_id and n.delete_at == None)
        if obj:
            obj.data = data
            obj.metadata = metadata
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            GlobalVariable(project_id=project_id, metadata=metadata, data=data, user=user)

    @classmethod
    @db_session
    def get_global_metadata_variable(cls, project_id):
        obj = get(n for n in GlobalVariable if n.project_id == project_id and n.delete_at == None)
        if obj:
            data = {
                'project_id': obj.project_id,
                'metadata': obj.metadata
            }
            return data
        else:
            raise IsNotExist(title='全部变量不存在', detail=f'repo id为{project_id}的全局变量不存在')

    @classmethod
    @db_session
    def get_global_variable(cls, project_id):
        obj = get(n for n in GlobalVariable if n.project_id == project_id and n.delete_at == None)
        if obj:
            return obj.data
        else:
            raise IsNotExist(title='全部变量不存在', detail=f'repo id为{project_id}的全局变量不存在')
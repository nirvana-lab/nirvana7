# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from openapi.db.models.env import Env
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger
from openapi.db.models.env import Env

log = Logger('db/variable')

class Variable(db.Entity):

    _table_ = 'variable'

    id = PrimaryKey(int, auto=True)
    metadata = Required(Json, index=True)
    data = Required(Json, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    user = Required(str)
    info = Optional(Json)
    env = Required(Env)

    @classmethod
    @db_session
    def update_variable(cls, env_id, metadata, data, user):
        obj = get(n for n in Variable if n.env.id == env_id and n.env.delete_at == None
                  and n.delete_at == None)
        if obj:
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
            obj.metadata = metadata
            obj.data = data
        else:
            Variable(user=user, metadata=metadata, data=data, env=env_id)

    @classmethod
    @db_session
    def delete_variable_by_env_id(cls, env_id, user):
        obj = get(n for n in Variable if n.env.id == env_id and n.env.delete_at == None)
        if obj:
            obj.user = user
            obj.delete_at = datetime.datetime.utcnow()

    @classmethod
    @db_session
    def get_metadata_variable_by_env_id(cls, env_id):
        obj = get(n for n in Variable if n.env.id == env_id and n.env.delete_at == None
                  and n.delete_at == None)
        if obj:
            return obj.metadata
        else:
            raise IsNotExist(title='环境里没有设置项目变量', detail=f'环境id为{env_id}的环境下没有找到项目变量')

    @classmethod
    @db_session
    def get_data_variable_by_env_id(cls, env_id):
        obj = get(n for n in Variable if n.env.id == env_id and n.env.delete_at == None
                  and n.delete_at == None)
        if obj:
            return obj.data
        else:
            raise IsNotExist(title='环境里没有设置项目变量', detail=f'环境id为{env_id}的环境下没有找到项目变量')
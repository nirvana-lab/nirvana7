# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional, commit)
import datetime
from logbook import Logger
from openapi.db.models.gitfile import GitFile
from openapi.utils.exception_handle import IsExist, IsNotExist

log = Logger('db/env')

class Env(db.Entity):

    _table_ = 'env'

    id = PrimaryKey(int, auto=True)
    env = Required(str)
    description = Optional(str, nullable=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    user = Required(str)
    info = Optional(Json)
    gitfile = Required(GitFile)
    variable = Set('Variable')

    @classmethod
    @db_session
    def create(cls, file_id, env, description, user):
        obj = get(n for n in Env if n.env == env and n.delete_at == None and
                  n.gitfile.id == file_id and n.gitfile.delete_at == None)
        if obj:
            raise IsExist(title=f'环境名为{env}的环境已经存在', detail=f'已经存在的环境id为:{obj.id}')
        else:
            new_obj = Env(env=env, description=description, user=user, gitfile=file_id)
            commit()
            return new_obj.id


    @classmethod
    @db_session
    def list(cls, file_id):
        objs = select(n for n in Env if n.delete_at == None and n.gitfile.id == file_id
                      and n.gitfile.delete_at == None)
        env_list = []
        for obj in objs:
            tmp_dict = {}
            tmp_dict['id'] = obj.id
            tmp_dict['env'] = obj.env
            tmp_dict['description'] = obj.description
            env_list.append(tmp_dict)
        return env_list

    @classmethod
    @db_session
    def delete_env_by_id(cls, env_id, user):
        obj = get(n for n in Env if n.id == env_id and n.delete_at == None)
        if obj:
            obj.delete_at = datetime.datetime.utcnow()
            obj.user = user
        else:
            raise IsNotExist(title='删除的环境不存在', detail=f'环境id为{env_id}的环境不存在')

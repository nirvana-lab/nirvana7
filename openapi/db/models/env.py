# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
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

    @classmethod
    @db_session
    def create(cls, file_id, env, description, user):
        obj = get(n for n in Env if n.env == env and n.delete_at == None and
                  n.gitfile.id == file_id and n.gitfile.delete_at == None)
        if obj:
            raise IsExist(title=f'环境名为{env}的环境已经存在', detail=f'已经存在的环境id为:{obj.id}')
        else:
            Env(env=env, description=description, user=user, gitfile=file_id)

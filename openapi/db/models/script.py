# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger

log = Logger('db/script')

class Script(db.Entity):

    _table_ = 'script'

    id = PrimaryKey(int, auto=True)
    script = Required(str)
    script_file = Required(str)
    description = Optional(str)
    content = Required(str)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    project_id = Required(str)
    user = Required(str)
    info = Optional(Json)

    @classmethod
    @db_session
    def create(cls, project_id, script, script_file, description, content, user):
        obj = get(n for n in Script if n.script_file==script_file and n.delete_at == None)
        if obj:
            raise IsExist(title='脚本已经存在', detail=f'脚本{script_file} 已经存在')
        Script(project_id=project_id, script=script, script_file=script_file, description=description, content=content, user=user)

    @classmethod
    @db_session
    def list(cls, project_id):
        re_list = []
        objs = select(n for n in Script if n.delete_at == None and n.project_id == project_id)
        if objs:
            for obj in objs:
                tmp_dict = {
                    'id': obj.id,
                    'script': obj.script,
                    'script_file': obj.script_file,
                    'description': obj.description,
                    'content': obj.content
                }
                re_list.append(tmp_dict)
        return re_list
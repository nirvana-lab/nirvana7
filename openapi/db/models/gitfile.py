# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional, commit)
import uuid
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger

log = Logger('db/gitfile')

class GitFile(db.Entity):

    _table_ = 'gitfile'
    id = PrimaryKey(int, auto=True)
    project_id = Required(str)
    file_name = Required(str)
    file_path = Required(str)
    ref = Optional(str)
    blob_id = Required(str)
    commit_id = Optional(str)
    last_commit_id = Required(str)
    content = Required(Json)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime,  nullable=True)
    user = Required(str)
    info = Optional(Json)
    testcase = Set('TestCase')
    env = Set('Env')


    @classmethod
    @db_session
    def get_obj_by_project_id_and_file_path_and_update_content(cls, project_id, file_path, blob_id, commit_id, last_commit_id, content, user):
        obj = get(n for n in GitFile if n.project_id == project_id and n.delete_at == None
                  and n.file_path == file_path)
        if obj:
            if obj.blob_id != blob_id:
                obj.blob_id = blob_id
                obj.commit_id = commit_id
                obj.last_commit_id = last_commit_id
                obj.content = content
                obj.user = user
                obj.update_at = datetime.datetime.utcnow()
            return obj.id
        else:
            raise IsNotExist(title='获取文件不存在', detail=f'项目{project_id}下的文件{file_path}不存在')

    @classmethod
    @db_session
    def get_obj_pk_by_project_id_and_file_path(cls, project_id, file_path):
        obj = get(n for n in GitFile if n.project_id == project_id and n.delete_at == None
                  and n.file_path == file_path)
        if obj:
            return obj.id
        else:
            raise IsNotExist(title='获取文件不存在', detail=f'项目{project_id}下的文件{file_path}不存在')

    @classmethod
    @db_session
    def create_obj_by_project_id_and_file_path(cls, project_id, file_name, file_path, ref, blob_id, commit_id, last_commit_id, content, user):
        obj = get(n for n in GitFile if n.project_id == project_id and n.delete_at == None
                  and n.file_path == file_path)
        if obj:
            raise IsExist(title='文件已经存在', detail=f'proejct_id为{blob_id}, file_path为{file_path}的文件已存在')
        else:
            obj = GitFile(file_name=file_name, file_path=file_path, ref=ref, blob_id=blob_id, commit_id=commit_id,
                          last_commit_id=last_commit_id, content=content, user=user, project_id=project_id)
            commit()
            return obj.id
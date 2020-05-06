# -*- coding: utf-8 -*-
from openapi.db.models.gitfile import GitFile
from openapi.db.models.env import Env
from logbook import Logger
from openapi.db.models.variable import Variable
from openapi.utils.exception_handle import IsExist, IsNotExist, DefalutError


log = Logger('service/env')

def create_env(project_id, file_path, ref, body, user):
    file_id = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    env = body.get('env')
    description = body.get('description')
    env_id = Env.create(file_id, env, description, user)
    Variable.update_variable(env_id, {}, {}, user)


def env_list(project_id, file_path, ref, user):
    file_id = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    env_list = Env.list(file_id)
    return env_list
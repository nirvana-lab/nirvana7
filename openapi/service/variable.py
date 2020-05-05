# -*- coding: utf-8 -*-
from openapi.db.models.gvariable import GlobalVariable
from openapi.db.models.variable import Variable
from openapi.db.models.env import Env
from openapi.db.models.gitfile import GitFile
from logbook import Logger

log = Logger('service/gvariable')

def update_global_variable(project_id, body, user):
    medadata = body.get('metadata')
    data = {}
    for k, v in medadata.items():
        if v.get('selected'):
            data[k] = v.get('value')
    GlobalVariable.update_global_variable(project_id=project_id, metadata=medadata, data=data, user=user)

def get_global_variable_by_id(project_id):
    data = GlobalVariable.get_global_variable(project_id)
    return data


def update_project_variable(project_id, file_path, ref, body, user):
    file_id = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    env_list = Env.list(file_id)
    env_list = list_handle(env_list)
    for env_data in body:
        env_id = int(env_data.get('env_id'))
        if env_id in env_list:
            medadata = env_data.get('metadata')
            data = {}
            for k, v in medadata.items():
                if v.get('selected'):
                    data[k] = v.get('value')
            Variable.update_variable(env_id, medadata, data, user)
            env_list.remove(env_id)
    for env_id in env_list:
        Variable.delete_variable_by_env_id(env_id, user)

def get_project_variable_list(project_id, file_path, ref):
    file_id = GitFile.get_obj_pk_by_project_id_and_file_path(project_id, file_path)
    env_list = Env.list(file_id)
    env_list = list_handle(env_list)
    data = []
    for env_id in env_list:
        metadata = Variable.get_variable_by_env_id(env_id)
        tmp_dict = {}
        tmp_dict['env_id'] = env_id
        tmp_dict['metadata'] = metadata
        data.append(tmp_dict)
    return data

def list_handle(env_list):
    data = []
    for env in env_list:
        env_id = env.get('id')
        data.append(env_id)
    return data
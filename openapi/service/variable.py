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
    data = GlobalVariable.get_global_metadata_variable(project_id)
    return data


def update_project_variable(env_id, body, user):
    medadata = body.get('metadata')
    data = {}
    for k, v in medadata.items():
        if v.get('selected'):
            data[k] = v.get('value')
    Variable.update_variable(env_id, medadata, data, user)

def get_project_variable_by_env(env_id):
    metadata = Variable.get__metadata_variable_by_env_id(env_id)
    return {
        'env_id': env_id,
        'metadata': metadata,
    }
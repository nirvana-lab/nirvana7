# -*- coding: utf-8 -*-
from openapi.db.models.script import Script
from logbook import Logger
from openapi.utils import gitlab_handle,case_handle
from openapi.utils.exception_handle import IsExist, IsNotExist, DefalutError
from openapi.config.config import NirvanaConfig
from openapi.utils.common import is_exist_python_path
import os

log = Logger('service/script')

def create_script(project_id, body, user):
    script = body.get('script')
    description = body.get('description')
    content = body.get('content')
    script_file = body.get('script_file')

    Script.create(project_id=project_id, script=script, script_file=script_file,description=description, content=content, user=user)

    nirvana_config = NirvanaConfig()
    script_save_path = nirvana_config.script_save_path(project_id)
    is_exist_python_path(script_save_path)
    script_file_path = os.path.join(script_save_path, script_file)
    with open(script_file_path, 'w') as name:
        name.write(content)

def get_script_list_by_project_id(project_id):
    return Script.list(project_id)
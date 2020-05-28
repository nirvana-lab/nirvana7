# -*- coding: utf-8 -*-
from openapi.db.models.script import Script
from logbook import Logger
from openapi.config.config import NirvanaConfig
from openapi.utils.common import is_exist_python_path, delete_file
import os
import types

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


def update_script_content_by_script_id(script_id, body, user):
    script = body.get('script')
    description = body.get('description')
    content = body.get('content')
    script_file, project_id = Script.update(script_id, script, description,content, user)

    nirvana_config = NirvanaConfig()
    script_save_path = nirvana_config.script_save_path(project_id)
    is_exist_python_path(script_save_path)
    script_file_path = os.path.join(script_save_path, script_file)
    with open(script_file_path, 'w') as name:
        name.write(content)

def delete_script_by_script_id(script_id, user):
    script_file, project_id = Script.delete(script_id, user)
    nirvana_config = NirvanaConfig()
    script_delete_path = nirvana_config.script_save_path(project_id)
    script_file_path = os.path.join(script_delete_path, script_file)
    delete_file(script_file_path, script_file)

def get_content_by_script_id(script_id):
    return Script.get_content_by_script_id(script_id)

def get_function_list_and_args(project_id):
    func_list = Script.list(project_id)
    data = []
    if func_list:
        for func in func_list:
            import_module = __import__(f"openapi.script.{project_id}.{func.get('script_file')[:-3]}", fromlist=True)

            for name, item in vars(import_module).items():
                if isinstance(item, types.FunctionType):
                    tmp_dict = {}
                    tmp_dict['name'] = f'{name}.py'
                    tmp_dict['args'] = item.__code__.co_varnames
                    data.append(tmp_dict)
    return data
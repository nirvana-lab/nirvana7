from logbook import Logger
from openapi.config.config import NirvanaConfig
from openapi.utils.exception_handle import DefalutError
from urllib.parse import quote

log = Logger('utils/gitlab_handle')

def get_file_content_from_gitlab(project_id, file_path, ref, token):
    gitlab = NirvanaConfig().gitlab_config()

    url = f'https://{gitlab.get("gitlab_url")}/api/v4/projects/{project_id}/repository/files/{quote(file_path, safe="")}?ref={ref}'
    headers = {
        'Private-Token': token
    }

    try:
        import requests
        resp = requests.get(url=url, headers=headers)

        if resp.status_code == 200:
            content = resp.json()
            file_name = content.get('file_name')
            file_path = content.get('file_path')
            encoding = content.get('encoding')
            ref = content.get('ref')
            blob_id = content.get('blob_id')
            commit_id = content.get('commit_id')
            last_commit_id = content.get('last_commit_id')

            if encoding == 'base64':
                import base64
                re_content = base64.b64decode(content.get('content'))
            else:
                re_content = content.get('content')
            return file_name, file_path, ref, blob_id, commit_id, last_commit_id, re_content
        else:
            raise DefalutError(title='获取gitlab报错', detail=f'{resp.text}')
    except DefalutError as e:
        raise DefalutError(title=f'{e.title}', detail=f'{e.detail}')
    except Exception as e:
        raise DefalutError(title='获取gitlab文件内容错误', detail=f'{e}')

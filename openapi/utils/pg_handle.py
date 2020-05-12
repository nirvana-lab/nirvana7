# -*- coding: utf-8 -*-
import psycopg2
from openapi.config.config import NirvanaConfig

class Postgres(object):

    def __init__(self):
        nirvana_config = NirvanaConfig()
        pg_provider, pg_host, pg_user, pg_password, pg_database = nirvana_config.postgres_config()

        self.conn = psycopg2.connect(database=pg_database, user=pg_user, password=pg_password, host=pg_host, port='5432')
        self.cur = self.conn.cursor()

    def get_case_content_by_id(self, case_id):
        sql = f'SELECT * FROM "public"."testcase" WHERE id={case_id}'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res[0]

    def get_repo_id_by_env_id(self, env_id):
        sql = f'SELECT gitfile FROM "public"."env" WHERE id={env_id}'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        file_id = res[0][0]

        sql = f'SELECT project_id FROM "public"."gitfile" WHERE id={file_id}'
        self.cur.execute(sql)
        res2 = self.cur.fetchall()
        return res2[0][0]

    def get_global_variable_by_repo_id(self, repo_id):
        sql = f'SELECT data FROM "public"."global_variable" WHERE project_id=CAST({repo_id} as VARCHAR) AND delete_at is null'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res[0][0]

    def get_variable_by_env_id(self, env_id):
        sql = f'SELECT data FROM "public"."variable" WHERE env={env_id} AND delete_at is null'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res[0][0]
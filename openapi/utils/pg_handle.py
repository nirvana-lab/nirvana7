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
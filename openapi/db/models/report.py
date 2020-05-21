# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from openapi.db.models.testsuit import TestSuit
from logbook import Logger

log = Logger('db/report')

class Report(db.Entity):

    _table_ = 'report'

    id = PrimaryKey(int, auto=True)
    report_path = Required(str)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str)
    info = Optional(Json)
    testsuit = Required(TestSuit)

    @classmethod
    @db_session
    def create(cls, report_path, suit_id, user):
        Report(report_path=report_path, testsuit=suit_id, user=user)

    @classmethod
    @db_session
    def get_last_report_by_suit_id(cls, suit_id):
        objs = select(n for n in Report if n.testsuit.id == suit_id).order_by(desc(Report.id))
        if objs:
            return objs.first().report_path
        return ''
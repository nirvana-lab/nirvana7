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
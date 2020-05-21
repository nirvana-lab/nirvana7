# -*- coding: utf-8 -*-
from openapi.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get, Optional)
import datetime
from openapi.utils.exception_handle import IsExist, IsNotExist
from logbook import Logger

log = Logger('db/testcase')

class TestSuit(db.Entity):

    _table_ = 'testsuit'

    id = PrimaryKey(int, auto=True)
    suit = Required(str)
    project_id =Required(str)
    description = Optional(str)
    suit_content = Required(Json)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    delete_at = Optional(datetime.datetime, nullable=True)
    user = Required(str)
    info = Optional(Json)
    report = Set('Report')

    @classmethod
    @db_session
    def create(cls, suit, description, project_id, suit_content, user):
        obj = get(n for n in TestSuit if n.suit == suit and n.delete_at == None)
        if obj:
            raise IsExist(title='测试套件已经存在', detail=f'测试套件{suit}已经存在')
        TestSuit(suit=suit, description=description, project_id=project_id, suit_content=suit_content, user=user)

    @classmethod
    @db_session
    def list(cls, project_id):
        suit_list = []
        objs = select(n for n in TestSuit if n.project_id == project_id and n.delete_at == None)
        for obj in objs:
            tmp_dict = {
                'id': obj.id,
                'suit': obj.suit,
                'description': obj.description
            }
            suit_list.append(tmp_dict)
        return suit_list

    @classmethod
    @db_session
    def get_content_by_suit_id(cls, suit_id):
        obj = get(n for n in TestSuit if n.id == suit_id and n.delete_at == None)
        if obj:
            return {
                'id': obj.id,
                'project_id': obj.project_id,
                'suit': obj.suit,
                'description': obj.description,
                'suit_content': obj.suit_content
            }
        else:
            raise IsNotExist(title='测试套件不存在', detail=f'id为{suit_id}的测试套件不存在')

    @classmethod
    @db_session
    def update_content_by_suit_id(cls, suit_id, suit, description, suit_content, user):
        obj = get(n for n in TestSuit if n.id == suit_id and n.delete_at == None)
        if obj:
            obj.suit = suit
            obj.description = description
            obj.suit_content = suit_content
            obj.user = user
            obj.update_at = datetime.datetime.utcnow()
        else:
            raise IsNotExist(title='测试套件不存在', detail=f'id为{suit_id}的测试套件不存在')
# -*- coding: utf-8 -*-
from openapi.db.models.testsuit import TestSuit
from openapi.db.models.report import Report
from logbook import Logger
from openapi.utils import case_handle
from httprunner.api import HttpRunner
from httprunner import report
from openapi.db.models.report import Report
import os

log = Logger('service/testsuit')

def create_testsuit(project_id, body, user):
    suit = body.get('suit')
    description = body.get('description')
    suit_content = body.get('suit_content')
    TestSuit.create(suit=suit, description=description, project_id=project_id,
                    suit_content=suit_content, user=user)

def get_testsuit_list_by_project_id(project_id):
    suit_list = TestSuit.list(project_id)
    for suit in suit_list:
        report_path = Report.get_last_report_by_suit_id(int(suit.get('id')))
        suit['report'] = report_path.split('/')[-1]
    return suit_list

def run_testsuit_by_suit_id(suit_id, user):
    data = TestSuit.get_content_by_suit_id(suit_id)
    suit_content = data.get('suit_content')
    project_id = data.get('project_id')
    case_id_env_id_list = []
    for content in suit_content:
        case_id_env_id_list.append({'exec_id': content.get('exec_id'), 'env_id': content.get('env_id')})
    test_suit_parse = case_handle.TestSuitParse(case_id_env_id_list, project_id)
    suite = test_suit_parse.get_httprunner_test_suite_json()

    runner = HttpRunner()
    result = runner.run(suite)

    report_save_path = os.path.join(os.getcwd(),'openapi/reports')
    report_path = report.gen_html_report(result, report_dir=report_save_path)
    Report.create(report_path, suit_id, user)
    return report_path.split('/')[-1]

def update_testsuit_content_by_suit_id(suit_id, body, user):
    suit = body.get('suit')
    description = body.get('description')
    suit_content = body.get('suit_content')
    TestSuit.update_content_by_suit_id(suit_id=suit_id, suit=suit, description=description, suit_content=suit_content, user=user)

def get_testsuit_content_by_suit_id(suit_id):
    return TestSuit.get_content_by_suit_id(suit_id)
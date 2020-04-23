import uuid
from termcc.helper.logger import Config, inject_basic, inject_color
from flask import request

def inject_flask(record):
    inject_basic(record)
    try:
        record.extra['trace_id'] = request.headers.get('trace-id') or uuid.uuid1().hex
        record.extra['ip'] = request.remote_addr or None
        record.extra['method'] = request.method or None
        record.extra['path'] = request.path or None
    except:
        record.extra['ip'] = None
        record.extra['method'] = None
        record.extra['trace_id'] = None
        record.extra['path'] = None


def inject_flask_color(record):
    inject_flask(record)
    inject_color(record)


def setup_logger():
    lc = Config(inject=inject_flask_color)
    lc.setup_format(
        lc.basic_format(color=True),
        lc.time_format(),
        lc.process_format(),
        lc.trace_format(),
        logger_names=['stream-out'])
    lc.push(logger_names=['stream-out'])
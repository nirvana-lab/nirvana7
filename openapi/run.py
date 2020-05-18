#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from flask_cors import CORS
from logbook import Logger

from openapi.utils.log_handle import setup_logger
from openapi.utils.problem_handle import problem_exception_handler, exception_handler
from openapi.db.db import db
from flask import g
from openapi.config.config import check_config_path

from openapi.db.models.gitfile import GitFile # noqa: F401
from openapi.db.models.testcase import TestCase # noqa: F401
from openapi.db.models.env import Env # noqa: F401
from openapi.db.models.variable import Variable # noqa: F401
from openapi.db.models.gvariable import GlobalVariable # noqa: F401
from openapi.db.models.script import Script # noqa: F401

if __name__ == '__main__':
    setup_logger()
    log = Logger('nirvana')
    log.info('database mapping generating')
    db.generate_mapping(create_tables=True)
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='specs/')
    CORS(app.app)
    app.add_api('openapi.yaml', arguments={'title': 'api'})
    log.info('api.yaml loaded!')
    app.add_error_handler(connexion.ProblemException, problem_exception_handler)
    app.add_error_handler(Exception, exception_handler)
    log.info('error handler added')

    @app.app.before_request
    def before():
        g.username = "nirvana7"

    check_config_path()
    app.run(host='0.0.0.0', debug=True)
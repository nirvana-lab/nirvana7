from logbook import Logger
from termcc.helper.trace import trace_exception
from connexion import (ProblemException, problem, FlaskApi)

log = Logger('nirvana')

def exception_handler(exception):
    log.critical("{}:{}:{}-{}".format(getattr(exception, 'name', 'uncaught'),
                                   getattr(exception, 'code', 500),
                                   getattr(exception, 'description', 'uncaught'),
                                   getattr(exception, 'type', 'about:blank')
                                   ))

    trace_exception(exception, log)

    response = problem(title=getattr(exception, 'name', 'uncaught'),
                       status=getattr(exception, 'code', 500),
                       detail=getattr(exception, 'description', 'uncaught'),
                       type=getattr(exception, 'type', 'about:blank')
                       )
    return FlaskApi.get_response(response)


def problem_exception_handler(exception):
    log.error("{}:{}:{}-{}".format(exception.title, exception.status, exception.detail, exception.type))
    trace_exception(exception, log)
    response = exception.to_problem()
    return FlaskApi.get_response(response)

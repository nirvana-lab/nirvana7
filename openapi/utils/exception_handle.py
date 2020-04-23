from connexion import ProblemException

class NotFound(ProblemException):
    def __init__(self, title="NOT_FOUND", detail="", status=400, type="NotFound", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class IsExist(ProblemException):
    def __init__(self, title="IsExist", detail="", status=400, type="IsExist", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class IsNotExist(ProblemException):
    def __init__(self, title="IsNotExist", detail="", status=400, type="IsNotExist", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class SystemError(ProblemException):
    def __init__(self, title="系统异常", detail="", status=400, type="SystemError", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class FormatTypeError(ProblemException):
    def __init__(self, title="格式化异常", detail="", status=400, type="FormatTypeError", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class DefalutError(ProblemException):
    def __init__(self, title="未知异常", detail="", status=400, type="DefalutError", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class FileError(ProblemException):
    def __init__(self, title="文件异常", detail="", status=400, type="FileError", **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class TestCaseError(ProblemException):
    def __init__(self, title='执行测试用例异常', detail='', status=400, type='TestCaseError', **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)

class GitExecError(ProblemException):
    def __init__(self, title='执行Git命令异常', detail='', status=444, type='GitExecError', **kwargs):
        super().__init__(title=title, detail=detail, status=status, type=type, **kwargs)
class ParamsMissing(Exception):
    def __init__(self, params):
        err = "Parameter: '%s' is missing!" % params
        Exception.__init__(self, err)


class ParamsError(Exception):
    pass


class FileNotExist(Exception):
    def __init__(self, msg):
        err = "File: %s not exist!" % msg
        Exception.__init__(self, err)


class DirNotExist(Exception):
    def __init__(self, msg):
        err = "Dir: %s not exist!" % msg
        Exception.__init__(self, err)

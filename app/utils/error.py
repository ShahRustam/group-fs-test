# -*- coding: utf-8 -*-

from app.config import *


def newError(errorKey, errorMessage):
    errorsDict = collections.OrderedDict()
    errorsDict['errorKey'] = errorKey
    errorsDict['errorMessage'] = errorMessage
    return errorsDict


def sendError(errors):
    return jsonify({"status": 0, "errors": errors}), 406


class ErrorResponse:
    @staticmethod
    def makeCustomError(key, msg):
        return newError(key, msg)

    @staticmethod
    def makeNeedDataError(field):
        return newError(field.lower() + "_need_data", field + ' field not found.')

    @staticmethod
    def makeIsEmptyError(name, name2=None):
        if not name2:
            name2 = name
        return newError(name.lower() + "_is_empty", " | need to specify ")

    @staticmethod
    def makeNotFoundError(name):
        return newError(name.lower() + "_not_found", name + ' not found.')

    @staticmethod
    def makeInvalidFormatError(name, name2=None):
        if not name2:
            name2 = name
        return newError(name.lower() + "_invalid_format", " | invalid format.")
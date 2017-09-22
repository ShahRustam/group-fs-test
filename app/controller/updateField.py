# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *
from app.controller.login import loginRequired


class UpdateField(MethodView):
    @loginRequired
    def post(self, name, link):
        user = currentUser()
        errors = []
        try:
            value = request.form["value"].strip()
        except KeyError, error:
            errors.append(ErrorResponse.makeNeedDataError(error.args[0]))
            return sendError(errors)
        try:
            client[str(user.get("_id"))][name].find_one_and_update({"_id": ObjectId(link.split("__")[0])},
                                                                   {"$set": {str(link.split("__")[1]): value}})
            return jsonify({"status": 1, "data": []}), 200
        except:
            return jsonify({"status": 0, "data": []}), 403

    @loginRequired
    def delete(self, name, link):
        user = currentUser()
        try:
            client[str(user.get("_id"))][name].delete_one({"_id": ObjectId(link)})
            return jsonify({"status": 1, "data": []}), 200
        except:
            return jsonify({"status": 0, "data": []}), 403

# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *
from app.controller.login import loginRequired


class TableView(MethodView):
    @loginRequired
    def get(self, name):
        user = currentUser()
        data = []
        page = request.args.get(get_page_parameter(), type=int, default=1)
        names = client[str(user.get("_id"))].collection_names(include_system_collections=False)
        for row in client[str(user.get("_id"))][name].find().sort("0-id", 1).skip((page - 1) * 15).limit(15):
            data.append(collections.OrderedDict(sorted(row.items())))
        pagination = Pagination(page=page, total=client[str(user.get("_id"))][name].count(), per_page=15,
                                record_name='rows', bs_version=3)
        return render_template('tableView.html', title="Table View", pageName="tableView", loginIn=True, user=user,
                               name=name, pagination=pagination,
                               names=names,
                               data=data)

    def post(self, name):
        user = currentUser()
        keys = client[str(user.get("_id"))][name].find_one().keys()
        errors = []
        newDict = {}
        try:
            for key in keys:
                if key != "_id":
                    try:
                        newDict[key] = int(request.form[key].strip())
                    except:
                        try:
                            newDict[key] = float(request.form[key].strip())
                        except:
                            newDict[key] = request.form[key].strip()
        except KeyError, error:
            errors.append(ErrorResponse.makeNeedDataError(error.args[0]))
            return sendError(errors)
        element = client[str(user.get("_id"))][name].insert(newDict)
        return jsonify({"status": 1, "data": str(element)})

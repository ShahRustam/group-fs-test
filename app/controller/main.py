# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *
from app.controller.login import loginRequired

class Main(MethodView):
    @loginRequired
    def get(self):
        user = currentUser()
        data = []
        names = client[str(user.get("_id"))].collection_names(include_system_collections=False)
        # for name in names:
        #     oneDict = {"name":name}
        #     array = []
        #     for row in client[str(user.get("_id"))][name].find():
        #         array.append(row)
        #     oneDict['data'] = array
        #     data.append(oneDict)
        return render_template('main.html', title="Main", pageName="main", loginIn = True, user = user, names = names)

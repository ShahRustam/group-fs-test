# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *

class Logout(MethodView):
    def get(self):
        tokenKey = request.cookies.get('Token-Key')
        client['main']['tokens'].delete_many({"token": tokenKey})
        return redirect('/login')
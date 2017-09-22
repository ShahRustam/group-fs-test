#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from config import *

from app.controller.login import Login
from app.controller.signUp import SignUp
from app.controller.main import Main
from app.controller.logout import Logout
from app.controller.uploadSQL import UploadSQL
from app.controller.tableView import TableView
from app.controller.updateField import UpdateField

app = Flask(__name__)

app.secret_key = secret_key
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MINIFY_PAGE'] = True

HTMLMIN(app)

SignUpView = SignUp.as_view('SignUp')
app.add_url_rule('/signUp', view_func=SignUpView, methods=['GET', 'POST'])

LoginView = Login.as_view('Login')
app.add_url_rule('/login', view_func=LoginView, methods=['GET', 'POST'])

MainView = Main.as_view('Main')
app.add_url_rule('/', view_func=MainView, methods=['GET', 'POST'])

LogoutView = Logout.as_view('Logout')
app.add_url_rule('/logout', view_func=LogoutView, methods=['GET', 'POST'])

UploadSQLView = UploadSQL.as_view('UploadSQL')
app.add_url_rule('/uploadSQL', view_func=UploadSQLView, methods=['GET', 'POST'])

TableViewView = TableView.as_view('TableView')
app.add_url_rule('/view/<name>', view_func=TableViewView, methods=['GET', 'POST'])

UpdateFieldView = UpdateField.as_view('UpdateField')
app.add_url_rule('/view/<name>/<link>', view_func=UpdateFieldView, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':
    # try:
    #     client['main']['users'].delete_many({})
    #     client['main']['tokens'].delete_many({})
    # except:
    #     pass
    app.run(host="0.0.0.0", port=80, debug=True)

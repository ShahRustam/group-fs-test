# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *


class SignUp(MethodView):
    def get(self):
        return render_template('signUp.html', title="SignUp", pageName="login")

    def post(self):
        errors = []
        try:
            email = request.form["email"].strip()
            fullname = request.form["fullname"].strip()
            password = request.form["password"].strip()
            password2 = request.form["password2"].strip()
        except KeyError, error:
            errors.append(ErrorResponse.makeNeedDataError(error.args[0]))
            return sendError(errors)
        self.checkfield(email, fullname, password, password2, errors)
        if errors:
            return sendError(errors)
        db = client['main']
        usersCollection = db['users']
        oldUser = usersCollection.find_one({"email": email})
        if not oldUser:
            password = sha512(password + secret_key).hexdigest()
            user = {"email": email, "password": password, "fullname": fullname, "active": 1}
            id = usersCollection.insert(user)
            return jsonify({"status": 1, "data": []})
        else:
            return sendError(ErrorResponse.makeCustomError("email_already_exist", "User already exist."))
            # status, data = createUser(email,password,fullname)
            # if status==0:
            #     return data
            # else:
            #     return jsonify({"status": 1, "data": []})

    def checkfield(self, email, fullname, password, password2, errors):
        if email == "":
            errors.append(ErrorResponse.makeIsEmptyError("Email"))
        else:
            if not validate_email(email, check_mx=True):
                errors.append(ErrorResponse.makeInvalidFormatError("Email"))
        if fullname == "":
            errors.append(ErrorResponse.makeIsEmptyError("Fullname", "fullname"))
        if password == "":
            errors.append(ErrorResponse.makeIsEmptyError("Password", "password"))
        if password2 == "":
            errors.append(ErrorResponse.makeIsEmptyError("Password2", "password"))
        if password != password2:
            errors.append(
                ErrorResponse.makeCustomError("password_error", " | do not match"))
            errors.append(
                ErrorResponse.makeCustomError("password2_error", " | do not match"))
        pass

# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *

class Login(MethodView):
    def get(self):
        return render_template('login.html', title="Login", pageName="login")

    def post(self):
        errors = []
        try:
            email = request.form["email"].strip()
            password = request.form["password"].strip()
        except KeyError, error:
            errors.append(ErrorResponse.makeNeedDataError(error.args[0]))
            return sendError(errors)
        self.checkfield(email, password, errors)
        if errors:
            sendError(errors)
        db = client['main']
        usersCollection = db['users']
        user = usersCollection.find_one({"email": email})
        if not user:
            errors.append(
                ErrorResponse.makeCustomError("email_user_not_found", " | user is not found"))
        else:
            if user.get("password") != sha512(password + secret_key).hexdigest():
                errors.append(
                    ErrorResponse.makeCustomError("password_incorrect", " | invalid password"))
            else:
                token, expired = Token.make(user.get('_id'))
                return jsonify({'status': 1, 'token': token, 'expired': expired}), 200
        if errors:
            return sendError(errors)

    def checkfield(self, email, password, errors):
        if email == "":
            errors.append(ErrorResponse.makeIsEmptyError("Email"))
        else:
            if not validate_email(email):
                errors.append(ErrorResponse.makeInvalidFormatError("Email"))
        if password == "":
            errors.append(ErrorResponse.makeIsEmptyError("Password", "пароль"))
        pass

def loginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        requestToken = request.cookies.get('Token-Key')
        db = client['main']
        tokensCollection = db['tokens']
        usersCollection = db['users']
        token = tokensCollection.find_one({"token":requestToken})
        if token:
            user = usersCollection.find_one({"_id": token.get("userId")})
            if user.get("active") == 1:
                if token.get('expired') > time():
                    return f(*args, **kwargs)
        resp = make_response(redirect('/login'))
        resp.set_cookie('Token-Key', expires=0)
        resp.set_cookie('Token-Expired', expires=0)
        return resp
    return wrap

# -*- coding: utf-8 -*-
from app.config import *

def genCode(length):
    firstCode = uuid4().get_hex()
    secondCode = sha512(firstCode).hexdigest()
    return secondCode[0:length]

def currentUser():
    requestToken = request.cookies.get('Token-Key')
    db = client['main']
    tokensCollection = db['tokens']
    usersCollection = db['users']
    token = tokensCollection.find_one({"token": requestToken})
    if token:
        user = usersCollection.find_one({"_id": token.get("userId")})
        if user:
            return user
    return False


class Token:
    TOKEN_EXPIRED_INTERVAL_MS = 86400

    @classmethod
    def make(cls, userId):
        client['main']['tokens'].delete_many({"userId": userId})
        token = Token.makeNew(userId)
        return token

    @classmethod
    def makeNew(cls, userId):
        tokenKey = genCode(64)
        tokenExpired = int(time() + Token.TOKEN_EXPIRED_INTERVAL_MS)
        client['main']['tokens'].insert({"token": tokenKey, "expired": tokenExpired, "userId": userId})
        return tokenKey, tokenExpired


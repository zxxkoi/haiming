import uuid
from functools import wraps

from flask import session, request, abort

from models.user import User

import redis
import json


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


csrf_tokens = redis.StrictRedis()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        # if token in csrf_tokens and csrf_tokens[token] == u.id:
        #     csrf_tokens.pop(token)
        #     return f(*args, **kwargs)
        if csrf_tokens.exists(token):
            v = csrf_tokens.get(token)
            i = json.loads(v)
            if i == u.id:
                # print('before ceshi', csrf_tokens.exists(token))
                csrf_tokens.delete(token)
                # print('ceshi', csrf_tokens.exists(token))
                return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    u.id = json.dumps(u.id)
    csrf_tokens.set(token, u.id)
    return token

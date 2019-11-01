import json
from functools import wraps

from flask import request, abort

with open("config.json", "r") as f:  # TODO: this ain't ideal
    CONFIG = json.load(f)


def edit_auth_required(func):
    @wraps(func)
    def decorated_func(*args, **kws):
        if not CONFIG.get("edit_auth_key"):
            return func(*args, **kws)
        if 'Authorization' not in request.headers:
            abort(401)
        if request.headers['Authorization'] != CONFIG["edit_auth_key"]:
            abort(401)
        return func(*args, **kws)
    return decorated_func

from functools import wraps
from flask import session,redirect,url_for

#限制登录装饰器
def login_reqeired(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get("user_id"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("login"))

    return wrapper
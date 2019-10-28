from flask import session
def isLogin():
    if session.get('userName')!=None:
        return True
    else:
        return False
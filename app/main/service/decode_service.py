from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def encode_url(user_name,folder,path):
    url = f"{folder}/{path}"
    serialize = Serializer(current_app.config["SECRET_KEY"], 60*30) # 60 secs by 30 mins
    token = serialize.dumps({'username': user_name , "url": url }).decode('utf-8') # encode
    return token


def decode_url(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        user_id = s.loads(token)
        if not user_id:
            raise PermissionError("Token Expired ! ")
        url = s.loads(token)['url']
        return url     
    except:
        raise PermissionError("Token Expired ! ")
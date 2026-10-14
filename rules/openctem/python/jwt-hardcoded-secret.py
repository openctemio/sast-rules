import jwt, os
# ruleid: openctem.python.crypto.jwt-hardcoded-secret
cookie = jwt.encode({"user": "a"}, 'csrf_vulneribility', algorithm='HS256')
# ok: openctem.python.crypto.jwt-hardcoded-secret
token = jwt.encode({"user": "a"}, os.environ["JWT_KEY"], algorithm='HS256')

import jwt
from datetime import datetime, timezone
from config import Config

# 토큰 생성. 인코드 파라미터- > (페이로드, 시크릿키, 해쉬 알고리즘)
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])

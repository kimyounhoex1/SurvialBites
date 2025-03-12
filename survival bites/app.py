from flask import Flask, render_template, request, jsonify, redirect, make_response
from pymongo import MongoClient
from config import Config
import bcrypt
from functools import wraps
import jwt
import datetime
from datetime import timezone

app = Flask(__name__)
app.config.from_object(Config)




######################################################### 
# !!mongodb user 관리 구현!!제바알아ㅏ아라랑라   !!!!!!전체 완료!!!!우와
#########################################################

# config.py에서 관리
client = MongoClient('localhost', 27017)
db = client.jungle

# 아이디 값으로 유저 찾는 함수. 많이 사용될 듯...
def find_user_by_id(user_id):
    return db.members.find_one({'id': user_id})

# 유저 생성하는 함수 - 와우 성공!!!!!!
def create_user(user_id, password, name):

    # 해쉬함수 사용해서 비밀번호 암호화
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 유저 생성 - 됬습ㄴㅇ니다.!!!!
    user = {'id': user_id, 'pw': hashed_pw, 'name': name}
    db.members.insert_one(user)
    return user


#########################################################
# !!회원가입 로그인 처리 인증 엔드포인트 구현!!
# !!auth!!
#########################################################

# signup으로 post요청 보낼때 ---완료!!!!
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('pw')
    name = data.get('name')
    print(find_user_by_id(user_id))
    # 아이디 중복 처리 하기
    if find_user_by_id(user_id):
        return jsonify({'error': '이미 존재하는 아이디입니다.'}) #여기서 함수 종료됨
    create_user(user_id, password, name)
    return jsonify({'message': '회원가입 성공'})


# ---로그인 구현 완료!!!!--
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('pw')

    # 아이디 일치 체크-완
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({'error': '존재하지 않는 아이디입니다.'})

    # 비밀번호 일치 체크-완
    if not bcrypt.checkpw(password.encode('utf-8'), user['pw']):
        return jsonify({'error': '비밀번호가 일치하지 않습니다.'})

    # 로그인 인증 완료 후 토큰 발행 - 완
    token = generate_token(user_id)
    
    
    #  여기서 페이지 로딩을 처리하면 되나????
    response = make_response(redirect('/postingpage'))
    response.set_cookie("jwtToken", token, httponly=True, secure=True, samesite="Strict")
    
    return response


#########################################################
# !!접근방지 기능 구현 (JWT토큰이 없다면 접근이 불가능한 엔드포인트)!!
# !!protecte!!
#########################################################
# 나중에 하자!!!!
# 접근방지 구현
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwtToken")
        if not token:
            # 여기서 문제 발생
            return redirect('/loginpage')
        # 유효성검사를 해봐요!!!!!
        try:
            # 페이로드에서 데이터 추출하기!!!ㅠㅠ
            payload = verify_token(token)
            # 페이로드에서 유저 아이디 추출
            user_id = payload.get("user_id")
            # db에 페이로드에서 추출한 유저 아이디 찾기
            current_user = find_user_by_id(user_id)
            #만약 없다면...
            if current_user is None:
                return redirect("/loginpage")
        #그 외 모든 예외상황을 포착
        except Exception as e:
            return redirect("/loginpage")
        return f(current_user["id"], *args, **kwargs)
    return decorated

# @app.route('/profile', methods=['GET'])
# @token_required
# def profile(current_user):
#     return jsonify({'message': '인증된 사용자만 접근 가능합니다.', 'user': current_user['name']}), 200


#########################################################
# # !!!!!!!<<JWT>>>ㅌ토큰ㅋㅋㄴㅋㄴㄴㄴ생서엉어어어어어하자!!!!!!!! 
#########################################################토
#토큰생성 ---완!!
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


# 토큰 해체??????
def verify_token(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])


# 라우터

@app.route('/')
def homepage():
    return render_template('home.html', show_profile=False, have_bg_img=True)

@app.route('/loginpage')
def loginpage():
    return render_template('login.html', show_profile=False, have_bg_img=True)

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html', show_profile=True, have_bg_img=False)

@app.route('/postingpage')
@token_required
def postingpage(user_id):
    return render_template('posting.html', show_profile=True, have_bg_img=False, id=user_id)



if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)
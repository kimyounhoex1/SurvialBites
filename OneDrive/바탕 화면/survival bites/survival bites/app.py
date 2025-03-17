from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for
from pymongo import MongoClient
from config import Config
import bcrypt
from functools import wraps
import jwt
import datetime
from datetime import timezone
import uuid
import os
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

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
    password_confirm = data.get('pw_cf')
    name = data.get('name')qwe
    # 아이디 자리 확인
    if not (6 <= len(user_id) <= 20):
        print("len")
        return jsonify({'error': '아이디는 6자 이상 20자 이하로 입력해주세요.'})
    # 아이디 존재확인
    if find_user_by_id(user_id):
        return jsonify({'error': '이미 존재하는 아이디입니다.'}) #여기서 함수 종료됨
    # 비밀번호 일치 확인ㅇ
    if password != password_confirm:
        return jsonify({'error': '입력한 비밀번호가 일치하지 않습니다.'}) #여기서도 함수 종료
    create_user(user_id, password, name)
    return jsonify({"result": "success", 'message': '회원가입 성공'})

# ---로그인 구현 완료!!!!--
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('pw')

    # 아이디 일치 체크-완
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({"result": "failure", 'message': '존재하지 않는 아이디입니다.'})

    # 비밀번호 일치 체크-완
    if not bcrypt.checkpw(password.encode('utf-8'), user['pw']):
        return jsonify({"result": "failure", 'message': '비밀번호가 일치하지 않습니다.'})

    # 로그인 인증 완료 후 토큰 발행 - 완
    token = generate_token(user_id)
    
    
    #  여기서 페이지 로딩을 처리하면 되나????
    response = make_response(redirect(url_for('postingpage')))
    response.set_cookie("jwtToken", token)
    
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
        response = make_response(redirect('/loginpage'))
        if not token:
            # 여기서 문제 발생
            print("durlsl?")
            return response
        # 유효성검사를 해봐요!!!!!
        try:
            # 페이로드에서 데이터 추출하기!!!ㅠㅠ
            payload = verify_token(token)
            # 페이로드에서 유저 아이디 추출
            user_id = payload.get("user_id")
            # db에 페이로드에서 추출한 유저 아이디 찾기
            current_user = db.members.find_one({"id": user_id})
            #만약 없다면...
            if current_user is None:
                return redirect("/loginpage")
            
        #그 외 모든 예외상황을 포착
        except Exception as e:
            return redirect("/loginpage")
        
        return f(current_user["id"], *args, **kwargs)
    return decorated



#########################################################
# # !!!!!!!<<JWT>>>ㅌ토큰ㅋㅋㄴㅋㄴㄴㄴ생서엉어어어어어하자!!!!!!!! 
#########################################################토
#토큰생성 ---완!!
def generate_token(user_id):
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1),
        }
        # PyJWT 2.0 이상 버전에서는 jwt.encode()가 문자열을 반환
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token
    except Exception as e:
        print(f"Token generation error: {str(e)}")
        raise e


# 토큰 해체??????
def verify_token(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])




#########################################################
#김지을 코드
#########################################################토





# 참여목록 가져오기
@app.route('/getList')
def getList():
    post_id = request.form['post_id']
    resultList= []
    post = db.posts.findOne({'_id': ObjectId(post_id)})
    participants = post["member_list"]

    for participant in participants:
        member_id = participant['members_id']
        member = db.memebers.find_one({'_id': ObjectId(member_id)})
    
    resultList.append(member['name'])

    return jsonify({'result': 'success', 'participants': resultList})

# 포스트 업로드
@app.route('/uploadPost', methods=['POST'])
def uploadPost():
    # 토큰 분해하기
    token_value = request.cookies.get("jwtToken")
    id = verify_token(token_value)["user_id"]
    
    if 'file' in request.files:
        file_receive = request.files['file']
        path = "static/images/"
        
        os.makedirs(path, exist_ok=True)

        filename = secure_filename(file_receive.filename)
        extension = filename.split('.')[-1].lower()
        unique_filename = str(uuid.uuid4()) + '.' + extension

        file_receive.save(os.path.join(path, unique_filename))
        image_url = f"/static/images/{unique_filename}"
    else:
        image_url = "/static/images/main.jpg"

    # form.get() 사용하여 안전하게 데이터 가져오기
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    foodtype = request.form.get('foodtype', '')
    meetingtype = request.form.get('meetingtype', '')
    appointment_time = request.form.get('appointment_time', '')
    max_of_participants = request.form.get('max_of_participants', '1')
    current_participants = request.form.get('current_participants', '0')
    
    # db 맞추기
    db.posts.insert_one({
        'user_id': id,
        'title': title,
        'image': image_url,
        'content': content,
        'food_type': foodtype,
        'meeting_type': meetingtype,
        'appointment_time': appointment_time,
        'max_of_participants': max_of_participants,
        'current_participants': current_participants
    })

    return jsonify({'result': 'success'})

# 메인 페이지 포스트들 보여주는 거

@app.route('/showPosts')
def showPosts():
    posts = db.posts.find({})
    
    post_list = []

    for post in posts:
        post['_id'] = str(post['_id'])
        post_list.append(post)

    return render_template('postList.html', post_list=post_list)

#각 포스트 상세 페이지








# 모임 참여하기 로직
## 참여자 중복 확인 -> 로그인 로직에 비슷한 기능 있음.
########
@app.route('/join', methods=['POST'])
def join():
    # 포스트 아이디 넘겨 받기
    post_id = request.form['post_id']
    user_id = request.form["user_id"]
    # 포스트 아이디로 찾기
    result = db.posts.find_one({'_id': ObjectId(post_id)})
        
    current_participants = int(result.get('current_participants', 0))
    max_of_participants = int(result.get('max_of_participants', 0))
    
    # 사용자가 이미 이 게시물에 참여했는지 확인
    find_user = db.posts.find_one({'_id': ObjectId(post_id), 'member_list': user_id})
    
    # 유저가 이미 참여 했는지 확인
    if find_user:
        return jsonify({"result": "failure", "message": "이미 참여한 유저입니다."})
    # 여기가 정상적인 동작이지요. 이 유저는 아직 참여하지 않았어여ㅛ. 참여할 자격이 있답니다.
    else:
        # 하지만 참여 인원이 꽉 찼다면????
        if current_participants + 1 > max_of_participants:
            return jsonify({"result": "failure", "message": "참여자가 꽉 찼습니다."})
        # 와우!! 빈자리가 남아 있네요!!!
        else:
            # 그렇다면 명단에 넣어 줄게요.
            db.posts.update_one({'_id': ObjectId(post_id)}, {"$addToSet": {"member_list": user_id}})
            # 참여인원 수도 늘여요!!!!!!!!!
            current_participants += 1
            db.posts.update_one({'_id': ObjectId(post_id)}, {"$set": {"current_participants": current_participants}})
            return jsonify({'result': 'success'})

@app.route('/joinlist', methods=['POST'])
def joinlist():
    post_id = request.form['post_id']
    find_user_list = db.posts.find_one({ "_id": ObjectId(post_id)})
    user_list = find_user_list.get("member_list", [])
    return jsonify({"list" : user_list})


# 배달 커피챗 필터기능 - 이제 앎
@app.route('/filter', methods=['GET'])
@token_required
def filter(user_id):
    meetingtype = request.args.get('meetingtype')

    if meetingtype == '배달':
        posts = db.posts.find({"meeting_type": meetingtype})
    elif meetingtype == '커피챗':
        posts = db.posts.find({"meeting_type": meetingtype})
    else:
        posts = db.posts.find({})

    return render_template('main.html', posts=posts, show_profile=True, have_bg_img=False, id=user_id)









#########################
# 맵핑
########################
@app.route('/')
def homepage():
    return render_template('home.html', show_profile=False, have_bg_img=True)

@app.route('/loginpage')
def loginpage():
    if request.cookies.get('jwtToken') is not None:
        return make_response(redirect("/mainpage"))
    return render_template('login.html', show_profile=False, have_bg_img=True)

@app.route('/mainpage')
@token_required
def mainpage(user_id):
    posts = list(db.posts.find())
    return render_template('main.html', show_profile=True, have_bg_img=False, id=user_id, posts=posts)

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html', show_profile=False, have_bg_img=False)

@app.route('/postingpage')
@token_required
def postingpage(user_id):
    return render_template('posting.html', show_profile=True, have_bg_img=False, id=user_id)



# 포스트 이동 완료
@app.route('/content/<post_id>', methods=['GET'])
@token_required
def post(user_id, post_id):
    post = db.posts.find_one({'_id': ObjectId(post_id)})
    if post:
        return render_template('content.html',page_type="postpage", show_profile=True, have_bg_img=False, id=user_id, post=post)
    else:
        return "게시물을 찾을 수 없습니다.", 404


    

@app.route('/memberlist', methods=['GET'])
def memberlistPage():
    return

@app.route('/memberlist', methods=["POST"])
def memberlist():
    return


#마이페이지 기능
@app.route('/mypage', methods=['GET'])
@token_required
def getmypage(user_id):
    posts = list(db.posts.find({'user_id': user_id}))
    return render_template('main.html', show_profile=True, have_bg_img=False, id=user_id, posts=posts, page_type="mypage")

@app.route('/logout', methods=['POST'])
@token_required
def logout(user_id):
    response = make_response(redirect("/loginpage"))
    response.set_cookie("jwtToken", "", 0)
    # if request.cookies.get('jwtToken'):
    #     return jsonify({"result": "failure", "message": "로그아웃 실패"})
    return response

# 마이페이지
@app.route('/updatepost/<post_id>', methods=['GET'])
@token_required
def getupdatepage(user_id, post_id):
    post = db.posts.find_one({'_id': ObjectId(post_id)})
    return render_template('content.html', post=post, page_type="mypage", show_profile=True, have_bg_img=False, id=user_id)

# 수정기능은 맞지 않는다 판단 -> why? 이미 참여한 사람이 있는 상태에서 수정이 들어가면 약속을 어기는 거기 때문에
@app.route('/updatepost/<post_id>', methods=['POST'])
def postupdatpage(post_id):
    action = request.form['action']
    response = {"result": "failure"}

    # if action == 'edit':
    #     updated_data = request.form.get('updated_data')
    #     if updated_data:
    #         result = db.posts.update_one(
    #             {'_id': ObjectId(post_id)},
    #             {'$set': {'content': updated_data}}
    #         )
    #         if result.modified_count > 0:
    #             response = {"result": "success"}
    #         else:
    #             response = {"result": "failure"}
    #     else:
    #         response = {"result": "failure"}

    if action == 'remove':
        result = db.posts.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count > 0:
            response = {"result": "success"}
        else:
            response = {"result": "failure"}

    return jsonify(response)

@app.route('/myposting', methods=['GET'])
def myposting():
    return



if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)
   
   
   
   
#    day1 0230 퇴근 0830 출근
#    day2 0430 퇴근 0900 출근
#    day3 퇴근없음
#    살려주세요......................
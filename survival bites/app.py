from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # home.html 템플릿을 렌더링하여 반환합니다.
    return render_template('home.html', show_profile=False, have_bg_img=True)

@app.route('/login')
def login():
    return render_template('login.html', show_profile=False, have_bg_img=True)

@app.route('/signup')
def signup():
    return render_template('signup.html', show_profile=True, have_bg_img=False)

@app.route('/makeContents')
def makeContents():
    return render_template('makeContents.html', show_profile=True, have_bg_img=False)


if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)
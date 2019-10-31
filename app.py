from flask import Flask,render_template,url_for,request,redirect,session,g
from sqlalchemy import or_,and_,any_
import config
from models.User import User
from models.Question import Question
from exts import db
from decorators import login_required
app = Flask(__name__)
# 数据库链接的配置，此项必须，格式为（数据库+驱动://用户名:密码@数据库主机地址:端口/数据库名称）
app.config.from_object(config)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=14)
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    questions = Question.query.order_by(Question.creat_time.desc()).all()
    return render_template('index.html',questions = questions)

@app.route('/search/',methods=['GET','POST'])
def search():
    print('hello')
    key_word = request.form.get('key_word')
    print(key_word)
    questions = Question.query.filter(or_(Question.content.like('%'+key_word+'%'),Question.title.like('%'+key_word+'%'))).all()
    return render_template('index.html',questions = questions)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        request.method == 'POST'
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password==password).first()
        if user:
            print(user)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return u'账号或密码不正确'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已注册'
        else:
            if password1 != password2:
                return u'两次输入密码不一致'
            else:
                user = User(telephone=telephone,username = username,password=password2)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        author_id = session.get('user_id')
        author = User.query.filter(User.id==author_id).first()
        ques = Question(title = title,content = content,author_id = author_id,author = author)
        db.session.add(ques)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.context_processor
def userInfo():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        return {'user':user.username}
    else:
        return {}


# @app.route('/add_article',methods=['POST','GET'])
# def add_article():
#     context = {}
#     if g.user:
#         if request.method =='POST':
#             title = request.form.get('title')
#             body = request.form.get('body')
#             author = request.form.get('author')
#             if title == ''or body=='':
#                 context['msg'] = '标题或内容不能为空'
#                 return render_template('addArticle.html',context = context)
#             else:
#                 blog = Article(title = title,content = body)
#                 try:
#                     db.session.add(blog)
#                     db.session.commit()
#                 except:
#                     context['msg'] = '入库失败'
#                     return render_template('addArticle.html',context=context)
#                 return redirect(url_for('article'))
#
#         else:
#             return render_template('addArticle.html',context=context)
#     else:
#             return render_template('login.html')
#
# @app.route('/article/')
# def article():
#         if g.user:
#             result = Article.query.all()
#             return render_template('article.html',result = result)
#         else:
#             context = {}
#             context['value']='请先登录'
#             return render_template('login.html',context=context)
#
# @app.route('/comment/<id>',methods=['GET','POST'])
# def comment(id):
#     if g.user:
#         if request.method=='GET':
#             return render_template('comment.html')
#         else:
#             content = request.form.get('content')
#             userId = g.user.id
#             comment = ArticleComment(comment=content,user_id=userId,article_id=id)
#             print(comment)
#             db.session.add(comment)
#             db.session.commit()
#             return 'success'
#     else:
#         context = {}
#         context['value'] = '请先登录'
#         return render_template('login.html', context=context)
#
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     context = {}
#     err = False
#     if request.method == 'POST':
#         req_name = request.form.get('username')
#         req_pwd = request.form.get('password')
#         if req_name == '' or req_pwd == '':
#             err = True
#             context['msg']='账号或密码不能为空'
#             context['err']=err
#             print(context)
#             return render_template('login.html',**context)
#         else:
#             user = User.query.filter(User.loginName == req_name).first()
#             if user.loginName == req_name and user.password == req_pwd:
#                 session['userName'] = user.loginName
#                 session.permanent = True
#                 return redirect(url_for('article'))
#             else:
#                 err = True
#                 return render_template('login.html',err = err)
#     else:
#         return render_template('login.html')
#
# @app.before_request
# def is_login():
#     userName = session.get('userName')
#     user = User.query.filter(User.loginName==userName).first()
#     g.user = user
#     if g.user:
#         print("不为空")
#     else:
#         print("为空")
#
#
#
# @app.route('/logout/',methods=['GET','POST'])
# def logout():
#     if isLogin:
#         session.pop('userName')
#         return '登出成功！'
#     else:
#         context = {}
#         context['value'] = '请先登录'
#         return render_template('login.html', context=context)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5050)


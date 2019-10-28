from flask import Flask,render_template,url_for,request,redirect,session,g
import config
import os
from  models.article import Article
from etcs import db
from datetime import timedelta
from utils import isLogin
app = Flask(__name__)
# 数据库链接的配置，此项必须，格式为（数据库+驱动://用户名:密码@数据库主机地址:端口/数据库名称）
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=14)
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    #session操作
    session['userName'] = 'allen'
    session.permanent = True
    #增加
    # article1 = Article(article_name='天龙八部',author='金庸',price=None)
    # db.session.add(article1)
    # db.session.commit()
    #查询
    # result = Article.query.filter(Article.author == '金庸').all()
    # l = result #数组
    # print(l)
    # article1 = l[0] #字典
    # print(article1.article_name)
    #改(查、改、提)
    # result = Article.query.filter(Article.author == '金庸').all()
    # result[0].author = 'allen'
    # db.session.commit()
    #删除（查、删、提）
    # result = Article.query.filter(Article.price==None).all()
    # db.session.delete(result[1])#不能直接result传入
    # db.session.commit()
    # return redirect(url_for('login'))
    return redirect(url_for('article'))

@app.route('/add_article',methods=['POST','GET'])
def add_article():
    context = {}
    if request.method =='POST':
        title = request.form.get('title')
        body = request.form.get('body')
        author = request.form.get('author')
        if title == ''or body=='':
            context['msg'] = '标题或内容不能为空'
            return render_template('addArticle.html',context = context)
        else:
            blog = Article(title = title,content = body)
            try:
                db.session.add(blog)
                db.session.commit()
            except:
                context['msg'] = '入库失败'
                return render_template('addArticle.html',context=context)
            return redirect(url_for('article'))

    else:
        return render_template('addArticle.html',context=context)

@app.route('/article/')
def article():
        userName = session.get("userName")
        if userName == 'llj':
            result = Article.query.all()
            result = Article.query.all()
            print(session.get('userName'))
            # session.pop()
            # session.clear
            return render_template('article.html',result = result)
        else:
            context = {}
            context['value']='请先登录'
            return render_template('login.html',context=context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {}
    err = False
    if request.method == 'POST':
        req_name = request.form.get('username')
        req_pwd = request.form.get('password')
        if req_name == '' or req_pwd == '':
            err = True
            context['msg']='账号或密码不能为空'
            context['err']=err
            print(context)
            return render_template('login.html',**context)
        elif req_name == 'llj' and req_pwd=='123456':
            session['userName']=req_name
            return redirect(url_for('article'))
        else:
            err = True
            context['msg'] = '账号和密码不匹配'
            context['err'] = err
            return render_template('login.html',**context)
    else:
        return render_template('login.html')

@app.route('/logout/',methods=['GET','POST'])
def logout():
    if isLogin:
        session.pop('userName')
        return '登出成功！'
    else:
        context = {}
        context['value'] = '请先登录'
        return render_template('login.html', context=context)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5050)


from etcs import db
class Article(db.Model):
    __tablename__  = 'article'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    title = db.Column(db.String(70),nullable=True)
    content = db.Column(db.String(1000),nullable=True)
    author_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('Article'))

    def __init__(self,title,content):
        self.title = title
        self.content = content
    # def __repr__(self):
    #     return '<User %r>' % self.username

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    loginName = db.Column(db.String(20),nullable=True)
    password = db.Column(db.String(20),nullable=True)

    def __init__(self,name):
        self.name = name


class ArticleComment(db.Model):
    __tablename__ = 'article_comment'
    id = db.Column(db.INTEGER, primary_key=True,autoincrement=True)
    user_id = db.Column(db.INTEGER,db.ForeignKey('user.id'),nullable=True)
    article_id = db.Column(db.INTEGER,db.ForeignKey('article.id'),nullable=True)
    comment = db.Column(db.String(1000),nullable=True)


    def __init__(self,comment,body,author):
        self.comment = comment
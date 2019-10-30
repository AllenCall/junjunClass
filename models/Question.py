from exts import db
from datetime import datetime

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #datetime.now()获取的是服务器运行的时间
    # datetime.now获取的是模型创建的时间
    creat_time = db.Column(db.DATETIME,default=datetime.now)
    author_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = db.backref('question'))
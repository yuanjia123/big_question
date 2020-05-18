from exts import db

from datetime import datetime

#加密模块
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    # 邮箱
    email = db.Column(db.String(50), nullable=False)  # unique唯一

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)

    #时间 默认是此时此刻
    create_time = db.Column(db.DateTime,default=datetime.now)

    #外键
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    #relationship
    author = db.relationship("User",backref = db.backref("question"))


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    #评论的问题不能为空
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default = datetime.now)

    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    #这个评论是哪一个问题的回答
    question = db.relationship("Question",backref=db.backref("answersss",order_by = id.desc()))

    author = db.relationship("User",backref = db.backref("answers"))



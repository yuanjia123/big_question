from flask import Flask,request,render_template,redirect,url_for,session,g
from models import User,Question,Answer
from exts import db
import config
from decorators import login_reqeired
from decorators import login_reqeired
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
@login_reqeired
def index():
    context = {
        "questions":Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template("index.html",**context)

@app.route("/question/",methods=["GET","POST"])
@login_reqeired
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        title = request.form.get("title")
        content = request.form.get("content")

        question = Question(title = title,content = content)

        #谁发的问题
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))



@app.route("/detail/<question_id>")
def detail(question_id):
    #这条问题的模型
    question_model = Question.query.filter(Question.id == question_id).first()

    #下面的评论的数量  一个问题下面有很多评论， 问题表的主键id 是很多评论表的外键
    num = Answer.query.filter(Answer.question_id == question_id).count()
    return render_template("detail.html",question = question_model,nums = num)

@app.route("/add_answer/",methods=["GET","POST"])
def add_answer():
    # 拿到内容, 和这个问题的id
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    # 插入到数据库
    answer = Answer(content=content)

    # 这个评论属于哪一个作者
    answer.author = g.user

    # 评论是给那一个问题的  评论表的question
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question

    # 提交
    db.session.add(answer)
    db.session.commit()

    # 重新调用详细页面
    return redirect(url_for('detail', question_id=question_id))

@app.route("/search/")
def search():
    #get请求的 获取q
    q = request.args.get("q")

    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q)))
    print("进来了没")
    return render_template("index.html",questions = questions)




# @dp.route("/email_captcha/")
# def email_captcha():
#     email = request.args.get("email")
#     if not email:
#         return restful.params_error("请传递邮箱参数")
#     #产生一个随机的参数
#     source = list(string.ascii_letters)
#     source.extend(map(lambda x:str(x),range(0,10)))
#     #产生的这个随机数给captcha
#     captcha = "".join(random.sample(source,6))
#
#     message = Message("python论坛邮箱验证码",recipients=[email],body="您的邮箱验证码是%s"%captcha)
#     #可能发生错误、所以加上处理机制
#     try:
#         mail.send(message)
#     except:
#         return restful.server_error()
#     return restful.success()
#
#     # 运行以后网站栏输入  http: // 127.0.0.1: 8000 / cms / email_captcha /?email = 871105356 @ qq.com

@app.route("/setEmail/",methods=["GET","POST"])
@login_reqeired
def setEmail():
    if request.method == 'GET':
        return render_template("setEmail.html")
    else:
        pass



@app.route("/my_center/",methods=["GET","POST"])
@login_reqeired
def my_center():

    if request.method == 'GET':
        return render_template("my_center.html")
    else:
        print("g.user.username:{}, g.user.password:{}, g.user.telephone:{}, g.user.email:{}".format(g.user.username,g.user.password,g.user.telephone,g.user.email))
        telephone = request.form.get("telephone")
        password_old = request.form.get("password_old")
        if telephone == g.user.telephone and password_old == g.user.password:
            password_new1 = request.form.get("password_new1")
            password_new2 = request.form.get("password_new2")

            if password_new1 == password_new2:
                user = User.query.filter(User.id == g.user.id).first()
                user.password = password_new1
                db.session.add(user)
                db.session.commit()
                #return "密码修改成功"

                return render_template("my_center.html", success = "密码修改成功，请重新登录")
            else:
                error = "两次新密码输入不一致，请重新输入"
                return render_template("my_center.html",error = error)
        else:
            error = "旧账号密码输入不正确，请重新输入"
            return render_template("my_center.html",error = error)


@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        user = User.query.filter(User.telephone == telephone).first()
        print("拿到这个账号的数据对象 user")

        if telephone == user.telephone and password == user.password:
            session["user_id"] = user.id
            print("登录成功")

            # 如果想31天不需要登录
            session.permanent = True
            #return "登陆成功"
            return redirect(url_for("index"))
        else:
            #return "登陆失败"
            return redirect(url_for("login"))

@app.route("/regist/",methods=["GET","POST"])
def regist():
    try:
        if request.method == 'GET':
            return render_template("regist.html")

        else:
            #获取
            telephone = request.form.get("telephone")
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            email = request.form.get("captcha")


            #判断是否已经注册
            user = User.query.filter(User.telephone == telephone).first()
            if user:
                return render_template("regist.html",re_user = "手机号已经注册,请更换手机号")

            else:
                if password1 != password2:
                     return render_template("regist.html", re_password = "两次密码必须相同")

                #开始注册
                else:
                    #个月User表增加数据
                    user = User(telephone = telephone, username = username, password = password1,email = email)
                    #添加
                    db.session.add(user)
                    #提交
                    db.session.commit()
                    #return "success"
                    return redirect(url_for("login"))

    except Exception as e:
        print("注册异常")
        return "error"
        #return redirect(url_for("login"))

@app.route("/outlogin/")
def outlogin():
    session.clear()
    return redirect(url_for("login"))

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
            print("g.user",g.user.username)



@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user":user}
    else:
        #s上下文处理器 默认要一定要返回一个字典
        return{}
# 优化代码 上下文处理器、运行的流程是：
# 1、用户发送了请求先执行before_request (这里用来看session里面事都有user_id) ,拿到以后给全局g 使用  （g:在flask当中有一个专门存储用户信息的对象，再一次请求的所有地方都可以用）
#  2、执行对应的视图函数
#  3、执行上下文处理器 context_processor

if __name__ == '__main__':
    # host = "0.0.0.0",port = 8000
    app.run(debug=True,port = 8000)

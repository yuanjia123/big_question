import os

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'big_question'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False


#百度搜索 qq邮箱服务器地址和端口

# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"

# 587对应的协议是哦TLS
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "871105356@qq.com"
MAIL_PASSWORD = "zgyfsthuujpjbcfa"
MAIL_DEFAULT_SENDER = "871105356@qq.com"
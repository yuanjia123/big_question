from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from big_question import app
from exts import db

# flask_script下面的 Manager 控制台绑定app
manager = Manager(app)

#添加迁移脚本的命令到 flask_script的Manager 下面
manager.add_command("db",MigrateCommand)

#Migrate 绑定 app和db
migrate = Migrate(app,db)

if __name__ == '__main__':
    manager.run()

'''
cmd  去操作这三句话
python manage.py db init

如果已经存在一张表，继续增加表，只需要1、from models import（表明） 2、执行下面语句 
python manage.py db migrate
python manage.py db upgrade
'''
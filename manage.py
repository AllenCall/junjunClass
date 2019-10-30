from flask_script import Manager
from app import app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from  models.User import User
from  models.Question import Question

manager = Manager(app)
#1. 要使用flask_migrate，必须绑定app和db
migrate = Migrate(app,db)
# 2、把migrateCommand加到manager中
manager.add_command('db',MigrateCommand)

# cmd执行
# 1.python manage.py db init初始化迁移文件（只需执行一次）
# 2.python manage.py db migrate迁移
# 3.python manage.py db upgrade更新
if __name__ == '__main__':
    manager.run()
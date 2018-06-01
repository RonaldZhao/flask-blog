import os

from flask import Flask

def create_app(test_config=None):
    """
    这是一个应用工厂函数
    """
    # create and configure the app
    """
    __name__: 是当前python模块的名称。应用需要知道在哪里设置路径，使用 __name__ 是一个方便的方法。
    instance_relative_config: 默认为False，目的是告诉应用配置文件是相对于 instance folder 的相对路径。
    实例文件夹在 flaskr 包外面，用于存放本地数据(例如配置密钥和数据库)，不应当提交到版本控制系统
    """
    app = Flask(__name__, instance_relative_config=True)

    """
    下面的设置是一个应用的缺省配置。
    SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。在开发过程中为了方便可以设置为'dev'，但是在发布的时候应当使用一个随机值来重载它。
    DATABASE 参数是 SQLite 数据库文件的存放路径。它位于Flask用于存放实例的 app.instance_path 中。
    """
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # 使用 config.py 文件中的值来重载缺省配置，如果此文件存在的话。例如：当正式部署的时候用于设置一个正式的 SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Flask!'
    
    from . import db
    db.init_app(app)

    # 导入并注册蓝图
    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

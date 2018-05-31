import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
g 是一个特殊对象，独立于每一个请求。在处理请求的过程中，它可以用于存储 可能多个函数都会用到 的数据。
把连接存储于其中，可以多次使用，而不用在同一个请求中每次调用 get_db 时都创建一个新的连接。

current_app 也是一个特殊对象，该对象指向处理请求的 Flask 应用。这里使用了应用工厂，那么在其余的代码中就不会出现应用对象。
当应用创建后，在处理一个请求时，get_db 会被调用，这样就需要使用 current_app。
"""
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    清空所有已经存在的数据并且重新创建所有表
    """
    init_db()
    click.echo('数据库初始化完成。')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

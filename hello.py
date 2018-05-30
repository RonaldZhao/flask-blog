from flask import Flask, render_template

app = Flask(__name__)

# 使用 route 装饰器将函数绑定到 URL 上
@app.route('/')
def home():
    return '这是主页'

@app.route('/pages')
def pages():
    return '这是pages页面'

# 在路由中使用变量
@app.route('/user/')
@app.route('/user/<username>')
def user(username=None):
    # return '你好, {0}。'.format(username)
    return render_template('index.html', name=username)

@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post: {0}'.format(post_id)

if __name__ == '__main__':
    app.run()

import os
import uuid
from werkzeug.datastructures import FileStorage

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    flash
)

from routes import *

from models.user import User

from models.topic import Topic

from models.reply import Reply

from utils import log

main = Blueprint('index', __name__)


cache = redis.StrictRedis()


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    if u is None:
        flash('注册失败，用户名已注册或者用户名小于三位')
        return redirect(url_for('.index'))
    flash('注册成功')
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        # 转到 topic.index 页面
        flash('用户名或密码错误')
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def not_found(e):
    return render_template('404.html')


def created_topic(user_id):
    # ts = Topic.all(user_id=user_id)
    # ts = sorted(ts, key=lambda t: t.reply_new().created_time, reverse=True)
    # return ts
    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        ts = sorted(ts, key=lambda t: t.reply_new().created_time, reverse=True)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        cache.expire(k, 10)
        return ts


def replied_topic(user_id):
    # rs = Reply.all(user_id=user_id)
    # rt = set()
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     rt.add(t)
    # rt = sorted(rt, key=lambda s: s.reply_new().created_time, reverse=True)
    # return rt
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        rt = set()
        for r in rs:
            t = Topic.one(id=r.topic_id)
            rt.add(t)
        rt = sorted(rt, key=lambda s: s.reply_new().created_time, reverse=True)
        v = json.dumps([t.json() for t in rt])
        cache.set(k, v)
        cache.expire(k, 10)
        return rt


@main.route('/user/<string:username>')
def user_index(username):
    u = User.one(username=username)
    if u is None:
        abort(404)
    else:
        ts = created_topic(u.id)
        rt = replied_topic(u.id)
        return render_template(
            'user_profile.html',
            user=u,
            topic=ts,
            replied_topic=rt,
            )


@main.route('/images/<filename>')
# @csrf_required
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)


@main.route('/image/add', methods=['POST'])
@csrf_required
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.setting'))


@main.route('/setting')
def setting():
    u = current_user()
    token = new_csrf_token()
    return render_template('setting.html', u=u, token=token)


@main.route('/update/password', methods=['POST'])
@csrf_required
def update_password():
    u = current_user()
    old_pass = request.form['old_pass']
    if u.password == User.salted_password(old_pass):
        new_pass = request.form['new_pass']
        u.password = User.salted_password(new_pass)
        User.update(u.id, password=u.password)
        flash('success')
    else:
        flash('fail')
    return redirect(url_for('.setting'))
    # return render_template('setting.html', u=u, token=new_csrf_token())


@main.route('/update/user', methods=['POST'])
@csrf_required
def update_user():
    u = current_user()
    username = request.form['name']
    signature = request.form['signature']
    User.update(u.id, username=username, signature=signature)
    # r = 'success'
    flash('success')
    return redirect(url_for('.setting'))
    # return render_template('setting.html', u=u, token=new_csrf_token())


@main.route('/quit')
def quit():
    session.pop('user_id')
    return redirect(url_for('.index'))
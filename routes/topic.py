from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board
from models.topic import Topic

import redis


main = Blueprint('topic', __name__)
# cache = redis.StrictRedis()


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, u=u)
    # ms = Topic.all()
    # u = current_user()
    # token = new_csrf_token()
    # # if cache.exists('token'):
    # #     token = cache.get('token')
    # # else:
    # #     token = new_csrf_token()
    # #     cache['token'] = token
    # return render_template("topic/index.html", ms=ms, u=u, token=token)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u = current_user()
    return render_template("topic/detail.html", topic=m, u=u)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
def new():
    # if cache.exists('token'):
    #     token = cache.get('token')
    # else:
    #     token = new_csrf_token()
    #     cache['token'] = token
    board_id = int(request.args.get('board_id', '-1'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", token=token, bs=bs, bid=board_id)


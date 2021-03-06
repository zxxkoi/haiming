import flask_mail
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages
from config import admin_mail

main = Blueprint('mail', __name__)


# @main.route("/add", methods=["POST"])
# def add():
#     form = request.form.to_dict()
#     form['receiver_id'] = int(form['receiver_id'])
#     u = current_user()
#     form['sender_id'] = u.id
#
#     # 发邮件
#     r = User.one(id=form['receiver_id'])
#     m = flask_mail.Message(
#         subject=form['title'],
#         body=form['content'],
#         sender=admin_mail,
#         recipients=[r.email]
#     )
#     mail.send(m)
#
#     Messages.new(form)
#     return redirect(url_for('.index'))
@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    receiver_username = form['receiver_username']
    # 发邮件
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_username=u.username,
        receiver_username=receiver_username
    )

    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()
    if u is None:
        redirect(url_for('index.index'))
    send = Messages.all(sender_username=u.username)
    received = Messages.all(receiver_username=u.username)

    t = render_template(
        'mail/index.html',
        send=send,
        received=received,
    )
    return t


@main.route('/view/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.username in [message.receiver_username, message.sender_username]:
        return render_template('mail/detail.html', message=message)
    else:
        return redirect(url_for('.index'))

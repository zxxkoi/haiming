import time

from sqlalchemy import Column, Unicode, UnicodeText, String

from config import admin_mail

from models.base_model import SQLMixin, db
from models.user import User
from tasks import send_async, mailer


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_username = Column(String(50), nullable=False)
    receiver_username = Column(String(50), nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_username: str, receiver_username: str):
        form = dict(
            title=title,
            content=content,
            sender_username=sender_username,
            receiver_username=receiver_username
        )
        Messages.new(form)

        receiver: User = User.one(username=receiver_username)
        import threading
        # form = dict(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content'],
        # )
        # t = threading.Thread(target=_send_mail, kwargs=form)
        # t.start()
        #
        # m = mailer.new(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        # )
        # m.plain = form['content']
        #
        # mailer.send(m)
        # sleep(30)
        send_async.delay(
            subject=form['title'],
            author=admin_mail,
            to=receiver.email,
            plain=form['content']
        )
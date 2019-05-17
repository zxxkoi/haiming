import time

from sqlalchemy import Column, Unicode, UnicodeText, Integer

from config import admin_mail

from models.base_model import SQLMixin, db
from models.user import User
from tasks import send_async, mailer


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Messages.new(form)

        receiver: User = User.one(id=receiver_id)
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
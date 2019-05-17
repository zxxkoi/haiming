import time

from sqlalchemy import String, Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
from models.user import User
# from models.topic import Topic


class Reply(SQLMixin, db.Model):

    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    # @classmethod
    # def rank(cls, ts):
    #     for i in range(len(ts) - 1):
    #         for j in range(len(ts) - i - 1):
    #             a = ts[i].created_time
    #             b = ts[j + i + 1].created_time
    #             if a < b:
    #                 ts[i], ts[j + i + 1] = ts[j + i + 1], ts[i]
    #     return ts

    @classmethod
    def new(cls, form, user_id):
        form['created_time'] = int(time.time())
        form['updated_time'] = int(time.time())
        form['user_id'] = user_id
        m = super().new(form)
        return m
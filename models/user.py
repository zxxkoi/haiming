import hashlib

from sqlalchemy import Column, String
import config
from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    image = Column(String(100), nullable=False, default='/images/default.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)
    signature = Column(String(256), default='“ 这家伙很懒，什么个性签名都没有留下。 ”')

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        # password = form['password']
        # print('register', User.one(username=name), len(name))
        if len(name) > 2 and User.one(username=name) is None:
            # u = User.new(form)
            # u.password = u.salted_password(password)
            # u.save()
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
        # user = User.one(username=form['username'])
        # print('validate_login <{}>'.format(form))
        # if user is not None and user.password == User.salted_password(form['password']):
        #     return user
        # else:
        #     return None

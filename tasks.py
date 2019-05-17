import time

from celery import Celery
# from app import configured_app
from marrow.mailer import Mailer

import secret
from config import admin_mail

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


# app = configured_app()

def configured_mailer():
    config = {
        # 'manager.use': 'futures',
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


mailer = configured_mailer()


# @app.task(bind=True)
# def send_twitter_status(self, oauth, tweet):
#     try:
#         twitter = Twitter(oauth)
#         twitter.update_status(tweet)
#     except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
#         raise self.retry(exc=exc)


@celery.task(bind=True)
def send_async(self, subject, author, to, plain):
    try:
        m = mailer.new(
            subject=subject,
            author=author,
            to=to,
        )
        m.plain = plain
        mailer.send(m)
        time.sleep(10)
        raise ValueError('tetest')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


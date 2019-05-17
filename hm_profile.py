import app
from routes.index import user_index
import cProfile
from pstats import Stats


def profile_request(path, cookie, f):
    a = app.configured_app()
    pr = cProfile.Profile()
    headers = {'Cookie': cookie}

    with a.test_request_context(path, headers=headers):
        pr.enable()

        # r = f()
        # assert type(r) == str, r
        f('admin')

        pr.disable()

    # pr.dump_stats('gua_profile.out')
    # pr.create_stats()
    # s = Stats(pr)
    pr.create_stats()
    s = Stats(pr).sort_stats('cumulative')
    s.dump_stats('profile.pstat')

    s.print_stats('.*hm.*')
    # s.print_callers()


if __name__ == '__main__':
    path = '/user/admin'
    cookie = 'session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyX2lkIjoyfQ.XMsQRw.5Xn-_EjA2cZsY0uzSMRhOl6OBic'
    profile_request(path, cookie, user_index)

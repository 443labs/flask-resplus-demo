from flask import g
from flask.sessions import SecureCookieSessionInterface


class AppSessionInterface(SecureCookieSessionInterface):
    def save_session(self, *args, **kwargs):
        # prevent session creation when authenticating from the authorization header
        # https://flask-login.readthedocs.io/en/latest/#disabling-session-cookie-for-apis
        if g.get('authenticated_from_header'):
            return
        return super(AppSessionInterface, self).save_session(*args, **kwargs)

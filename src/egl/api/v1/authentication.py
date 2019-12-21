from flask import jsonify

from flask_login import login_required, current_user, logout_user, login_user
from flask_restplus import Resource
from flask_restplus_patched import Namespace, abort
from werkzeug.exceptions import Unauthorized

from egl.api.v1 import Auditable
from egl.api.v1.schemas import LoginSchema, UserSchema, CurrentUserSchema
from egl.db.models.user import User
from egl.db.sessions import db

ns = Namespace('Authentication')


@ns.route('/current')
class CurrentUserResource(Resource):

    @login_required
    @ns.response(UserSchema())
    def get(self):
        return current_user


@ns.route('/login')
class LoginResource(Resource, Auditable):

    @ns.parameters(LoginSchema(), locations=['json'])
    @ns.response(UserSchema())
    def post(self, login):
        """
        Wire up a non-standard REST login end point, and revisit to support a traditional Authorization header.
        This provides quick entry for all of the moving parts, and ensuring bcrypt and our seed data is working as desired.
        """

        # see if a user exists with this email address
        user = db.session.query(User).filter(User.email == login.email).one_or_none()
        if user is None:
            # create an audit log for this failed login attempt
            log = self.audit('Login Failed', '{} email not found'.format(login.email), meta={'email': login.email})
            db.session.add(log)
            db.session.commit()

            raise Unauthorized()

        # next check to see if the supplied password maches
        if user.check_password(login.password):
            # if so, log the user in via flask-login
            login_user(user)

            # create an audit log entry
            log = self.audit('Login Succeeded', '{} logged in'.format(login.email), meta={'email': login.email})
            db.session.add(log)
            db.session.commit()

            return user

        # # otherwise the email was correct, but the password was wrong, create an audit log entry
        log = self.audit('Login Failed', '{} attempted invalid password'.format(login.email), meta={'email': login.email})
        db.session.add(log)
        db.session.commit()

        raise Unauthorized()


@ns.route('/logout')
class LogoutResource(Resource):

    @login_required
    def post(self):
        logout_user()

        # otherwise the email was correct, but the password was wrong, create an audit log entry
        log = self.audit('User Logged Out', current_user.email if current_user else None)
        db.session.add(log)
        db.session.commit()

        return '', 204

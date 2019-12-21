from flask_restplus import Resource
from flask_restplus_patched import Namespace
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict, NotFound

from egl.api.v1 import Auditable
from egl.api.v1.authorization import authorize
from egl.api.v1.schemas import PagingParametersSchema, UserPageSchema, UserSchema, NewUserSchema
from egl.api.v1.services import UserService
from egl.db.models import Permissions, User
from egl.db.sessions import db

ns = Namespace('Users')


@ns.route('/')
class UsersResource(Resource):

    @ns.parameters(PagingParametersSchema(), locations=['query'])
    @ns.response(UserPageSchema())
    def get(self, paging):
        service = UserService()
        return service.get_users(paging.page, paging.per_page)

    @ns.parameters(NewUserSchema(), locations=['json'])
    @ns.response(UserSchema(), code=201)
    def post(self, user):
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@ns.route('/<id>')
class UserResource(Resource, Auditable):

    @authorize(Permissions.view_users)
    @ns.response(UserSchema())
    def get(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            raise NotFound()
        return user

    @authorize(Permissions.modify_users)
    def delete(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            raise NotFound()

        if user.is_system_user:
            raise Conflict('This is a system user and cannot be deleted.')

        try:
            db.session.delete(user)
            audit_log_entry = self.audit_deletion(db_model=User, entity=user)
            db.session.add(audit_log_entry)
            db.session.commit()
            return '', 204

        except IntegrityError:
            raise Conflict('This user still has data within the system and cannot be deleted.')

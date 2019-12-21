from egl.api.v1 import Auditable
from egl.db.models import User
from egl.db.sessions import db


class UserService(Auditable):

    def get_users(self, page, per_page):
        return db.session.query(User).paginate(page, per_page, False)

    def create(self, dto):
        raise NotImplemented()

    def update(self, dto):
        raise NotImplemented()

    def delete(self, user_id):
        raise NotImplemented()

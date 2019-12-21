import bcrypt
import uuid
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.mutable import MutableDict

from egl.db.base import Base
from egl.db.sessions import db


def hash_password(password: str) -> str:
    password = password or ''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    password = password or ''
    hashed_password = hashed_password or ''
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf-8'))


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, index=True, unique=False, nullable=True)
    meta = Column(JSON, default=MutableDict, nullable=True)
    active = Column(Boolean, default=True, nullable=False, index=True)
    is_system_user = Column(Boolean, nullable=False, default=False)

    def change_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    @property
    def is_superuser(self) -> bool:
        from egl.db.models import UserGroups
        return self.is_in_group(UserGroups.superusers)

    def is_in_group(self, group) -> bool:
        if group is None:
            return False

        if self.groups is None:
            return False

        for group in self.groups:
            if str(group.id) == str(group.id):
                return True

        return False

    def is_in_group_or_parent(self, group) -> bool:
        if self.is_in_group(group):
            return True

        return self.is_in_group(group.parent)

    def has_permission(self, permission) -> bool:

        if self.is_system_user:
            return True

        if permission is None:
            return False

        if self.groups is None:
            return False

        from egl.db.models import UserGroups
        for group in self.groups:
            if group.permissions is None:
                continue

            if str(group.id) == str(UserGroups.superusers.id):
                return True

            for group_permission in group.permissions:
                if str(group_permission.id) == str(permission.id):
                    return True

        return False

    def get_effective_permissions(self) -> list:

        if self.is_superuser:
            from egl.db.models import Permission
            return db.session.query(Permission).all()

        permissions = []
        if self.groups:
            for group in self.groups:
                if group.permissions is None:
                    continue

                for permission in group.permissions:
                    if permission not in permissions:
                        permissions.append(permission)

        return permissions

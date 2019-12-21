import logging

from egl.api.v1 import Auditable
from egl.db.models import User, Users, UserGroup, UserGroups, Permission, Permissions
from egl.db.sessions import db
from flask_login import current_user, login_user, logout_user


class SeedDataService(Auditable):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def seed(self):
        self.user = self.seed_user(Users.seed_service, audit=False)
        db.session.commit()

        self.seed_user(Users.root)
        self.seed_user(Users.admin)
        self.seed_user(Users.minion)
        self.seed_user(Users.guest)

        self.seed_group(UserGroups.superusers)
        self.seed_group(UserGroups.admins)

        self.seed_permission(Permissions.view_users)
        self.seed_permission(Permissions.view_user_groups)

        self.seed_permission(Permissions.modify_users)
        self.seed_permission(Permissions.modify_user_groups)
        self.seed_permission(Permissions.modify_permissions)
        db.session.commit()

    def seed_user(self, user: User, audit=False) -> User:
        existing = db.session.query(User).get(user.id)
        if not existing:
            existing = db.session.query(User).filter(User.email == user.email).first()
            if not existing:
                existing = user
                db.session.add(existing)
                if audit:
                    db.session.add(self.audit_creation(db_model=User, entity=user))
                self.logger.info('Adding user: {}'.format(existing))


        existing.email = user.email or existing.email
        existing.password = user.password or existing.password
        existing.meta = user.meta or existing.meta
        existing.active = user.active or existing.active
        return existing

    def seed_group(self, group: UserGroup) -> UserGroup:
        existing = db.session.query(UserGroup).get(group.id)
        if not existing:
            existing = group
            db.session.add(existing)
            self.logger.info('Adding group: {}'.format(existing))

        existing.name = group.name
        existing.is_system_group = group.is_system_group
        existing.parent_id = group.parent_id
        return existing

    def seed_permission(self, permission: Permission) -> Permission:
        existing = db.session.query(Permission).get(permission.id)
        if not existing:
            existing = permission
            db.session.add(existing)
            self.logger.info('Adding permission: {}'.format(existing))

        existing.name = permission.name
        return existing

    def seed_group_permission(self, group: UserGroup, permission: Permission):
        if permission not in group.permissions:
            group.permissions.append(permission)
            self.logger.info('Adding permission: {} to group: {}'.format(permission, group))

    def seed_group_member(self, group: UserGroup, user: User):
        if user not in group.members:
            group.members.append(user)
            self.logger.info('Adding user: {} to group: {}'.format(user, group))

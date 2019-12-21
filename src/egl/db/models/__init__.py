from egl import config
from .audit_log import AuditLog
from .permission import Permission
from .user import User, hash_password
from .user_group import UserGroup
from .user_group_member import UserGroupMember
from .user_group_permission import UserGroupPermission


class Users:
    """ Known users """
    seed_service = User(id='73ff4c06-5054-425e-a6fe-496a489a3013', email='seed@egl.corg', password=hash_password(config.get('passwords.seed')), is_system_user=True)
    root = User(id='11b11961-949d-4c44-bf6a-1a44487c141d', email='root@egl.org', password=hash_password(config.get('passwords.root')), is_system_user=True)
    admin = User(id='a1e121cc-76d8-45a1-a476-2936c6ba3278', email='admin@egl.org', password=hash_password(config.get('passwords.admin')), is_system_user=True)
    minion = User(id='99ddc422-d2d4-46a7-a236-929abeda9af9', email='minion@egl.org', password=hash_password(config.get('passwords.minion')), is_system_user=True)
    guest = User(id='788251aa-7290-4e96-b223-7ff42e27ba79', email='guest@egl.org', password=hash_password(config.get('passwords.guest')))


class UserGroups:
    """ Known user groups """
    superusers = UserGroup(id='9722578b-814c-43b0-b31c-f263dccf3e09', name='Superusers', is_system_group=True)
    admins = UserGroup(id='ceb3d33c-a84a-4f8f-8331-1f6354f37a03', name='Administrators', is_system_group=True)


class Permissions:
    """ Known permissions """
    view_users = Permission(id='13316e24-c6ab-438a-9c75-fe88dc11d35e', name='View Users')
    view_user_groups = Permission(id='93c19831-e08a-435d-a3f2-1882e4f5c1c5', name='View User Groups')

    modify_users = Permission(id='0994a60c-8556-4abe-b2b1-3190ba24a81a', name='Modify Users')
    modify_user_groups = Permission(id='d73635e4-dccc-489c-8954-b986cd19455a', name='Modify User Groups')
    modify_permissions = Permission(id='6977e2be-5bb1-46df-8a35-8c8ff790c9ed', name='Modify Permissions')

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from egl.db.base import Base


class UserGroupPermission(Base):
    __tablename__ = 'user_group_permissions'

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    user_group_id = Column(UUID(as_uuid=True), ForeignKey('user_groups.id'), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)

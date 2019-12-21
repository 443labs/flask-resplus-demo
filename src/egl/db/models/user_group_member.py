from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from egl.db.base import Base


class UserGroupMember(Base):
    __tablename__ = 'user_group_members'

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    user_group_id = Column(UUID(as_uuid=True), ForeignKey('user_groups.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

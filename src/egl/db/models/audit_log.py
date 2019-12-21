import uuid

from sqlalchemy.dialects.postgresql import UUID, JSON, TEXT
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy import func

from egl.db.base import Base


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user_email = Column(String, index=True, unique=False, nullable=True)
    action = Column(String, index=True, unique=False, nullable=True)
    description = Column(String, index=True, unique=False, nullable=True)
    meta = Column(JSON, default=MutableDict, nullable=True)
    request = Column(TEXT, index=False, unique=False, nullable=False)
    url = Column(String, index=True, unique=False, nullable=False)

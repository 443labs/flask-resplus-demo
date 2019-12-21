"""add audit logs table

Revision ID: 494020788fe3
Revises: 267e9efef687
Create Date: 2018-02-18 17:51:13.626868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, JSON, JSONB

# revision identifiers, used by Alembic.
revision = '494020788fe3'
down_revision = '267e9efef687'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'audit_logs',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('id', UUID(), nullable=False, server_default=func.uuid_generate_v4()),
        sa.Column('user_id', UUID(), nullable=True),
        sa.Column('user_email', sa.String(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('meta', JSONB(), nullable=True),
        sa.Column('request', sa.TEXT(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_url'), 'audit_logs', ['url'], unique=False)


def downgrade():
    # op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    # op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    # op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    # op.drop_index(op.f('ix_audit_logs_url'), table_name='audit_logs')
    op.drop_table('audit_logs')

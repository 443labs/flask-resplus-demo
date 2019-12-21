"""add groups and permissions tables

Revision ID: b4e59ddf3c5f
Revises: 494020788fe3
Create Date: 2018-05-30 21:07:03.377748

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, JSON

# revision identifiers, used by Alembic.
revision = 'b4e59ddf3c5f'
down_revision = '494020788fe3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_groups',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('id', UUID(), nullable=False),
        sa.Column('parent_id', UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('is_system_group', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['user_groups.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_groups_created_at'), 'user_groups', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_groups_updated_at'), 'user_groups', ['updated_at'], unique=False)
    op.create_index(op.f('ix_user_groups_name'), 'user_groups', ['name'], unique=False)

    op.create_table(
        'permissions',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('id', UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_created_at'), 'permissions', ['created_at'], unique=False)
    op.create_index(op.f('ix_permissions_updated_at'), 'permissions', ['updated_at'], unique=False)

    op.create_table(
        'user_group_members',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('user_group_id', UUID(), nullable=False),
        sa.Column('user_id', UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user_group_id'], ['user_groups.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_group_id', 'user_id')
    )

    op.create_table(
        'user_group_permissions',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('user_group_id', UUID(), nullable=False),
        sa.Column('permission_id', UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user_group_id'], ['user_groups.id'], ),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.PrimaryKeyConstraint('user_group_id', 'permission_id')
    )


def downgrade():
    op.drop_table('user_group_permissions')
    op.drop_table('user_group_members')
    op.drop_table('user_groups')
    op.drop_table('permissions')

"""add users table

Revision ID: 267e9efef687
Revises: 
Create Date: 2018-02-18 17:37:22.715432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

from sqlalchemy.dialects.postgresql import UUID, JSON
# revision identifiers, used by Alembic.
revision = '267e9efef687'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    # We want to avoid an error trying to use the uuid_generate_v4(), so we have to install this extension
    # Example Error: sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) function uuid_generate_v4() does not exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table(
        'users',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('id', UUID(), nullable=False, server_default=func.uuid_generate_v4()),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('meta', JSON(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('is_system_user', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_updated_at'), 'users', ['updated_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_active'), 'users', ['active'], unique=False)


def downgrade():
    # op.drop_index(op.f('ix_users_created_at'), table_name='users')
    # op.drop_index(op.f('ix_users_updated_at'), table_name='users')
    # op.drop_index(op.f('ix_users_email'), table_name='users')
    # op.drop_index(op.f('ix_users_active'), table_name='users')
    op.drop_table('users')

"""create user table

Revision ID: eeb52de7dc06
Revises: 
Create Date: 2021-01-11 22:29:08.914332

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eeb52de7dc06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('username', sa.String(100), unique=True),
        sa.Column('hashed_password', sa.String(100)),
        sa.Column('email', sa.String(200)),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_date', sa.DateTime)
    )


def downgrade():
    pass

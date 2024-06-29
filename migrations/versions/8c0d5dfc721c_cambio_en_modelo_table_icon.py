"""Cambio en modelo table -icon-

Revision ID: 8c0d5dfc721c
Revises: e5849c0bfa8e
Create Date: 2024-06-29 20:53:13.531758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c0d5dfc721c'
down_revision = 'e5849c0bfa8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('icon', sa.String(length=250), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table', schema=None) as batch_op:
        batch_op.drop_column('icon')

    # ### end Alembic commands ###

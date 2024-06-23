"""Initial migration.

Revision ID: 3765a4f2e4d6
Revises: 
Create Date: 2024-06-20 11:03:36.650344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3765a4f2e4d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('restaurant_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_number', sa.Integer(), nullable=False),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id_client'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('table_number')
    )
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id']),
    sa.ForeignKeyConstraint(['table_id'], ['table.id']),
    sa.ForeignKeyConstraint(['order_id'], ['order.id']),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('table_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_table', sa.Integer(), nullable=False),
    sa.Column('id_client', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id_client'], ['client.id'], ),
    sa.ForeignKeyConstraint(['id_table'], ['table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_table('invoice_detail',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('id_invoice', sa.Integer(), nullable=False),
    # sa.Column('id_product', sa.Integer(), nullable=False),
    # sa.Column('quantity', sa.Integer(), nullable=False),
    # sa.Column('unit_price', sa.Float(), nullable=False),
    # sa.Column('subtotal', sa.Float(), nullable=False),
    # sa.ForeignKeyConstraint(['id_invoice'], ['invoice.id'], ),
    # sa.ForeignKeyConstraint(['id_product'], ['product.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    op.create_table('product_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_session', sa.Integer(), nullable=False),
    sa.Column('id_product', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id_product'], ['product.id'], ),
    sa.ForeignKeyConstraint(['id_session'], ['table_session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_table')
    # op.drop_table('invoice_detail')
    op.drop_table('table_session')
    op.drop_table('invoice')
    op.drop_table('table')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('client')
    op.drop_table('order')
    op.drop_table('order_item')
    op.drop_table('menu')
    op.drop_table('restaurant')
    # ### end Alembic commands ###

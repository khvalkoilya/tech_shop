"""add product and type

Revision ID: ed2b2d41c3ca
Revises: 9eadbad22452
Create Date: 2020-03-29 19:52:32.714673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2b2d41c3ca'
down_revision = '9eadbad22452'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=64), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_model'), 'product', ['model'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_model'), table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###

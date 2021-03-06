"""new model

Revision ID: 6711a8d82e3b
Revises: 
Create Date: 2020-02-28 22:14:31.889611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6711a8d82e3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.String(length=30), nullable=False),
    sa.Column('lastname', sa.String(length=30), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('register_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_username'), 'admin', ['username'], unique=True)
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('vehicle_number', sa.String(length=20), nullable=False),
    sa.Column('chasis_num', sa.String(length=20), nullable=False),
    sa.Column('color', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=250), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    op.drop_index(op.f('ix_admin_username'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###

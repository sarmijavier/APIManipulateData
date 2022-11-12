"""empty message

Revision ID: 814d99e2c200
Revises: 30d1f61f6022
Create Date: 2022-11-02 15:17:13.167341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '814d99e2c200'
down_revision = '30d1f61f6022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foot_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('brand', sa.String(length=100), nullable=True),
    sa.Column('calories', sa.Float(), nullable=True),
    sa.Column('carbs', sa.Float(), nullable=True),
    sa.Column('fat', sa.Float(), nullable=True),
    sa.Column('fiber', sa.Float(), nullable=True),
    sa.Column('protein', sa.Float(), nullable=True),
    sa.Column('sodium', sa.Float(), nullable=True),
    sa.Column('water', sa.Float(), nullable=True),
    sa.Column('name', sa.String(length=500), nullable=True),
    sa.Column('complete_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), server_default='0', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('foot_data')
    # ### end Alembic commands ###
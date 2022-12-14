"""empty message

Revision ID: 13a4cdeb847a
Revises: 1b58f4940a94
Create Date: 2022-11-02 23:05:24.740866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13a4cdeb847a'
down_revision = '1b58f4940a94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record_date', sa.Column('data_taken', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('record_date', 'data_taken')
    # ### end Alembic commands ###

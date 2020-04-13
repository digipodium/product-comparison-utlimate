"""empty message

Revision ID: 5c89912733d6
Revises: 4cd97c0f838c
Create Date: 2020-04-11 15:14:43.340799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c89912733d6'
down_revision = '4cd97c0f838c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_scraped_data_link'), 'scraped_data', ['link'], unique=True)
    op.create_index(op.f('ix_scraped_data_name'), 'scraped_data', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scraped_data_name'), table_name='scraped_data')
    op.drop_index(op.f('ix_scraped_data_link'), table_name='scraped_data')
    # ### end Alembic commands ###

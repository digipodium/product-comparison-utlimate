"""empty message

Revision ID: cb882321a76b
Revises: 5c89912733d6
Create Date: 2020-04-11 15:19:41.919473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb882321a76b'
down_revision = '5c89912733d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_post_created_on', table_name='post')
    op.drop_table('post')
    op.add_column('scraped_data', sa.Column('query', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scraped_data', 'query')
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('created_on', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_post_created_on', 'post', ['created_on'], unique=False)
    # ### end Alembic commands ###

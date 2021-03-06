"""add user cascade

Revision ID: 5fd5c089b572
Revises: cb11df18c46a
Create Date: 2018-07-22 01:10:45.413108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fd5c089b572'
down_revision = 'cb11df18c46a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trakt_creds', type_='foreignkey')
    op.create_foreign_key(None, 'trakt_creds', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trakt_creds', type_='foreignkey')
    op.create_foreign_key(None, 'trakt_creds', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###

"""empty message

Revision ID: 9a147a066ac5
Revises: 5644e8296c86
Create Date: 2022-06-26 20:19:17.127611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9a147a066ac5'
down_revision = '5644e8296c86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('character_name', sa.String(length=50), nullable=True))
    op.drop_constraint('favorites_ibfk_4', 'favorites', type_='foreignkey')
    op.create_foreign_key(None, 'favorites', 'character', ['character_name'], ['name'])
    op.drop_column('favorites', 'character_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('character_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'favorites', type_='foreignkey')
    op.create_foreign_key('favorites_ibfk_4', 'favorites', 'character', ['character_id'], ['id'])
    op.drop_column('favorites', 'character_name')
    # ### end Alembic commands ###
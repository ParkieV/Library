"""initial

Revision ID: 7f70143598b4
Revises: 
Create Date: 2023-05-16 23:55:23.656084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f70143598b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('authors', sa.String(), nullable=True),
    sa.Column('user_id_taken', sa.Integer(), nullable=True),
    sa.Column('user_reserved_id', sa.Integer(), nullable=True),
    sa.Column('date_start_use', sa.Date(), nullable=True),
    sa.Column('date_finish_use', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id_taken'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_reserved_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.Column('book_id_taken', sa.Integer(), nullable=True),
    sa.Column('reserved_book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id_taken'], ['books.id'], ),
    sa.ForeignKeyConstraint(['reserved_book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('books')
    # ### end Alembic commands ###

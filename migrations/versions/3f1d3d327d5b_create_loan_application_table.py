"""create loan application table

Revision ID: 3f1d3d327d5b
Revises: 
Create Date: 2023-11-27 18:30:20.422173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f1d3d327d5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loan_application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.String(length=255), nullable=False),
    sa.Column('establishment_year', sa.Integer(), nullable=False),
    sa.Column('loan_amount', sa.Integer(), nullable=False),
    sa.Column('accounting_software', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan_application')
    # ### end Alembic commands ###

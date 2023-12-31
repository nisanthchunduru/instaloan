"""Add business email attribute to LoanApplication model

Revision ID: 76eaf25be1f4
Revises: 93e5d6015198
Create Date: 2023-11-27 20:58:43.414450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76eaf25be1f4'
down_revision = '93e5d6015198'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('loan_application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('business_email', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('loan_application', schema=None) as batch_op:
        batch_op.drop_column('business_email')

    # ### end Alembic commands ###

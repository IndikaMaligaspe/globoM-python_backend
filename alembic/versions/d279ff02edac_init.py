"""init

Revision ID: d279ff02edac
Revises: 
Create Date: 2020-12-20 05:37:54.168734

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'd279ff02edac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
       "users",
       sa.Column("id", sa.Integer, primary_key=True),
       sa.Column("first_name", sa.String),
       sa.Column("last_name", sa.String),
       sa.Column("email", sa.String, nullable=False),
       sa.Column("password", sa.String, nullable=False),
       sa.Column("is_active", sa.Boolean), 
       sa.Column("created_on", sa.Date), 
    )

    op.create_table(
       "transactions",
       sa.Column("id", sa.Integer, primary_key=True),
       sa.Column("transaction_date", sa.Date, nullable=False),
       sa.Column("transaction_type", sa.String, nullable=False),
       sa.Column("description", sa.String, nullable=False),
       sa.Column("charge", sa.Numeric, default=0),
       sa.Column("deposit", sa.Numeric, default=0), 
       sa.Column("notes", sa.String), 
       sa.Column("createdOn", sa.Date, default=datetime.now()),
       sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    )


def downgrade():
    op.drop_table(
        "transactions"
    )
    op.drop_table(
        "users"
    )


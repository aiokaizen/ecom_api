"""First migration

Revision ID: 2c890a8cddbf
Revises:
Create Date: 2025-01-12 20:45:54.483549

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import String


# revision identifiers, used by Alembic.
revision: str = "2c890a8cddbf"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", String(length=256), nullable=False),
        sa.Column("price", sa.Numeric(precision=11, scale=2), nullable=False),
        sa.Column("description", String(), nullable=True),
        sa.Column("technical_properties", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="almbc",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("product", schema="almbc")
    # ### end Alembic commands ###

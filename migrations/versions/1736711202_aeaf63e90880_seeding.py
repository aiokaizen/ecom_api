"""Seeding

Revision ID: aeaf63e90880
Revises: 2c890a8cddbf
Create Date: 2025-01-12 20:46:42.475419

"""

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from faslava.config.database_manager import db_manager

from app.models import Product


# revision identifiers, used by Alembic.
revision: str = "aeaf63e90880"
down_revision: Union[str, None] = "2c890a8cddbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    product_data = []
    print("\n\nSEEDING STARTED\n\n")
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    with db_manager.session_scope() as session:
        for product_dict in product_data:
            print("Creating product:", product_dict["name"])
            product = Product(**product_dict)
            session.add(product)


def downgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    with db_manager.session_scope() as session:
        product_ids = [product["id"] for product in product_data]
        statement = sqlmodel.delete(Product).where(Product.id.in_(product_ids))
        session.exec(statement)

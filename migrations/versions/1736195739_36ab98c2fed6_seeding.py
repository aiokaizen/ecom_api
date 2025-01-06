"""Seeding

Revision ID: 36ab98c2fed6
Revises: 6d7d13d0ba3d
Create Date: 2025-01-06 21:35:39.949051

"""

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from faslava.config.database_manager import db_manager

from app.models.models import Product, TechnicalProperty


# revision identifiers, used by Alembic.
revision: str = "36ab98c2fed6"
down_revision: Union[str, None] = "6d7d13d0ba3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    with db_manager.session_scope() as session:
        for product_dict in product_data:
            product_properties = product_dict.pop("technical_properties", {})
            product = Product(**product_dict)
            session.add(product)
            session.flush()
            for name, value in product_properties.items():
                property = TechnicalProperty(
                    **{"product_id": product.id, "name": name, "value": value}
                )
                session.add(property)


def downgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    with db_manager.session_scope() as session:
        product_ids = [product["id"] for product in product_data]

        sqlmodel.delete(TechnicalProperty).where(
            TechnicalProperty.product_id.in_(product_ids)
        )

        sqlmodel.delete(Product).where(Product.id.in_(product_ids))

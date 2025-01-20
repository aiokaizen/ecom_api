"""Seeding

Revision ID: 31c5448e0ac3
Revises: 3b644c2bb1bd
Create Date: 2025-01-20 20:41:06.844164

"""

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import insert

from faslava.config.database_manager import engine

from app.models.models import Product


# revision identifiers, used by Alembic.
revision: str = "31c5448e0ac3"
down_revision: Union[str, None] = "3b644c2bb1bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    # Code example for the migration
    print("Product data:", product_data)
    with engine.begin() as conn:
        result = conn.execute(insert(Product), product_data)


def downgrade() -> None:
    product_ids = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)
        product_ids = [product["id"] for product in product_data]

    # Code example for the migration
    print("Product data:", product_data)
    with engine.begin() as conn:
        result = conn.execute(sa.delete(Product).where(Product.id.in_(product_ids)))

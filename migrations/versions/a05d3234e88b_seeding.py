"""seeding

Revision ID: a05d3234e88b
Revises: f0d170b4acd7
Create Date: 2024-12-29 18:23:18.701385

"""

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlmodel import delete

from faslava.config.database_manager import db_manager
from app.models.models import Product, TechnicalProperty
from app.services.product_services import create_product, create_technical_property


# revision identifiers, used by Alembic.
revision: str = "a05d3234e88b"
down_revision: Union[str, None] = "f0d170b4acd7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    for product_dict in product_data:
        product_properties = product_dict.pop("technical_properties", {})
        product = Product(**product_dict)
        create_product(product)
        for name, value in product_properties.items():
            property = TechnicalProperty(
                **{"product_id": product.id, "name": name, "value": value}
            )
            create_technical_property(property)


def downgrade() -> None:
    product_data = []
    with open("seeding_data.json", "r") as f:
        product_data = json.load(f)

    with db_manager.session_scope() as session:
        product_ids = [product["id"] for product in product_data]

        delete(TechnicalProperty).where(TechnicalProperty.product_id.in_(product_ids))

        delete(Product).where(Product.id.in_(product_ids))

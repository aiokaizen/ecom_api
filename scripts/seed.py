import random

from faker import Faker
from faslava.models.user_models import UserAccount
from scripts.seed_data import CATEGORIES_LIST, CONTINENTS
from slugify import slugify

from sqlalchemy import insert

from faslava.logging import logger
from faslava.config.database_manager import engine

from app.models import (
    Product,
    Category,
    CategoryProductAssociation,
    Tag,
    Order,
    OrderProductAssociation,
    Customer,
)

from scripts.utils import get_product_data, generate_price, generate_random_properties

# ProductNameProvider = DynamicProvider(
#     provider_name="product_name",
#     elements=[p["name"] for p in get_product_data()],
# )

fake = Faker(locale="en_US")
# fake.add_provider(ProductNameProvider)


def seed(product_count: int = 100, order_count: int = 1000):
    products_data = get_product_data()
    logger.info("Start seeding process...")
    logger.info(f"Creating {product_count} products and {order_count} orders.")
    products_list = []
    logger.info("Generating products...")
    for pindex in range(product_count):
        logger.debug(f"Generating product {pindex + 1} data")
        try:
            product_dict = products_data[pindex]
        except IndexError:
            product_dict = {}
        product_data = {
            "id": product_dict.get("id", None),
            "name": product_dict.get("name", fake.catch_phrase()),
            "price": product_dict.get("price", generate_price()),
            "description": product_dict.get("description", fake.paragraph()),
            "custom_properties": product_dict.get(
                "custom_properties", generate_random_properties(fake, min=1)
            ),
            "tags": [fake.catch_phrase() for _ in range(random.randint(0, 10))],
            "sku": fake.numerify("%####"),
            "manufacturer": fake.company(),
        }
        products_list.append(product_data)

    with engine.begin() as conn:
        logger.info("Bulk inserting generated products to the database.")
        conn.execute(insert(Product), products_list)

    logger.info("Generating categories...")
    categories_data = []
    for cat in CATEGORIES_LIST:
        categories_data.append({"name": cat})

    with engine.begin() as conn:
        logger.info("Bulk inserting generated categories to the database.")
        conn.execute(insert(Category), categories_data)

    logger.info("Generating user accounts...")
    users_data = []
    for _ in range(max(order_count // 100, 5)):
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        users_data.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "full_name": full_name,
                "gender": random.choice(["M", "F"]),
                "image_url": f"media/user/avatar/{slugify(full_name)}.jpeg",
                "geoip": {
                    "ip": fake.ipv4(),
                    "city_name": fake.city(),
                    "country_iso_code": fake.country_code(),
                    "location": {
                        "lon": round(random.random() * 260 - 180, 2),
                        "lat": round(random.random() * 180 - 90, 2),
                    },
                    "region_name": fake.catch_phrase(),
                    "continent_name": random.choice(CONTINENTS),
                },
            }
        )

    with engine.begin() as conn:
        logger.info("Bulk inserting generated users to the database.")
        conn.execute(insert(UserAccount), users_data)

    logger.info("Seeding process finished successfully.")

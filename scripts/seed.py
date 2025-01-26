from datetime import datetime, timedelta
import random

from faker import Faker
from faker.providers import phone_number, address
from enums.enums import OrderTypeEnum
from faslava.models.user_models import Address, UserAccount
from scripts.seed_data import CATEGORIES_LIST, CONTINENTS
from slugify import slugify

# from sqlalchemy import insert, select
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

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

from scripts.utils import (
    generate_discount,
    generate_phone_number,
    generate_tax,
    get_product_data,
    generate_price,
    generate_random_properties,
)

# ProductNameProvider = DynamicProvider(
#     provider_name="product_name",
#     elements=[p["name"] for p in get_product_data()],
# )

fake = Faker(locale="en_US")
fake.add_provider(phone_number)
fake.add_provider(address)
# fake.add_provider(ProductNameProvider)


def seed(product_count: int = 100, order_count: int = 1000):
    products_data = get_product_data()
    logger.info("Start seeding process...")
    logger.info(f"Creating {product_count} products and {order_count} orders.")
    products_list = []
    tags_list = []
    logger.info("Generating products...")
    with engine.begin() as conn:
        result = conn.execute(select(Product.id))
        users_ids = [id[0] for id in result.all()]

    for pindex in range(product_count):
        logger.debug(f"Generating product {pindex + 1} data")
        try:
            product_dict = products_data[pindex]
        except IndexError:
            product_dict = {}
        product_data = {
            # "id": pid,
            "name": product_dict.get("name", fake.catch_phrase()),
            "price": product_dict.get("price", generate_price()),
            "description": product_dict.get("description", fake.paragraph()),
            "custom_properties": product_dict.get(
                "custom_properties", generate_random_properties(fake, min=1)
            ),
            "tags": [
                fake.catch_phrase().split(" ")[0] for _ in range(random.randint(0, 10))
            ],
            "sku": fake.numerify("%####"),
            "brand": fake.company(),
            "manufacturer": fake.company(),
        }

        if product_data["tags"]:
            tags_list.extend([{"name": tag} for tag in product_data["tags"]])

        products_list.append(product_data)

    with engine.begin() as conn:
        logger.info("Bulk inserting generated products to the database.")
        conn.execute(insert(Product), products_list)

    product_ids = []
    with engine.begin() as conn:
        logger.debug("Retrieving product ids...")
        result = conn.execute(select(Product.id))
        product_ids = [id[0] for id in result.all()]

    with engine.begin() as conn:
        logger.info("Bulk inserting generated product tags to the database.")
        stmt = insert(Tag).values(tags_list)
        stmt = stmt.on_conflict_do_nothing()
        conn.execute(stmt)

    logger.info("Generating categories...")
    categories_data = []
    for cat in CATEGORIES_LIST:
        categories_data.append({"name": cat})

    with engine.begin() as conn:
        logger.info("Bulk inserting generated categories to the database.")
        conn.execute(insert(Category), categories_data)

    category_ids = []
    with engine.begin() as conn:
        logger.debug("Retrieving product ids...")
        result = conn.execute(select(Category.id))
        category_ids = [id[0] for id in result.all()]

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

    logger.info("Generating customers...")
    with engine.begin() as conn:
        logger.debug("Retrieving user ids...")
        result = conn.execute(select(UserAccount.id))
        users_ids = [id[0] for id in result.all()]

    customers_data = []
    customer_ids = []
    logger.debug("Creating customer data")
    for uid in users_ids:
        customers_data.append({"user_id": uid})

    with engine.begin() as conn:
        logger.info("Bulk inserting generated customers to the database.")
        conn.execute(insert(Customer), customers_data)

    addresses_data = []
    logger.debug("Creating address data")
    for uid in users_ids:
        for _ in range(random.randint(1, 2)):
            addresses_data.append(
                {
                    "user_id": uid,
                    "email_address": fake.email(),
                    "email_address_verified": random.choice([True, True, True, False]),
                    "phone_number": generate_phone_number(fake),
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "postal_code": fake.postcode().split("-")[0],
                }
            )

    with engine.begin() as conn:
        logger.info("Bulk inserting generated addresses to the database.")
        conn.execute(insert(Address).values(addresses_data))

    logger.info("Generating orders...")

    with engine.begin() as conn:
        logger.debug("Retrieving customer ids...")
        result = conn.execute(select(Customer.id))
        customer_ids = [id[0] for id in result.all()]

    orders_data = []
    start_date = datetime.now()
    day = 0
    batch_size = 1000
    for i in range(order_count):
        order_date = start_date - timedelta(days=day)
        go_next_day = random.random() >= 0.9  # Generates about 1000 order / 3 months
        if go_next_day:
            day += 1
        logger.debug(f"Go next day {day + 1}? {go_next_day}")

        orders_data.append(
            {
                "currency": random.choice(["USD", "MAD", "USD", "EUR", "USD", "MAD"]),
                "order_type": OrderTypeEnum.ORDER,
                "order_date": order_date,
                "total_price": 0,
                "discount": generate_discount(),
                "tax": generate_tax(),
                "total_quantity": 0,
                "products_count": 0,
                "customer_id": random.choice(customer_ids),
                "trigger_event": {
                    "source": "seeding",
                },
            }
        )

        if i % batch_size == 0:
            with engine.begin() as conn:
                logger.info("Bulk inserting generated orders to the database.")
                conn.execute(insert(Order), orders_data)
            orders_data.clear()

    with engine.begin() as conn:
        logger.info("Bulk inserting generated orders to the database.")
        conn.execute(insert(Order), orders_data)

    logger.info("Seeding process finished successfully.")

import json
import random
from copy import copy

from faker import Faker

from faslava.logging import logger
from scripts.seed_data import AVAILABLE_PROPERTIES_CONFIGURATION


def get_product_data():
    with open("seeding_data.json", "r") as f:
        return json.load(f)


def generate_price():
    multiples = [10, 10, 10, 10, 100, 100, 100, 100, 1000, 1000]
    price = round(random.random() * random.choice(multiples), 2)
    logger.debug(f"Generating price: {price}")
    return price


def generate_random_properties(fake: Faker, min: int = 0, max: int = 5):
    """
    Generate random properties.

    Args:
        min (int): The minimum properties to generate.
        max (int): The maximum properties to generate.
    """
    available_properties = AVAILABLE_PROPERTIES_CONFIGURATION
    property_pool = copy(available_properties)
    properties = {}
    for _ in range(random.randint(min, max)):
        property_name = random.choice(list(property_pool.keys()))
        property_conf = property_pool.pop(property_name)
        if isinstance(property_conf, list):
            properties[property_name] = random.choice(property_conf)
        if isinstance(property_conf, tuple):
            if property_conf[0] == "string":
                value = fake.catch_phrase()
                if property_conf[1]:
                    value = f"{value} " + property_conf[1]
            elif property_conf[0] == "float":
                value = round(random.random() * 100, 2)
                if property_conf[1]:
                    value = f"{value} " + property_conf[1]
            elif property_conf[0] == "int":
                value = round(random.randint(2, 120), 2)
                if property_conf[1]:
                    value = f"{value} " + property_conf[1]
            elif property_conf[0] == "choice":
                value = random.choice(property_conf[2])
                if property_conf[1]:
                    value = f"{value} " + property_conf[1]
            properties[property_name] = value
        elif isinstance(property_conf, str):
            if property_conf == "string":
                value = fake.catch_phrase()
            elif property_conf == "float":
                value = round(random.random() * 100, 2)
            elif property_conf == "int":
                value = round(random.randint(1, 100), 2)
            properties[property_name] = value
    logger.debug(f"Custom properties generated: {json.dumps(properties, indent=4)}")
    return properties

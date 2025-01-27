import os
import secrets
import string
from math import ceil
from typing import Optional

from slugify import slugify

from fastapi import UploadFile

from faslava.logging import logger

special_characters = ":;.!@#$%^&*_-+=?><~"


def gettext_lazy(s: str) -> str:
    """Internationalization placeholder function."""
    return f"<Tr> {s}"


def generate_secret_key(length: int = 50) -> str:
    """
    Generates a random secret_key and returns it.

    Args:
        length (int): The length of the secret key.
    """
    characters = string.ascii_letters + string.digits + special_characters
    return "".join(secrets.choice(characters) for _ in range(length))


def get_project_secret_key(length: int = 50) -> str:
    """
    Retrieves the project secret_key from .secret_key file if it exists, otherwize, it generates a random key and returns it.

    Args:
        length (int): The length of the secret key.
    """
    secret_key_file = ".secret_key"
    if os.path.exists(secret_key_file):
        with open(secret_key_file, "r") as f:
            return f.read()

    with open(secret_key_file, "w") as f:
        secret_key = generate_secret_key(length)
        f.write(secret_key)
        return secret_key


def generate_random_password(
    length: int = 8, include_special_chars: bool = True
) -> str:
    """
    Generates a random password and returns it.

    Args:
        length (int): The length of the secret key.
        include_special_chars (bool): If set to False, the password will not include special characters.
    """
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += special_characters
    return "".join(secrets.choice(characters) for _ in range(length))


async def save_uploaded_file(
    file: UploadFile,
    *,
    upload_dir: Optional[str] = None,
    batch_size: int = 10000,
    filename: Optional[str] = None,
):
    default_upload_dir = "user_upload"
    if not filename:
        filename = file.filename
    file_dir = upload_dir or default_upload_dir
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    filename, ext = os.path.splitext(filename)
    filepath: str = os.path.join(file_dir, f"{slugify(filename)}{ext}")
    try:
        with open(filepath, "wb") as f:
            for _ in range(ceil(file.size / batch_size)):
                f.write(await file.read(batch_size))

        return filepath
    except Exception as e:
        logger.error(
            f"Unexpected error was raised while saving the file {filepath}. e: {e}"
        )
        raise e

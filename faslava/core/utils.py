import os
import secrets
import string

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

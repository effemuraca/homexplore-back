from passlib.context import CryptContext
from bcrypt import hashpw, gensalt, checkpw
            
def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_hashed_password(hashed: str, password: str) -> bool:
    """
    Verifies the password against the hashed password.

    Args:
        hashed (str): The stored, hashed password.
        password (str): The plain text password to verify.

    Returns:
        bool: True if password is correct, False otherwise.
    """
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
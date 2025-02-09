from passlib.context import CryptContext
from bcrypt import hashpw, gensalt, checkpw
            
def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt
    :param password: The password to hash
    :return: The hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_hashed_password(hashed: str, password: str) -> bool:
    """
    Verifies the password against the hashed password
    :param hashed: The hashed password
    :param password: The password to verify
    """
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
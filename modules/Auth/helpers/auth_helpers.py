from passlib.context import CryptContext
from bcrypt import hashpw, gensalt, checkpw
            
def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_hashed_password(hashed: str, password: str) -> bool:
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
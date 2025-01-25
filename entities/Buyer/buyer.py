from pydantic import BaseModel
from typing import Optional

class Buyer(BaseModel):
    buyer_id: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None

    def __init__(
        self,
        buyer_id: str = None,
        password: str = None,
        email: str = None,
        phone_number: str = None,
        name: str = None,
        surname: str = None,
        age: int = None
    ):
        super().__init__()
        self.buyer_id = buyer_id
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.name = name
        self.surname = surname
        self.age = age
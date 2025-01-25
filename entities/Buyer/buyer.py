from pydantic import BaseModel
from typing import Optional
import re

class BuyerInfo(BaseModel):
    password: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None

    def __init__(
        self,
        password: str = None,
        email: str = None,
        phone_number: str = None,
        name: str = None,
        surname: str = None,
        age: int = None
    ):
        super().__init__()
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.name = name
        self.surname = surname
        self.age = age

    def check_buyer_info(self):
        """
        Checks if the minimum buyer infos required are inserted (age optional).
        """
        if not self.password or not self.email or not self.phone_number or not self.name or not self.surname:
            return False
        phone_pattern = re.compile(r'^\+\d{1,3}\s?\d{7,14}$')
        email_pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        if not phone_pattern.match(self.phone_number) or not email_pattern.match(self.email):
            return False
        return True

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
   
    def __init__(self, buyer_info: BuyerInfo):
        super().__init__()
        self.password = buyer_info.password
        self.email = buyer_info.email
        self.phone_number = buyer_info.phone_number
        self.name = buyer_info.name
        self.surname = buyer_info.surname
        self.age = buyer_info.age

    def get_buyer_info(self):
        """
        Returns the information not null of the buyer except the buyer_id.
        """
        return {k: v for k, v in self.dict().items() if k != "buyer_id" and v is not None}
    
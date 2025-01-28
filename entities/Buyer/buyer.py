import logging
import re
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Configura il logger
logger = logging.getLogger(__name__)

class Buyer(BaseModel):
    buyer_id: Optional[str] = Field(None, example="60d5ec49f8d2e30b8c8b4567")
    password: Optional[str] = Field(None, example="SecureP@ssw0rd")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    phone_number: Optional[str] = Field(None, example="+1 1234567890")
    name: Optional[str] = Field(None, example="John")
    surname: Optional[str] = Field(None, example="Doe")
    age: Optional[int] = Field(None, example=30)  #campo opzionale

    def update_info(self, buyer_info: 'Buyer'):
        """
        Aggiorna le informazioni del buyer con i dati forniti in buyer_info.
        """
        for field, value in buyer_info.model_dump().items():
            if value is not None:
                setattr(self, field, value)
        logger.debug(f"Buyer aggiornato: {self}")

    def get_buyer_info(self) -> dict:
        return self.model_dump()

    def is_valid(self) -> bool:
        """
        Verifica se le informazioni minime del buyer richieste sono valide.
        """
        if not all([self.password, self.email, self.phone_number, self.name, self.surname]):
            return False
        phone_pattern = re.compile(r'^\+\d{1,3}\s?\d{7,14}$')
        email_pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        if not phone_pattern.match(self.phone_number):
            return False
        if not email_pattern.match(self.email):
            return False
        return True
    

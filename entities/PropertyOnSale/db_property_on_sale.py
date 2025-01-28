from typing import Optional
from bson.objectid import ObjectId
from entities.PropertyOnSale.property_on_sale import PropertyOnSale
from setup.mongo_setup.mongo_setup import get_default_mongo_db
import logging


# Configura il logger
logger = logging.getLogger(__name__)


class PropertyOnSaleDB:
    def __init__(self, property_on_sale: Optional[PropertyOnSale] = None):
        self.property_on_sale = property_on_sale
    
    def create_property_on_sale(self) -> bool:
        if not self.property_on_sale:
            logger.error("Nessuna proprietà da creare.")
            return False
        if not self.property_on_sale.check_min_info():
            logger.error("Informazioni minime non fornite per la creazione della proprietà.")
            return False
        mongo_client = get_default_mongo_db()
        result = mongo_client.PropertyOnSale.insert_one(self.property_on_sale.model_dump(exclude_none=True, exclude={"property_on_sale_id"}))
        if result.inserted_id:
            self.property_on_sale.property_on_sale_id = str(result.inserted_id)
            logger.info(f"Proprietà creata con id {self.property_on_sale.property_on_sale_id}.")
            return True
        logger.error("Creazione della proprietà fallita.")
        return False
    
    
    

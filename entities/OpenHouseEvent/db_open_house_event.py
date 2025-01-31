import json
from typing import Optional
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
import redis
from setup.redis_setup.redis_setup import get_redis_client
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class OpenHouseEventDB:
    open_house_event: OpenHouseEvent = None

    def __init__(self, open_house_event: OpenHouseEvent):
        self.open_house_event = open_house_event

    # All logic has been moved to ReservationsSellerDB. This file can be removed or left empty.
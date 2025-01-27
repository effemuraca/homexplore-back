import json
from typing import Optional
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from setup.redis_setup.redis_setup import get_redis_client
import redis
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class OpenHouseEventDB:
    open_house_event: OpenHouseEvent = None

    def __init__(self, open_house_event: OpenHouseEvent):
        self.open_house_event = open_house_event

    def get_open_house_event_by_property(self, property_id: int) -> Optional[OpenHouseEvent]:
        if not property_id:
            logger.warning("Property ID not provided.")
            return None
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            logger.info(f"No open house event found for property_id={property_id}.")
            return None
        try:
            data = json.loads(raw_data)
            open_house_info = OpenHouseInfo(
                date=data.get("date"),
                time=data.get("time"),
                max_attendees=data.get("max_attendees", 0),
                attendees=data.get("attendees", 0)
            )
            self.open_house_event = OpenHouseEvent(property_id=property_id, open_house_info=open_house_info)
            return self.open_house_event
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding JSON data: {e}")
            return None

    def delete_open_house_event_by_property(self, property_id: int) -> bool:
        if not property_id:
            logger.warning("Property ID not provided for deletion.")
            return False
        redis_client = get_redis_client()
        try:
            result = redis_client.delete(f"property_id:{property_id}:open_house_info")
            if result:
                logger.info(f"Open house event deleted for property_id={property_id}.")
            else:
                logger.warning(f"Failed to delete open house event for property_id={property_id}.")
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion: {e}")
            return False

    def create_open_house_event(self, property_id: int, open_house_info: OpenHouseInfo) -> bool:
        if not property_id or not open_house_info:
            logger.warning("Property ID or OpenHouseInfo not provided for creation.")
            return False
        redis_client = get_redis_client()
        data = {
            "date": open_house_info.date,
            "time": open_house_info.time,
            "max_attendees": open_house_info.max_attendees,
            "attendees": open_house_info.attendees
        }
        try:
            result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
            # Set expiration based on date and time
            self.open_house_event = OpenHouseEvent(property_id=property_id, open_house_info=open_house_info)
            time_sec = self.open_house_event.date_and_time_to_seconds()
            if time_sec > 0:
                redis_client.expire(f"property_id:{property_id}:open_house_info", time_sec)
                logger.info(f"Set expiration for open house event of property_id={property_id} to {time_sec} seconds.")
            logger.info(f"Open house event created for property_id={property_id}.")
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during creation: {e}")
            return False

    def update_open_house_event(self, property_id: int, open_house_info: OpenHouseInfo) -> bool:
        if not property_id or not open_house_info:
            logger.warning("Property ID or OpenHouseInfo not provided for update.")
            return False
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No existing open house event found for property_id={property_id} to update.")
            return False
        try:
            data = json.loads(raw_data)
            if open_house_info.date is not None:
                data["date"] = open_house_info.date
            if open_house_info.time is not None:
                data["time"] = open_house_info.time
            if open_house_info.max_attendees is not None:
                data["max_attendees"] = open_house_info.max_attendees
            if open_house_info.attendees is not None:
                data["attendees"] = open_house_info.attendees

            result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
            self.open_house_event = OpenHouseEvent(property_id=property_id, open_house_info=open_house_info)
            logger.info(f"Open house event updated for property_id={property_id}.")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating open house event: {e}")
            return False

    def increment_attendees(self, property_id: int) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No open house event found for property_id={property_id} to increment attendees.")
            return False
        try:
            data = json.loads(raw_data)
            if data.get("attendees", 0) >= data.get("max_attendees", 0):
                logger.info(f"Attendees limit reached for property_id={property_id}.")
                return False
            data["attendees"] += 1
            result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
            logger.info(f"Attendees incremented for property_id={property_id}. New count: {data['attendees']}")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error incrementing attendees: {e}")
            return False

    def decrement_attendees(self, property_id: int) -> bool:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No open house event found for property_id={property_id} to decrement attendees.")
            return False
        try:
            data = json.loads(raw_data)
            if data.get("attendees", 0) == 0:
                logger.info(f"No attendees to decrement for property_id={property_id}.")
                return False
            data["attendees"] -= 1
            result = redis_client.set(f"property_id:{property_id}:open_house_info", json.dumps(data))
            logger.info(f"Attendees decremented for property_id={property_id}. New count: {data['attendees']}")
            return bool(result)
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error decrementing attendees: {e}")
            return False
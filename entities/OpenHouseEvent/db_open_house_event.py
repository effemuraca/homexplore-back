import json
from typing import Optional
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from setup.redis_setup.redis_setup import get_redis_client
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class OpenHouseEventDB:
    open_house_event: OpenHouseEvent = None

    def __init__(self, open_house_event: OpenHouseEvent):
        self.open_house_event = open_house_event

    def create_open_house_event(self) -> int:
        if not self.open_house_event:
            logger.error("No open house event to create.")
            return 400
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        data = {
            "day": self.open_house_event.open_house_info.day,
            "start_time": self.open_house_event.open_house_info.start_time,
            "max_attendees": self.open_house_event.open_house_info.max_attendees,
            "attendees": self.open_house_event.open_house_info.attendees
        }
        try:
            result = redis_client.set(f"property_id:{self.open_house_event.property_id}:open_house_info", json.dumps(data))
            # Set expiration based on day and time
            self.open_house_event = OpenHouseEvent(property_id=self.open_house_event.property_id, open_house_info=open_house_info)
            time_sec = self.open_house_event.open_house_info.convert_to_seconds()
            if time_sec and time_sec > 0:
                redis_client.expire(f"property_id:{self.open_house_event.property_id}:open_house_info", time_sec)
                logger.info(f"Set expiration for open house event of property_id={self.open_house_event.property_id} to {time_sec} seconds.")
            else:
                logger.warning(f"Invalid day or time for property_id={self.open_house_event.property_id}. No expiration set.")
                return 400
            logger.info(f"Open house event created for property_id={self.open_house_event.property_id}.")
            if result:
                return 201
            return 500
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during creation: {e}")
            return 500



    def get_open_house_event_by_property(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        raw_data = redis_client.get(f"property_id:{self.open_house_event.property_id}:open_house_info")
        if not raw_data:
            logger.info(f"No open house event found for property_id={self.open_house_event.property_id}.")
            return 404
        try:
            data = json.loads(raw_data)
            open_house_info = OpenHouseInfo(
                day = data.get("day"),
                start_time = data.get("start_time"),
                max_attendees = data.get("max_attendees", 0),
                attendees = data.get("attendees", 0)
            )
            self.open_house_event = OpenHouseEvent(property_id=self.open_house_event.property_id, open_house_info=open_house_info)
            return 200
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error decoding JSON data: {e}")
            return 500
        
    def update_open_house_event(self) -> int:
        redis_client = get_redis_client()
        raw_data = redis_client.get(f"property_id:{self.open_house_event.property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No existing open house event found for property_id={self.open_house_event.property_id} to update.")
            return 404
        try:
            data = json.loads(raw_data)
            if self.open_house_event.open_house_info.day is not None:
                data["day"] = self.open_house_event.open_house_info.day
            if self.open_house_event.open_house_info.start_time is not None:
                data["start_time"] = self.open_house_event.open_house_info.start_time
            if self.open_house_event.open_house_info.max_attendees is not None:
                data["max_attendees"] = self.open_house_event.open_house_info.max_attendees
            if self.open_house_event.open_house_info.attendees is not None:
                data["attendees"] = self.open_house_event.open_house_info.attendees

            result = redis_client.set(f"property_id:{self.open_house_event.property_id}:open_house_info", json.dumps(data))
            self.open_house_event = OpenHouseEvent(property_id=self.open_house_event.property_id, open_house_info=open_house_info)
            logger.info(f"Open house event updated for property_id={self.open_house_event.property_id}.")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error updating open house event: {e}")
            return 500

    def delete_open_house_event_by_property(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        try:
            result = redis_client.delete(f"property_id:{self.open_house_event.property_id}:open_house_info")
            if result:
                logger.info(f"Open house event deleted for property_id={self.open_house_event.property_id}.")
                return 200
            else:
                logger.warning(f"Failed to delete open house event for property_id={self.open_house_event.property_id}.")
                return 404
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error during deletion: {e}")
            return 500

    def increment_attendees(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        raw_data = redis_client.get(f"property_id:{self.open_house_event.property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No open house event found for property_id={self.open_house_event.property_id} to increment attendees.")
            return 404
        try:
            data = json.loads(raw_data)
            if data.get("attendees", 0) >= data.get("max_attendees", 0):
                logger.info(f"Attendees limit reached for property_id={self.open_house_event.property_id}.")
                return 400
            data["attendees"] += 1
            result = redis_client.set(f"property_id:{self.open_house_event.property_id}:open_house_info", json.dumps(data))
            logger.info(f"Attendees incremented for property_id={self.open_house_event.property_id}. New count: {data['attendees']}")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error incrementing attendees: {e}")
            return 500

    def decrement_attendees(self) -> int:
        redis_client = get_redis_client()
        if redis_client is None:
            return 500
        raw_data = redis_client.get(f"property_id:{self.open_house_event.property_id}:open_house_info")
        if not raw_data:
            logger.warning(f"No open house event found for property_id={self.open_house_event.property_id} to decrement attendees.")
            return 404
        try:
            data = json.loads(raw_data)
            if data.get("attendees", 0) == 0:
                logger.info(f"No attendees to decrement for property_id={self.open_house_event.property_id}.")
                return 400
            data["attendees"] -= 1
            result = redis_client.set(f"property_id:{self.open_house_event.property_id}:open_house_info", json.dumps(data))
            logger.info(f"Attendees decremented for property_id={self.open_house_event.property_id}. New count: {data['attendees']}")
            if result:
                return 200
            return 500
        except (json.JSONDecodeError, TypeError, redis.exceptions.RedisError) as e:
            logger.error(f"Error decrementing attendees: {e}")
            return 500
from fastapi import APIRouter, HTTPException
from modules.OpenHouse.models import response_models as ResponseModels
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB
import logging

open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

# Configure the logger
logger = logging.getLogger(__name__)

@open_house_router.get(
    "/open_house_event",
    response_model=OpenHouseEvent,
    responses=ResponseModels.OpenHouseEventResponseModelResponses
)
def get_open_house_event(property_id: int):
    """
    Recupera l'evento open house per un dato property_id.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    result = open_house_db.get_open_house_event_by_property(property_id)
    if not result:
        logger.warning(f"Open house event not found for property_id={property_id}")
        raise HTTPException(status_code=404, detail="Open house event not found")
    return open_house_db.open_house_event

@open_house_router.post(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateOpenHouseEventResponseModelResponses
)
def create_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    """
    Crea un nuovo evento open house per un dato property_id.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    try:
        success = open_house_db.create_open_house_event(property_id, open_house_info)
    except Exception as e:
        logger.error(f"Error creating open house event: {e}")
        raise HTTPException(status_code=500, detail="Error creating open house event")
    if not success:
        logger.error(f"Failed to create open house event for property_id={property_id}")
        raise HTTPException(status_code=500, detail="Error creating open house event")
    logger.info(f"Open house event created successfully for property_id={property_id}")
    return ResponseModels.SuccessModel(detail="Open house event created")

@open_house_router.delete(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteOpenHouseEventResponseModelResponses
)
def delete_open_house_event(property_id: int):
    """
    Elimina l'evento open house per un dato property_id.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    try:
        success = open_house_db.delete_open_house_event_by_property(property_id)
    except Exception as e:
        logger.error(f"Error deleting open house event: {e}")
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    if not success:
        logger.error(f"Failed to delete open house event for property_id={property_id}")
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    logger.info(f"Open house event deleted successfully for property_id={property_id}")
    return ResponseModels.SuccessModel(detail="Open house event deleted")

@open_house_router.put(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateOpenHouseEventResponseModelResponses
)
def update_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    """
    Aggiorna l'evento open house per un dato property_id.
    """
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    try:
        success = open_house_db.update_open_house_event(property_id, open_house_info)
    except Exception as e:
        logger.error(f"Error updating open house event: {e}")
        raise HTTPException(status_code=500, detail="Error updating open house event")
    if not success:
        logger.error(f"Failed to update open house event for property_id={property_id}")
        raise HTTPException(status_code=500, detail="Error updating open house event")
    logger.info(f"Open house event updated successfully for property_id={property_id}")
    return ResponseModels.SuccessModel(detail="Open house event updated")
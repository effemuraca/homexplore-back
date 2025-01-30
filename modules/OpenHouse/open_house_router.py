from fastapi import APIRouter, HTTPException
from modules.OpenHouse.models import response_models as ResponseModels
from modules.OpenHouse.models.open_house_models import CreateOpenHouseEvent, UpdateOpenHouseEvent
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent, OpenHouseInfo
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB
import logging
from fastapi.responses import JSONResponse

open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

# Configure the logger
logger = logging.getLogger(__name__)

@open_house_router.post("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.CreateOpenHouseEventResponseModelResponses) 
def create_open_house_event(open_house_info: CreateOpenHouseEvent):
    open_house_ev = OpenHouseEvent(
        property_id=open_house_info.property_id,
        open_house_info=OpenHouseInfo(
            day=open_house_info.day,
            start_time=open_house_info.start_time,
            max_attendees=open_house_info.max_attendees,
            attendees=0,
            area=open_house_info.area
        )
    )
    open_house_db = OpenHouseEventDB(open_house_ev)
    try:
        status = open_house_db.create_open_house_event()
    except Exception as e:
        logger.error(f"Error creating open house event: {e}")
        raise HTTPException(status_code=500, detail="Error creating open house event")
    if status == 400:
        raise HTTPException(status_code=400, detail="Invalid day or time")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error creating open house event")
    return JSONResponse(status_code=201, content={"detail": "Open house event created"})
    
@open_house_router.get("/open_house_event", response_model=OpenHouseEvent, responses=ResponseModels.GetOpenHouseEventResponseModelResponses)
def get_open_house_event(property_id: str):
    open_house_ev = OpenHouseEvent(property_id=property_id)
    open_house_db = OpenHouseEventDB(open_house_ev)
    try:
        status = open_house_db.get_open_house_event_by_property()
    except Exception as e:
        logger.error(f"Error retrieving open house event: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving open house event")
    if status == 404:
        raise HTTPException(status_code=404, detail="Open house event not found")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error retrieving open house event")
    # Successfully retrieved
    logger.info(f"Open house event retrieved successfully for property_id={property_id}")
    return open_house_db.open_house_event
  

@open_house_router.delete("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeleteOpenHouseEventResponseModelResponses)
def delete_open_house_event(property_id: str):
    open_house_ev = OpenHouseEvent(property_id=property_id)
    open_house_db = OpenHouseEventDB(open_house_ev)
    try:
        status = open_house_db.delete_open_house_event_by_property()
    except Exception as e:
        logger.error(f"Error deleting open house event: {e}")
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    if status == 404:
        raise HTTPException(status_code=404, detail="Open house event not found")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    return ResponseModels.SuccessModel(detail="Open house event deleted")

@open_house_router.put("/open_house_event", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateOpenHouseEventResponseModelResponses)
def update_open_house_event(open_house_info: UpdateOpenHouseEvent):
    open_house_ev = OpenHouseEvent(
        property_id=open_house_info.property_id,
        open_house_info=OpenHouseInfo(
            day=open_house_info.day,
            start_time=open_house_info.start_time,
            max_attendees=open_house_info.max_attendees,
            area=open_house_info.area
        )
    )
    open_house_db = OpenHouseEventDB(open_house_ev)
    try:
        status = open_house_db.update_open_house_event(area=open_house_info.area)
    except Exception as e:
        logger.error(f"Error updating open house event: {e}")
        raise HTTPException(status_code=500, detail="Error updating open house event")
    if status == 404:
        raise HTTPException(status_code=404, detail="Open house event not found")
    if status == 500:
        raise HTTPException(status_code=500, detail="Error updating open house event")
    return ResponseModels.SuccessModel(detail="Open house event updated")

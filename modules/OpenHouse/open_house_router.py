from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from modules.OpenHouse.models import response_models as ResponseModels
from modules.OpenHouse.models.open_house_models import OpenHouseInfo
from entities.OpenHouseEvent.open_house_event import OpenHouseEvent
from entities.OpenHouseEvent.db_open_house_event import OpenHouseEventDB

open_house_router = APIRouter(prefix="/open_house", tags=["open_house"])

@open_house_router.get(
    "/open_house_event",
    response_model=OpenHouseEvent,
    responses=ResponseModels.OpenHouseEventResponseModelResponses
)
def get_open_house_event(property_id: int):
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    result = open_house_db.get_open_house_event_by_property(property_id)
    if not result:
        raise HTTPException(status_code=404, detail="Open house event not found")
    return open_house_db.open_house_event

@open_house_router.post(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.CreateOpenHouseEventResponseModelResponses
)
def create_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    try:
        success = open_house_db.create_open_house_event(property_id, open_house_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating open house event")
    if not success:
        raise HTTPException(status_code=500, detail="Error creating open house event")
    return JSONResponse(status_code=201, content={"detail": "Open house event created"})

@open_house_router.delete(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.DeleteOpenHouseEventResponseModelResponses
)
def delete_open_house_event(property_id: int):
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    success = open_house_db.delete_open_house_event_by_property(property_id)
    if not success:
        raise HTTPException(status_code=500, detail="Error deleting open house event")
    return JSONResponse(status_code=200, content={"detail": "Open house event deleted"})

@open_house_router.put(
    "/open_house_event",
    response_model=ResponseModels.SuccessModel,
    responses=ResponseModels.UpdateOpenHouseEventResponseModelResponses
)
def update_open_house_event(property_id: int, open_house_info: OpenHouseInfo):
    open_house_db = OpenHouseEventDB(OpenHouseEvent())
    try:
        success = open_house_db.update_open_house_event(property_id, open_house_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating open house event")
    if not success:
        raise HTTPException(status_code=500, detail="Error updating open house event")
    return JSONResponse(status_code=200, content={"detail": "Open house event updated"})
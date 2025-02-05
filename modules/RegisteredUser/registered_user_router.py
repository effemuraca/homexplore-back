from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from modules.RegisteredUser.models.registered_user_models import Analytics1Input
from modules.RegisteredUser.models import response_models as ResponseModels

registered_user_router = APIRouter(prefix="/registered-user", tags=["RegisteredUser"])


@registered_user_router.post("/Analytics 1", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics1Responses)
def analytics_1(input : Analytics1Input):
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    try:
        pipeline = [
            {"$match": input.model_dump(exclude_none=True, exclude={"order_by"})},
            {"$project": {"neighbourhood": 1, "price_per_square_meter": {"$divide": ["$price", "$area"]}}},
            {"$group": {"_id": "$neighbourhood", "avg_price": {"$avg": "$price_per_square_meter"}}},
            {"$sort": {"avg_price": input.order_by}}
        ]
        aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response = "No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})

@registered_user_router.post("/Analytics 4", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics4Responses)
def analytics_4(input : str):
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    try:
        pipeline = [
            {"$match": {"city": input}},
            {"$project": {"type": 1, "price": 1}},
            {"$group": {"_id": "$type", "avg_price": {"$avg": "$price"}, "count": {"$sum": 1}}}
        ]
        aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response = "No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})

@registered_user_router.post("/Analytics 5", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics5Responses)
def analytics_5(citta : str, quartiere : str):
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    try:
        pipeline = [
           #numero medio di letti, bagni e metri quadri per ciascun tipo di immobile
            {"$match": {"city": citta, "neighbourhood": quartiere}},
            {"$group": {"_id": "$type", "avg_bed_number": {"$avg": "$bed_number"}, "avg_bath_number": {"$avg": "$bath_number"}, "avg_area": {"$avg": "$area"}}}
        ]
        aggregation_result = mongo_client.PropertyOnSale.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response = "No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})











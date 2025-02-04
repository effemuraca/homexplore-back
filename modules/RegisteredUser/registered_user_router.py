from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from modules.RegisteredUser.models.registered_user_models import Analytics1Input
from modules.RegisteredUser.models import response_models as ResponseModels

registered_user_router = APIRouter(prefix="/registered-user", tags=["RegisteredUser"])


@registered_user_router.get("/Analytics 1", response_model=ResponseModels.Analtyrics1ResponseModel, responses=ResponseModels.Analytics1Responses)
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
    if not aggregation_result:
        response="No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": list(aggregation_result)})










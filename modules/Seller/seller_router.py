from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from entities.MongoDB.Seller.seller import Seller, SoldProperty, SellerPropertyOnSale
from entities.MongoDB.Seller.db_seller import SellerDB
from modules.Seller.models.seller_models import UpdateSeller
from modules.Seller.models import response_models as ResponseModels
from entities.Redis.ReservationsSeller.reservations_seller import ReservationsSeller, ReservationS, next_weekday
from entities.Redis.ReservationsSeller.db_reservations_seller import ReservationsSellerDB
from entities.Redis.ReservationsBuyer.reservations_buyer import ReservationsBuyer, ReservationB
from entities.Redis.ReservationsBuyer.db_reservations_buyer import ReservationsBuyerDB
from entities.MongoDB.PropertyOnSale.property_on_sale import PropertyOnSale
from entities.MongoDB.PropertyOnSale.db_property_on_sale import PropertyOnSaleDB
from modules.Seller.models.seller_models import CreatePropertyOnSale, UpdatePropertyOnSale
from modules.Seller.models.seller_models import Analytics2Input, Analytics3Input
from typing import List, Optional
from bson.objectid import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler
import psutil
from setup.mongo_setup.mongo_setup import get_default_mongo_db
from datetime import datetime, timedelta

from modules.Auth.helpers.auth_helpers import JWTHandler, hash_password
import logging

seller_router = APIRouter(prefix="/seller", tags=["Seller"])

# Configura il logger
logger = logging.getLogger(__name__)

# Avvia scheduler all'avvio dell'applicazione
scheduler = BackgroundScheduler()
scheduler.start()

#Seller

#CONSISTENT
@seller_router.get("/profile_info", response_model=Seller, responses=ResponseModels.GetSellerResponses)
def get_seller(access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    temp_seller = Seller(seller_id=seller_id)
    db_seller = SellerDB(temp_seller)
    response = db_seller.get_profile_info()
    if response == 400:
        raise HTTPException(status_code=400, detail="Invalid seller id")
    if response == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    return db_seller.seller


#CONSISTENT
@seller_router.put("/", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdateSellerResponses)
def update_seller(seller: UpdateSeller, access_token: str = Depends(JWTHandler())):
    """
    Updates an existing seller.
    """
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    seller_old = Seller(seller_id=seller_id)
    seller_db = SellerDB(seller_old)
    
    if seller.email:
        result=seller_db.get_seller_by_email(seller.email)
        if result == 200 and seller_db.seller.seller_id != seller_id:
            raise HTTPException(status_code=400, detail="Email already in use.")
        if result == 500:
            raise HTTPException(status_code=500, detail="Failed to update seller.")
        
    
    # check if there's a password to crypt
    if seller.password:
        seller.password = hash_password(seller.password)
    
    seller_db.seller.seller_id = seller_id
    result = seller_db.update_seller(seller)
    if result == 400:
        raise HTTPException(status_code=result, detail="Seller ID is required.")
    elif result == 404:
        raise HTTPException(status_code=result, detail="Seller not found.")
    elif result == 500:
        raise HTTPException(status_code=result, detail="Failed to update seller.")
    elif result == 200:
        return JSONResponse(status_code=result, content={"detail": "Seller updated successfully."})

#CONSISTENT
@seller_router.get("/properties_on_sale", response_model=List[SellerPropertyOnSale], responses=ResponseModels.GetPropertiesOnSaleResponses)
def get_properties_on_sale(access_token: str = Depends(JWTHandler())):

    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    temp_seller = Seller(seller_id=seller_id)
    db_seller = SellerDB(temp_seller)
    result = db_seller.get_properties_on_sale()
    if result == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    if result== 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve sold properties.")
    return db_seller.seller.properties_on_sale

#CONSISTENT
@seller_router.get("/sold_properties", response_model=List[SoldProperty], responses=ResponseModels.GetSoldPropertiesResponses)
def get_sold_properties(access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    temp_seller = Seller(seller_id=seller_id)
    db_seller = SellerDB(temp_seller)
    result=db_seller.get_sold_properties()
    if result == 404:
        raise HTTPException(status_code=404, detail="Seller not found.")
    if result== 500:
        raise HTTPException(status_code=500, detail="Failed to retrieve sold properties.")
    return db_seller.seller.sold_properties


#CONSISTENT
@seller_router.get("/property_on_sale", response_model=List[SellerPropertyOnSale], responses=ResponseModels.GetPropertiesOnSaleResponses)
def get_property_on_sale_filtered(city: Optional[str] = None, neighbourhood: Optional[str] = None, address: Optional[str] = None, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if not city and not neighbourhood and not address:
        raise HTTPException(status_code=400, detail="City or neighbourhood or address is required.")
    
    temp_seller = Seller(seller_id=seller_id)
    db_seller = SellerDB(temp_seller)
    result = db_seller.get_property_on_sale_filtered(city, neighbourhood, address)
    if result == 404:
        raise HTTPException(status_code=404, detail="No seller found or no property found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch property.")
    return db_seller.seller.properties_on_sale


# Properties on sale

# CONSISTENT
@seller_router.post("/property_on_sale", response_model=ResponseModels.CreatePropertyOnSaleResponseModel, responses=ResponseModels.CreatePropertyOnSaleResponses)
def create_property_on_sale(input_property_on_sale: CreatePropertyOnSale, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    #insert the property on the property_on_sale collection
    property_on_sale = PropertyOnSale(**input_property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.create_property_on_sale()
    if response == 400:
        raise HTTPException(status_code=response, detail="Data required.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Failed to create property.")
    
    #insert the property on the seller collection
    seller= Seller(seller_id=seller_id)
    seller_db= SellerDB(seller)
    embedded_property_on_sale = SellerPropertyOnSale(**input_property_on_sale.model_dump(exclude={"type", "area", "bed_number", "bath_number", "description", "photos"}))
    embedded_property_on_sale.property_on_sale_id=db_property_on_sale.property_on_sale.property_on_sale_id
    response=seller_db.insert_property_on_sale(embedded_property_on_sale)
    if response != 200: 
        if response == 500:
            detail="Failed to create property."
        else:
            detail="Seller not found."
        #rollback
        response=db_property_on_sale.delete_property_on_sale_by_id(db_property_on_sale.property_on_sale.property_on_sale_id)
        if response==200:
            logging.error("Rollback successed.")
        else:
            logging.error("Rollback failed.")
        raise HTTPException(status_code=500, detail=detail)
    return JSONResponse(status_code=201, content={"detail": "Property created successfully.", "property_id": db_property_on_sale.property_on_sale.property_on_sale_id})


# Function to check and update the reservations when the load is low
def check_and_update_when_low_load(not_updated_ids: list, property_id: str, disponibility, address):
    # psutil.cpu_percent() checks the current CPU load
    current_load = psutil.cpu_percent(interval=1)
    logger.info(f"Actual load of the CPU: {current_load}%")
    if current_load < 30:
        # if the load is low, update the reservations
        for buyer_id in not_updated_ids:
            reservation_buyer = ReservationsBuyer(buyer_id=buyer_id)
            reservation_buyer_db = ReservationsBuyerDB(reservation_buyer)
            status = reservation_buyer_db.get_reservations_by_user()
            if status != 200:
                logger.error(f"Retry: impossibile to retrieve the buyer reservation {buyer_id}.")
                continue
            for reservation in reservation_buyer_db.reservations_buyer.reservations:
                if reservation.property_on_sale_id == property_id:
                    if disponibility is not None:
                        reservation.date = next_weekday(disponibility.day)
                        reservation.time = disponibility.time
                    if address is not None:
                        reservation.address = address
            status = reservation_buyer_db.update_reservation_buyer()
            # if the update do not fail, remove the buyer_id from the list
            if status == 200:
                not_updated_ids.remove(buyer_id)

        if not_updated_ids:
            logger.info(f"Retry: some reservations could not be updated: {not_updated_ids}.")
            # if there are still reservations to update, re-schedule the update
            next_run = datetime.now() + timedelta(minutes=5)
            scheduler.add_job(
                check_and_update_when_low_load,
                'date',
                run_date=next_run,
                args=[not_updated_ids, property_id, disponibility, address]
            )
            logger.info(f"Retry: job re-scheduled for {next_run}.")

    else:
        # if the load is still high, re-schedule the update
        next_run = datetime.now() + timedelta(minutes=5)
        scheduler.add_job(
            check_and_update_when_low_load,
            'date',
            run_date=next_run,
            args=[not_updated_ids, property_id, disponibility, address]
        )
        logger.info(f"Load too high ({current_load}%). Reschedule the job for {next_run}.")

# Function to check and delete the reservations when the load is low
def check_and_delete_when_low_load(not_deleted_ids: list, property_id: str):
    # psutil.cpu_percent() checks the current CPU load
    current_load = psutil.cpu_percent(interval=1)
    logger.info(f"Actual load of the CPU: {current_load}%")
    if current_load < 30:
        # if the load is low, update the reservations
        for buyer_id in not_deleted_ids:
            reservation_buyer = ReservationsBuyer(buyer_id=buyer_id)
            reservation_buyer_db = ReservationsBuyerDB(reservation_buyer)
            status = reservation_buyer_db.get_reservations_by_user()
            if status != 200:
                logger.error(f"Retry: impossibile to retrieve the buyer reservation {buyer_id}.")
                continue
            status = reservation_buyer_db.delete_reservation_by_property_on_sale_id(property_id)    
            # if the delete do not fail, remove the buyer_id from the list
            if status == 200:
                not_deleted_ids.remove(buyer_id)

        if not_deleted_ids:
            logger.info(f"Retry: some reservations could not be updated: {not_deleted_ids}.")
            # if there are still reservations to delete, re-schedule the delete
            next_run = datetime.now() + timedelta(minutes=5)
            scheduler.add_job(
                check_and_delete_when_low_load,
                'date',
                run_date=next_run,
                args=[not_deleted_ids, property_id]
            )
            logger.info(f"Retry: job re-scheduled for {next_run}.")
    else:
        # if the load is still high, re-schedule the delete
        next_run = datetime.now() + timedelta(minutes=5)
        scheduler.add_job(
            check_and_delete_when_low_load,
            'date',
            run_date=next_run,
            args=[not_deleted_ids, property_id]
        )
        logger.info(f"Load too high ({current_load}%). Reschedule the job for {next_run}.")

#CONSISTENT
@seller_router.put("/property_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.UpdatePropertyOnSaleResponses)
def update_property_on_sale(input_property_on_sale: UpdatePropertyOnSale, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    #update on the seller collection
    seller= Seller(seller_id=seller_id)
    db_seller= SellerDB(seller)
    embedded_property_on_sale = SellerPropertyOnSale(**input_property_on_sale.model_dump(exclude={"type", "area", "bed_number", "bath_number", "description", "photos"}))
    response=db_seller.update_property_on_sale(embedded_property_on_sale)
    if response == 404:
        detail="Seller not found or property not found in the properties_on_sale of seller collection."
    if response == 500:
        detail="Failed to update property."
    if response != 200:
        raise HTTPException(status_code=response, detail=detail)
    
    #update on the property_on_sale collection
    property_on_sale = PropertyOnSale(**input_property_on_sale.model_dump())
    db_property_on_sale = PropertyOnSaleDB(property_on_sale)
    response = db_property_on_sale.update_property_on_sale()
    if response == 404:
        logging.error("Missing property on property_on_sale collection, inconistencies in the database before operation, rollback impossible.")
        raise HTTPException(status_code=response, detail="Property not found in property_on_sale collection.")
    if response == 500:
        #rollback
        response=db_property_on_sale.get_property_on_sale_by_id(property_on_sale.property_on_sale_id)
        if response != 200:
            logging.error("Rollback failed.")
        else:
            embedded_property_on_sale = SellerPropertyOnSale(db_property_on_sale.property_on_sale)
            response=db_seller.update_property_on_sale(embedded_property_on_sale)
            if response != 200:
                logging.error("Rollback failed.")
            else:
                logging.error("Rollback successed.")
        raise HTTPException(status_code=response, detail="Failed to update property.")
    
    # handling redis part of the update
    if input_property_on_sale.disponibility is None or input_property_on_sale.address is None:
        # if input_property_on_sale.disponibility is None and input_property_on_sale.address is None, nothing to update in the reservations
        return JSONResponse(status_code=200, content={"detail": "Property updated successfully."})
    
    reservation_seller = ReservationsSeller(property_on_sale_id=input_property_on_sale.property_on_sale_id)
    reservation_seller_db = ReservationsSellerDB(reservation_seller)

    # get the reservations for the property
    status = reservation_seller_db.get_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch reservations.")


     # if disponibility has changed, update the ttl in the reservations seller
    if input_property_on_sale.disponibility is not None:
        status = reservation_seller_db.update_day_and_time(input_property_on_sale.disponibility.day, input_property_on_sale.disponibility.time)
        if status == 500:
            raise HTTPException(status_code=500, detail="Failed to update disponibility.")
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found.")

    # save all the buyer_ids of the reservations
    buyer_ids = [reservation.buyer_id for reservation in reservation_seller_db.reservations_seller.reservations]

    # for each reservation buyer, update the disponibility and address
    not_updated_ids = []
    for buyer_id in buyer_ids.copy():
        reservation_buyer = ReservationsBuyer(buyer_id=buyer_id)
        reservation_buyer_db = ReservationsBuyerDB(reservation_buyer)
        status = reservation_buyer_db.get_reservations_by_user()
        if status == 404:
            raise HTTPException(status_code=404, detail="No reservations found.")
        if status == 500:
            raise HTTPException(status_code=500, detail="Failed to fetch reservations.")
        for reservation in reservation_buyer_db.reservations_buyer.reservations:
            if reservation.property_on_sale_id == input_property_on_sale.property_on_sale_id:
                if input_property_on_sale.disponibility is not None:
                    reservation.date = next_weekday(input_property_on_sale.disponibility.day)
                    reservation.time = input_property_on_sale.disponibility.time
                if input_property_on_sale.address is not None:
                    reservation.address = input_property_on_sale.address
        status = reservation_buyer_db.update_reservation_buyer()
        # if the update do not fail, remove the buyer_id from the list
        if status == 200:
            buyer_ids.remove(buyer_id)
        else: 
            not_updated_ids.append(buyer_id)            
            
    if not_updated_ids:
            run_date = datetime.now() + timedelta(minutes=5)
            scheduler.add_job(
                check_and_update_when_low_load,
                'date',
                run_date=run_date,
                args=[not_updated_ids, input_property_on_sale.property_on_sale_id, input_property_on_sale.disponibility, input_property_on_sale.address]
            )
            logger.info(f"Update scheduled for {run_date} for some reservations that could not be updated.")
            
    return JSONResponse(status_code=200, content={"detail": "Property updated successfully."})

# Function to handle the reservations when a property is sold or deleted
def handleReservations(property_id: str) -> int:
    reservation_seller = ReservationsSeller(property_on_sale_id=property_id)
    reservation_seller_db = ReservationsSellerDB(reservation_seller)
    status = reservation_seller_db.get_reservation_seller()
    if status == 404:
        return 404
    if status == 500:
        return 500
    buyer_ids = [reservation.buyer_id for reservation in reservation_seller_db.reservations_seller.reservations]

    not_deleted_ids = []
    for buyer_id in buyer_ids:
        reservation_buyer = ReservationsBuyer(buyer_id=buyer_id)
        reservation_buyer_db = ReservationsBuyerDB(reservation_buyer)
        status = reservation_buyer_db.delete_reservation_by_property_on_sale_id(property_id)
        if status == 200:
            buyer_ids.remove(buyer_id)
        else: 
            not_deleted_ids.append(buyer_id)   

    if not_deleted_ids:
        run_date = datetime.now() + timedelta(minutes=5)
        scheduler.add_job(
            check_and_delete_when_low_load,
            'date',
            run_date=run_date,
            args=[not_deleted_ids, property_id]
        )
        logger.info(f"Delete scheduled for {run_date} for some reservations that could not be deleted.")
    return 200

#CONSISTENT 
@seller_router.post("/sell_property_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.SellPropertyOnSaleResponses)
def sell_property(property_to_sell_id: str, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if ObjectId.is_valid(property_to_sell_id) is False:
        raise HTTPException(status_code=400, detail="Invalid property id.")
    
    #check if property belongs to the seller
    seller= Seller(seller_id=seller_id)
    db_seller = SellerDB(seller)
    response=db_seller.check_property_on_sale(property_to_sell_id)
    if response == 404:
        raise HTTPException(status_code=404, detail="Property not found or seller not found.")
    if response == 500:
        raise HTTPException(status_code=500, detail="Failed to sell property.")

    #retrive info about the property to sell
    property_to_sell=PropertyOnSale(property_on_sale_id=property_to_sell_id)
    db_property_on_sale=PropertyOnSaleDB(property_to_sell)
    result=db_property_on_sale.delete_and_return_property(property_to_sell_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Property not found.")
    if result == 500:
        raise HTTPException(status_code=500, detail="Failed to sell property.")
    
    #move the property from properties_on_sale to sold_properties
    embedded_sold_property = SoldProperty(sell_date=datetime.now(),sold_property_id=property_to_sell.property_on_sale_id,**db_property_on_sale.property_on_sale.model_dump(include={"city", "neighbourhood", "price", "thumbnail", "type", "area", "registration_date"}))
    result = db_seller.sell_property(embedded_sold_property)
    if result != 200:
        if result == 500:
            detail="Failed to sell property."
        if result == 404:
            detail="Seller not found or property not found in the seller collection."
        #rollback
        result=db_property_on_sale.insert_property()
        if result != 200:
            logging.error("Rollback failed.")
        else:
            logging.error("Rollback successed.")
        raise HTTPException(status_code=500, detail=detail)

    
    # call a function that handles the reservations
    status = handleReservations(property_to_sell_id)
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to handle reservations.")
    return JSONResponse(status_code=200, content={"detail": "Property sold successfully."})
    
    
#CONSISTENT
@seller_router.delete("/property_on_sale", response_model=ResponseModels.SuccessModel, responses=ResponseModels.DeletePropertyOnSaleResponses)
def delete_property_on_sale(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if ObjectId.is_valid(property_on_sale_id) is False:
        raise HTTPException(status_code=400, detail="Invalid property id.")
    
    if ObjectId.is_valid(property_on_sale_id) is False:
        raise HTTPException(status_code=400, detail="Invalid property id.")
    
    #delete the property from the seller collection
    seller= Seller(seller_id=seller_id)
    db_seller= SellerDB(seller)
    response=db_seller.delete_embedded(property_on_sale_id)
    if response == 404:
        raise HTTPException(status_code=response, detail="Property not found or seller not found.")
    if response == 500:
        raise HTTPException(status_code=response, detail="Failed to delete property.")
    
    #delete the property from the property_on_sale collection
    db_property_on_sale = PropertyOnSaleDB(PropertyOnSale())
    response = db_property_on_sale.delete_property_on_sale_by_id(property_on_sale_id)
    if response == 404:
        #rollback impossible
        logger.error("Privious state of the database is inconsistent, rollback impossible, property eliminated from all the collections.")
        raise HTTPException(status_code=response, detail="Property not found.")
    if response == 500:
        #rollback
        logger.error("Failed to delete property from the property_on_sale collection.")
        response=db_property_on_sale.get_property_on_sale_by_id(property_on_sale_id)
        if response != 200:
            logger.error("Rollback failed.")
        else:
            embedded_property_on_sale = SellerPropertyOnSale(db_property_on_sale.property_on_sale)
            response=db_seller.insert_property_on_sale(embedded_property_on_sale)
            if response != 200:
                logger.error("Rollback failed.")
            else:
                logger.error("Rollback successed.")
        raise HTTPException(status_code=response, detail="Failed to delete property.")
    
    # call a function that handles the reservations
    status = handleReservations(property_on_sale_id)
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to handle reservations.")
    return JSONResponse(status_code=200, content={"detail": "Property deleted successfully."})

# ReservationsSeller

@seller_router.get(
    "/reservations",
    response_model=ReservationsSeller,
    responses=ResponseModels.GetReservationsSellerResponseModelResponses
)
def get_reservations_seller(property_on_sale_id: str, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if not property_on_sale_id:
        raise HTTPException(status_code=400, detail="Property on sale ID is required.")
    reservations_seller = ReservationsSeller(property_on_sale_id=property_on_sale_id)
    reservations_seller_db = ReservationsSellerDB(reservations_seller)
    status = reservations_seller_db.get_reservation_seller()
    if status == 404:
        raise HTTPException(status_code=404, detail="No reservations found.")
    if status == 500:
        raise HTTPException(status_code=500, detail="Failed to fetch reservations.")
    return reservations_seller_db.reservations_seller

# Analytics routes

#CONSISTENT
@seller_router.post("/Analytics/Analytics 2", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics2Responses)
def analytics_2(input : Analytics2Input, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    
    #convert input dates into datetime objects
    start = datetime.strptime(input.start_date, "%Y-%m-%d")
    end = datetime.strptime(input.end_date, "%Y-%m-%d")

    #check if the start date is before the end date
    if start > end:
        raise HTTPException(status_code=404, detail="Start date must be before end date")
    pipeline = [
            {
                "$match": {
                    "_id": ObjectId(seller_id),
                }
            },
            {"$unwind": "$sold_properties"},
            {
                "$match": {
                    "sold_properties.city": input.city,
                    "sold_properties.sell_date": {"$gte": start,"$lte": end}
                }
            },
            {
                "$group": {
                    "_id": "$sold_properties.neighbourhood",
                    "houses_sold": {"$sum": 1},
                    "revenue": {"$sum": "$sold_properties.price"}
                }
            },
            {
                "$project": {
                    "neighbourhood": "$_id",
                    "houses_sold": 1,
                    "revenue": 1,
                    "_id": 0
                }
            }
        ]
    try:
        aggregation_result = mongo_client.Seller.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response="No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})


#CONSISTENT
@seller_router.post("/Analytics/Analytics 3", response_model=ResponseModels.AnalyticsResponseModel, responses=ResponseModels.Analytics3Responses)
def analytics_3(input : Analytics3Input, access_token: str = Depends(JWTHandler())):
    seller_id, user_type = JWTHandler.verifyAccessToken(access_token)
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    if user_type != "seller":
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    mongo_client = get_default_mongo_db()
    if mongo_client is None:
        raise HTTPException(status_code=500, detail="Database client not found")
    start=datetime.strptime(input.start_date, "%Y-%m-%d")
    pipeline = [
            {"$match": {"_id": ObjectId(seller_id)}},
            {"$unwind": "$sold_properties"},
            {"$match": {"sold_properties.city": input.city, "sold_properties.registration_date": {"$gte": start}}},
            {"$project": {
                "time_to_sell": {
                    "$divide": [{"$subtract": ["$sold_properties.sell_date", "$sold_properties.registration_date"]},86400000 ]
                },
                "sold_properties.neighbourhood": 1
            }
            },
            {
            "$group": {
                "_id": "$sold_properties.neighbourhood",
                "avg_time_to_sell": {"$avg": "$time_to_sell"},
                "num_house": {"$sum": 1}
            }    
            },
            {
                "$project": {
                    "neighbourhood": "$_id",
                    "avg_time_to_sell": 1,
                    "num_house": 1,
                    "_id": 0
                }
            }
        ]
    try:
        aggregation_result = mongo_client.Seller.aggregate(pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    aggregation_result = list(aggregation_result)
    if not aggregation_result:
        response="No data found"
    else:
        response="Aggregated data finished successfully"
    return JSONResponse(status_code=200,content={"detail": response, "result": aggregation_result})



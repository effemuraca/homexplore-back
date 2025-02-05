from pydantic import BaseModel, Field, validator, field_validator, EmailStr
from bson import ObjectId 
from typing import Optional, List
import re
from datetime import datetime

# Seller
# class CreateSeller(BaseModel):
#     agency_name: str = Field(example="Agency Name")
#     email: str = Field(example="email@example.com")
#     password: str = Field(example="password123")
#     phone_number: str = Field(example="+38 1234567890")

class UpdateSeller(BaseModel):
    seller_id: str = Field(..., example="5f4f4f4f4f4f4f4f4f4f4f4f")
    agency_name: Optional[str] = Field(None, example="Agency Name")
    email: Optional[str] = Field(None, example="email@example.com")
    password: Optional[str] = Field(None, example="password123")
    phone_number: Optional[str] = Field(None, example="+38 1234567890")
    
    @validator("email")
    def validate_email(cls, value):
        email_pattern = re.compile(
            r"^(?!\.)(""([^""\r\\]|\\[""\r\\])*""|"
            r"([-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+(?:\.[-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+)*)"
            r")@((?:[A-Z0-9-]+\.)+[A-Z]{2,})$", re.IGNORECASE)
        if not email_pattern.match(value):
            raise ValueError("Invalid email format. Expected format: email@example.com")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value

# ReservationsSeller
class CreateReservationSeller(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    buyer_id: Optional[str] = Field(None, example="615c44fdf641be001f0c1111")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")
    day: str = Field(..., example="Monday")
    time: str = Field(..., example="12:00 PM")
    max_reservations: int = Field(..., example=5)
    
    @field_validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value
    
    @field_validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM AM/PM")
        return value
    
    @field_validator("max_reservations")
    def validate_max_reservations(cls, value):
        if value < 1 and value > 1000:
            raise ValueError("max_reservations must be greater than 0 and less than 1000")
        return value

    @field_validator("email")
    def validate_email(cls, value):
        email_pattern = re.compile(
            r"^(?!\.)(""([^""\r\\]|\\[""\r\\])*""|"
            r"([-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+(?:\.[-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+)*)"
            r")@((?:[A-Z0-9-]+\.)+[A-Z]{2,})$", re.IGNORECASE)
        if not email_pattern.match(value):
            raise ValueError("Invalid email format. Expected format: mail@example.com")
        return value
    
    @field_validator("phone")
    def validate_phone(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value
    
    @field_validator("property_on_sale_id")
    def validate_property_on_sale_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid property_on_sale_id")
        return value
    
    @field_validator("buyer_id")
    def validate_buyer_id(cls, value):
        if value and not ObjectId.is_valid(value):
            raise ValueError("Invalid buyer_id")
        return value
                                     
class UpdateReservationSeller(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    buyer_id: Optional[str] = Field(None, example="615c44fdf641be001f0c1111")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[str] = Field(None, example="john@example.com")
    phone: Optional[str] = Field(None, example="1234567890")
    

    @field_validator("email")
    def validate_email(cls, value):
        email_pattern = re.compile(
            r"^(?!\.)(""([^""\r\\]|\\[""\r\\])*""|"
            r"([-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+(?:\.[-!#\$%&'\*\+/=\?\^`\{\}\|~\w]+)*)"
            r")@((?:[A-Z0-9-]+\.)+[A-Z]{2,})$", re.IGNORECASE)
        if not email_pattern.match(value):
            raise ValueError("Invalid email format. Expected format: mail@example.com")
        return value
    
    @field_validator("phone")
    def validate_phone(cls, value):
        phone_pattern = re.compile(r"^\+\d{2} \d{10}$")
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format. Expected format: +xx xxxxxxxxxx")
        return value
    
    @field_validator("property_on_sale_id")
    def validate_property_on_sale_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid property_on_sale_id")
        return value
    
    @field_validator("buyer_id")
    def validate_buyer_id(cls, value):
        if value and not ObjectId.is_valid(value):
            raise ValueError("Invalid buyer_id")
        return value
    
class UpdateReservationSellerDateAndTime(BaseModel):
    property_on_sale_id: str = Field(..., example="615c44fdf641be001f0c1111")
    day: str = Field(..., example="Monday")
    time: str = Field(..., example="12:00 PM")

    @field_validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value
    
    @field_validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM AM/PM")
        return value


# PropertyOnSale
class CreateDisponibility(BaseModel):
    day: str = Field(example="Monday")
    time: str = Field(example="10:00-11:00 AM")
    max_attendees: int = Field(example=5)

    @validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM-HH:MM AM/PM")
        return value

class CreatePropertyOnSale(BaseModel):
    city: str = Field(example="New York")
    neighbourhood: str = Field(example="Bronx")
    address: str = Field(example="123 Main St")
    price: int = Field(example=270000)
    thumbnail: str = Field(example="http://example.com/photo.jpg")
    type: str = Field(example="condo")
    area: int = Field(example=100)
    bed_number: Optional[int] = Field(None, example=3) 
    bath_number: Optional[int] = Field(None, example=2) 
    description: Optional[str] = Field(None, example="Beautiful home") 
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) 
    disponibility: Optional[CreateDisponibility] = None   

class UpdateDisponibility(BaseModel):
    day: Optional[str] = Field(None, example="Monday")
    time: Optional[str] = Field(None, example="10:00-11:00 AM")
    max_attendees: Optional[int] = Field(None, example=5)

    @validator("day")
    def validate_day(cls, value):
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        if value not in valid_days:
            raise ValueError("Invalid day. Must be one of: " + ", ".join(valid_days))
        return value

    @validator("time")
    def validate_time(cls, value):
        time_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not time_pattern.match(value):
            raise ValueError("Invalid time format. Expected format: HH:MM-HH:MM AM/PM")
        return value

class UpdatePropertyOnSale(BaseModel):
    property_on_sale_id: str = Field(None, example="5f4f4f4f4f4f4f4f4f4f4f4f")
    city: Optional[str] = Field(None, example="New York")
    neighbourhood: Optional[str] = Field(None, example="Bronx")
    address: Optional[str] = Field(None, example="123 Main St")
    price: Optional[int] = Field(None, example=270000)
    thumbnail: Optional[str] = Field(None, example="http://example.com/photo.jpg")
    type: Optional[str] = Field(None, example="condo")
    area: Optional[int] = Field(None, example=100)
    bed_number: Optional[int] = Field(None, example=3) 
    bath_number: Optional[int] = Field(None, example=2) 
    description: Optional[str] = Field(None, example="Beautiful home") 
    photos: Optional[List[str]] = Field(None, example=["http://example.com/photo1.jpg"]) 
    disponibility: Optional[UpdateDisponibility] = None   

class FilteredSearchPropertyOnSale(BaseModel):
    city: Optional[str] = Field(None, example="New York")
    max_price: Optional[int] = Field(None, example=500000)
    neighbourhood: Optional[str] = Field(None, example="Brooklyn")
    type: Optional[str] = Field(None, example="House")
    area: Optional[int] = Field(None, example=2000)
    min_bed_number: Optional[int] = Field(None, example=3)
    min_bath_number: Optional[int] = Field(None, example=2)


# Analytics

class AnalyticsResponseModel(BaseModel):
    detail: str
    result: List[dict]

class Analytics2Input(BaseModel):
    agency_id: str = Field(example="5f4f4f4f4f4f4f4f4f4f4f4f")
    city: str = Field(example="New York")
    start_date: str = Field(example="2021-01-01")
    end_date: str = Field(example="2021-12-31")

    #create validator for date
    @validator("start_date")
    def validate_start_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
    @validator("end_date")
    def validate_end_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
class Analytics3Input(BaseModel):
    agency_id: str = Field(example="5f4f4f4f4f4f4f4f4f4f4f4f")
    city: str = Field(example="New York")
    start_date: str = Field(example="2021-01-01")

    #create validator for date
    @validator("start_date")
    def validate_start_date(cls, value):
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(value):
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value
    
    #check if agency is a valid ObjectId
    @validator("agency_id")
    def validate_agency(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid agency_id")
        return value
    
class Analytics6Input(BaseModel):
    agency_id: str = Field(example="5f4f4f4f4f4f4f4f4f4f4f4f")
    city: str = Field(example="New York")
    start_houre: str = Field(example="10:00 AM")
    end_houre: str = Field(example="12:00 PM")

    #create validator for houre
    @validator("start_houre")
    def validate_start_houre(cls, value):
        houre_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not houre_pattern.match(value):
            raise ValueError("Invalid houre format. Expected format: HH:MM AM/PM")
        return value
    
    @validator("end_houre")
    def validate_end_houre(cls, value, values):
        houre_pattern = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$")
        if not houre_pattern.match(value):
            raise ValueError("Invalid houre format. Expected format: HH:MM AM/PM")
        start_time = datetime.strptime(values["start_houre"], "%I:%M %p")
        end_time = datetime.strptime(value, "%I:%M %p")
        if start_time >= end_time:
            raise ValueError("end_houre must be after start_houre")
        return value
    

   
    
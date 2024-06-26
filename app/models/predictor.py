from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from app.utils.helpers import get_uuid4, get_utc_timestamp
from .enums import ResultClasses
from fastapi import UploadFile


class ImageData(BaseModel):
    id: str
    image: UploadFile



class PredictionRequest(BaseModel):
    uid : str  = Field(default_factory=get_uuid4)
    created_at : str = Field(default_factory= get_utc_timestamp, alias  = "createdAt")
    result_id :  str | None = Field(default= None,alias="resultId")
    image_count :  int  = Field( ge = 1, alias = "imageCount")
    

    model_config = SettingsConfigDict(populate_by_name=True)


class ResultItem(BaseModel):
    id :  str 
    label_class :  ResultClasses = Field(alias = "labelClass")

    model_config = SettingsConfigDict(populate_by_name=True)


class PredictionResult(BaseModel):
    uid : str  = Field(default_factory=get_uuid4)
    created_at : str = Field(default_factory= get_utc_timestamp, alias  = "createdAt")
    request_id :  str = Field(alias="requestId")
    classes : list[ResultItem] 

    model_config = SettingsConfigDict(populate_by_name=True)


from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from app.utils.helpers import get_uuid4, get_utc_timestamp
from .enums import LabelClasses
from fastapi import UploadFile


class ImageData(BaseModel):
    id: str
    image: UploadFile



class PredictionRequest(BaseModel):
    uid : str  = Field(default_factory=get_uuid4)
    image_id :  str = Field(min_length=1, alias="imageId")
    created_at : str = Field(default_factory= get_utc_timestamp, alias  = "createdAt")
    result_id :  str | None = Field(default= None,alias="resultId")

    model_config = SettingsConfigDict(populate_by_name=True)


class ResultItem(BaseModel):
    image_id :  str   = Field(alias = "imageId")
    label_class :  LabelClasses = Field(alias = "labelClass")

    model_config = SettingsConfigDict(populate_by_name=True)


class PredictionResult(BaseModel):
    uid : str  = Field(default_factory=get_uuid4)
    created_at : str = Field(default_factory= get_utc_timestamp, alias  = "createdAt")
    prediction_request_id :  str = Field(alias="PredictionrequestId")
    result : ResultItem 

    model_config = SettingsConfigDict(populate_by_name=True)


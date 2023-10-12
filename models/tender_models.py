from typing import List, Optional

from pydantic import BaseModel, Field

from models.tenders_list_models import BaseTender


class FileBase(BaseModel):
    name: str


class HeaderInfo(BaseModel):
    address: str


class AttachedImage(BaseModel):
    tender_id: int = Field(..., alias='tenderId')
    is_main_photo: bool = Field(..., alias='isMainPhoto')
    url: str
    file_base: FileBase = Field(..., alias='fileBase')


class ImageInfo(BaseModel):
    attached_images: List[AttachedImage] = Field(..., alias='attachedImages')


class ObjectInfoItem(BaseModel):
    label: str
    value: str


class ProcedureInfoItem(BaseModel):
    label: str
    value: Optional[str] = Field(None, alias='value')
    user_action: Optional[str] = Field(None, alias='userAction')


class Tender(BaseTender):
    image_info: Optional[ImageInfo] = Field(None, alias='imageInfo')
    header_info: Optional[HeaderInfo] = Field(None, alias='headerInfo')
    object_info: Optional[List[ObjectInfoItem]] = Field(None, alias='objectInfo')
    procedure_info: Optional[List[ProcedureInfoItem]] = Field(
        None, alias='procedureInfo'
    )


class AttachedImageSnakeCase(BaseModel):
    tender_id: int = Field(..., alias='tender_id')
    is_main_photo: bool = Field(..., alias='is_main_photo')
    url: str
    file_base: FileBase = Field(..., alias='file_base')


class TenderImagesInfo(BaseModel):
    tender_id: int = Field(..., alias='tender_id')
    attached_images: List[AttachedImageSnakeCase] = Field(..., alias='attached_images')


class TenderImages(BaseModel):
    images: List[TenderImagesInfo]
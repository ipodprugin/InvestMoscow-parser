from typing import List, Optional
from pydantic import BaseModel, Field


class SubwayStation(BaseModel):
    subway_station_id: int = Field(..., alias='subwayStationId')
    subway_station_name: str = Field(..., alias='subwayStationName')
    walking_time: int = Field(..., alias='walkingTime')
    public_transport_time: int = Field(..., alias='publicTransportTime')
    distance_to_object: float = Field(..., alias='distanceToObject')


class FileBase(BaseModel):
    file_hash: str = Field(..., alias='hash')
    file_extension: str = Field(..., alias='fileExtension')
    name: str


class AttachedPic(BaseModel):
    tender_id: int = Field(..., alias='tenderId')
    is_main_photo: bool = Field(..., alias='isMainPhoto')
    url: str
    image_description: str = Field(..., alias='imageDescription')
    file_base: FileBase = Field(..., alias='fileBase')


class BaseTender(BaseModel):
    id: Optional[int] = None
    # name: Optional[str] = None
    url: Optional[str] = None
    # subway_stations: Optional[List[SubwayStation]] = Field(None, alias='subwayStations')
    # object_type_id: Optional[int] = Field(None, alias='objectTypeId')
    # object_type_name: Optional[str] = Field(None, alias='objectTypeName')
    # object_type_code: Optional[str] = Field(None, alias='objectTypeCode')
    # type_id: Optional[int] = Field(None, alias='typeId')
    # type_code: Optional[str] = Field(None, alias='typeCode')
    # functionality_purposes_dou_tree_ids: Optional[List[int]] = Field(
    #     None, alias='functionalityPurposesDouTreeIds'
    # )
    # functionality_purposes: Optional[List[str]] = Field(
    #     None, alias='functionalityPurposes'
    # )
    # functionality_purpose_codes: Optional[List[str]] = Field(
    #     None, alias='functionalityPurposeCodes'
    # )
    # functionality_purposes_ids: Optional[List[int]] = Field(
    #     None, alias='functionalityPurposesIds'
    # )
    # price_per_square: Optional[float] = Field(None, alias='pricePerSquare')
    region_name: Optional[str] = Field(None, alias='regionName')
    district_name: Optional[str] = Field(None, alias='districtName')
    # address: Optional[str] = None
    # short_address: Optional[str] = Field(None, alias='shortAddress')
    object_area: Optional[float] = Field(None, alias='objectArea')
    start_price: Optional[float] = Field(None, alias='startPrice')
    # request_start_date: Optional[str] = Field(None, alias='requestStartDate')
    request_end_date: Optional[str] = Field(None, alias='requestEndDate')
    # tender_date: Optional[str] = Field(None, alias='tenderDate')
    # attached_pics: Optional[List[AttachedPic]] = Field(None, alias='attachedPics')
    # in_user_favorite: Optional[bool] = Field(None, alias='inUserFavorite')
    # in_user_compare: Optional[bool] = Field(None, alias='inUserCompare')
    # coords: Optional[str] = None
    # district_id: Optional[int] = Field(None, alias='districtId')
    # region_id: Optional[int] = Field(None, alias='regionId')
    # trade_form_id: Optional[int] = Field(None, alias='tradeFormId')
    # trade_form_code: Optional[str] = Field(None, alias='tradeFormCode')
    # program_id: Optional[int] = Field(None, alias='programId')
    # program_code: Optional[str] = Field(None, alias='programCode')
    # functionality_purpose_id: Optional[int] = Field(
    #     None, alias='functionalityPurposeId'
    # )
    # platform_link: Optional[str] = Field(None, alias='platformLink')
    # is_smp: Optional[bool] = Field(None, alias='isSmp')
    # update_date: Optional[str] = Field(None, alias='updateDate')
    # invest_object_id: Optional[int] = Field(None, alias='investObjectId')
    # room_floors: Optional[List[int]] = Field(None, alias='roomFloors')
    # floors: Optional[int] = None
    # count_of_room_codes: Optional[List] = Field(None, alias='countOfRoomCodes')
    # entrance_type_codes: Optional[List[str]] = Field(None, alias='entranceTypeCodes')
    # room_floors_codes: Optional[List[str]] = Field(None, alias='roomFloorsCodes')
    # create_date: Optional[str] = Field(None, alias='createDate')
    # is_io_area_in_hectars: Optional[bool] = Field(None, alias='isIoAreaInHectars')
    # unom: Optional[int] = None
    # portal_views: Optional[int] = Field(None, alias='portalViews')
    # object_address: Optional[str] = Field(None, alias='objectAddress')
    # engine: Optional[str] = None

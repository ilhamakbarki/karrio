from attr import s
from typing import Optional, Any, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class TrackingInfoType:
    status_code: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    created_at: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    reference: Optional[int] = None
    tracking_number: Optional[int] = None
    customer_tracking: Any = None
    customer_name: Optional[str] = None
    requested_by: Optional[str] = None
    cod_amount: Optional[str] = None
    declared_value: Any = None
    declared_value_currency: Any = None
    currency: Optional[str] = None
    delivery_name: Optional[str] = None
    delivery_email: Any = None
    delivery_city: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_region: Any = None
    delivery_postcode: Any = None
    delivery_country: Optional[str] = None
    delivery_phone: Optional[int] = None
    delivery_description: Any = None
    collection_name: Optional[str] = None
    collection_email: Any = None
    collection_city: Optional[str] = None
    collection_address: Any = None
    collection_region: Any = None
    collection_postcode: Any = None
    collection_country: Optional[str] = None
    collection_phone: Optional[int] = None
    collection_description: Any = None
    submission_date: Optional[str] = None
    pickup_date: Optional[str] = None
    received_at: Any = None
    delivery_date: Optional[str] = None
    weight: Optional[str] = None
    pieces: Optional[int] = None
    items_count: Optional[int] = None
    status: Optional[str] = None
    status_label: Optional[str] = None
    reason_en: Any = None
    reason_ar: Any = None
    created_at: Optional[str] = None
    id_customer: Optional[int] = None
    is_reverse_pickup: Optional[int] = None
    tracking_info: List[TrackingInfoType] = JList[TrackingInfoType]


@s(auto_attribs=True)
class DataType:
    shipments: List[ShipmentType] = JList[ShipmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    success: Optional[bool] = None
    data: Optional[DataType] = JStruct[DataType]

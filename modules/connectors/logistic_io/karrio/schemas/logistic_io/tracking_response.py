from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CustomerDetailsType:
    name: Optional[str] = None
    phone: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


@s(auto_attribs=True)
class CurrentStageType:
    stage: Optional[str] = None
    date: Optional[str] = None
    alpha_status_code: Optional[int] = None


@s(auto_attribs=True)
class OrderDetailsType:
    brand_reference_number: Optional[str] = None
    created_date: Optional[str] = None
    delivery_date: Any = None
    current_stage: Optional[CurrentStageType] = JStruct[CurrentStageType]


@s(auto_attribs=True)
class UpdateType:
    status: Optional[str] = None
    alpha_status_code: Optional[int] = None
    date: Optional[str] = None
    created_date: Optional[str] = None
    scanned_location: Any = None
    status_remark: Any = None
    additional_remark: Any = None


@s(auto_attribs=True)
class TrackingHistoryType:
    updates: List[UpdateType] = JList[UpdateType]


@s(auto_attribs=True)
class DatumType:
    referance_awb: Optional[str] = None
    cp_awb: Optional[str] = None
    is_mps: Optional[bool] = None
    box_count: Any = None
    allocated_courier_partner: Optional[str] = None
    customer_details: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    order_details: Optional[OrderDetailsType] = JStruct[OrderDetailsType]
    tracking_history: Optional[TrackingHistoryType] = JStruct[TrackingHistoryType]


@s(auto_attribs=True)
class TrackingResponseType:
    status: Optional[bool] = None
    data: List[DatumType] = JList[DatumType]

from attr import s
from typing import Any, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class ShippingType:
    reference: Any = None
    tracking_number: Optional[str] = None
    customer_tracking: Any = None
    customer_name: Optional[str] = None
    requested_by: Optional[str] = None
    price_set_amount: Any = None
    price_set_amount_incl_tax: Any = None
    tax_amount: Any = None
    tax_rate: Any = None
    cod_amount: Optional[int] = None
    declared_value: Optional[int] = None
    declared_value_currency: Optional[str] = None
    currency: Optional[str] = None
    delivery_name: Optional[str] = None
    delivery_email: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_neighbourhood: Optional[str] = None
    delivery_postcode: Optional[int] = None
    delivery_country: Optional[str] = None
    delivery_phone: Optional[int] = None
    delivery_description: Any = None
    collection_name: Optional[str] = None
    collection_email: Optional[str] = None
    collection_city: Optional[str] = None
    collection_address: Optional[str] = None
    collection_region: Any = None
    collection_postcode: Optional[int] = None
    collection_country: Optional[str] = None
    collection_phone: Optional[int] = None
    collection_description: Any = None
    submission_date: Optional[str] = None
    pickup_date: Any = None
    received_at: Any = None
    delivery_date: Any = None
    weight: Optional[int] = None
    pieces: Optional[int] = None
    items_count: Optional[int] = None
    status: Optional[str] = None
    status_label: Optional[str] = None
    created_at: Optional[str] = None
    is_reverse_pickup: Optional[int] = None
    label: Optional[str] = None
    pdf_label: Optional[str] = None


@s(auto_attribs=True)
class DataType:
    shipping: Optional[ShippingType] = JStruct[ShippingType]


@s(auto_attribs=True)
class ShippingResponseType:
    success: Optional[bool] = None
    data: Optional[DataType] = JStruct[DataType]

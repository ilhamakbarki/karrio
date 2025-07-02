from attr import s
from typing import Optional


@s(auto_attribs=True)
class ShippingRequestType:
    requested_by: Optional[str] = None
    declared_value: Optional[int] = None
    declared_value_currency: Optional[str] = None
    reference: Optional[str] = None
    is_cod: Optional[int] = None
    cod_amount: Optional[int] = None
    currency: Optional[str] = None
    delivery_name: Optional[str] = None
    delivery_email: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_neighbourhood: Optional[str] = None
    delivery_postcode: Optional[int] = None
    delivery_country: Optional[str] = None
    delivery_phone: Optional[int] = None
    delivery_description: Optional[str] = None
    collection_name: Optional[str] = None
    collection_email: Optional[str] = None
    collection_city: Optional[str] = None
    collection_address: Optional[str] = None
    collection_neighbourhood: Optional[str] = None
    collection_postcode: Optional[int] = None
    collection_country: Optional[str] = None
    collection_phone: Optional[int] = None
    collection_description: Optional[str] = None
    weight: Optional[int] = None
    pieces: Optional[int] = None
    items_count: Optional[int] = None

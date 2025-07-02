from attr import s
from typing import Optional, Any, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AdditionalType:
    deliverytype: Optional[str] = None
    additionalasync: Optional[bool] = None
    label: Optional[bool] = None
    orderdate: Optional[str] = None
    vendorcode: Optional[str] = None
    dutyfeepaidby: Optional[str] = None
    rvpreason: Any = None


@s(auto_attribs=True)
class InfoType:
    email: Optional[str] = None
    name: Optional[str] = None
    landmark: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    countrycode: Optional[str] = None
    postalcode: Optional[str] = None
    phone: Optional[str] = None
    phonecode: Optional[str] = None
    time: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    sku: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDetailsType:
    weight: Optional[int] = None
    breadth: Optional[int] = None
    height: Optional[int] = None
    length: Optional[int] = None
    invoicevalue: Optional[int] = None
    codvalue: Optional[int] = None
    ordertype: Optional[str] = None
    invoicenumber: Optional[str] = None
    invoicedate: Optional[str] = None
    referencenumber: Optional[str] = None
    currencycode: Optional[str] = None
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class ShippingRequestType:
    additional: Optional[AdditionalType] = JStruct[AdditionalType]
    pickupinfo: Optional[InfoType] = JStruct[InfoType]
    dropinfo: Optional[InfoType] = JStruct[InfoType]
    returninfo: Optional[InfoType] = JStruct[InfoType]
    taxinfo: Any = None
    shipmentdetails: Optional[ShipmentDetailsType] = JStruct[ShipmentDetailsType]

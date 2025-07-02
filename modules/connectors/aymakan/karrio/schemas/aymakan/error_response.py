from attr import s
from typing import List, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class ErrorsType:
    price_set: List[str] = []
    declared_value: List[str] = []


@s(auto_attribs=True)
class ErrorResponseType:
    error: Optional[bool] = None
    message: Optional[str] = None
    errors: Optional[ErrorsType] = JStruct[ErrorsType]
    response: Optional[str] = None

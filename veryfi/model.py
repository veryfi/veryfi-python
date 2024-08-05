from typing import Optional
from pydantic import BaseModel


class SharedLineItem(BaseModel):
    sku: Optional[str] = None
    category: Optional[str] = None
    tax: Optional[float] = None
    price: Optional[float] = None
    unit_of_measure: Optional[str] = None
    quantity: Optional[float] = None
    upc: Optional[str] = None
    tax_rate: Optional[float] = None
    discount_rate: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    hsn: Optional[str] = None
    section: Optional[str] = None
    weight: Optional[str] = None


class AddLineItem(SharedLineItem):
    order: int
    description: str
    total: float


class UpdateLineItem(SharedLineItem):
    order: Optional[int] = None
    description: Optional[str] = None
    total: Optional[float] = None

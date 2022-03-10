from typing import Optional
from pydantic import BaseModel


class SharedLineItem(BaseModel):
    sku: Optional[str]
    category: Optional[str]
    tax: Optional[float]
    price: Optional[float]
    unit_of_measure: Optional[str]
    quantity: Optional[float]
    upc: Optional[str]
    tax_rate: Optional[float]
    discount_rate: Optional[float]
    start_date: Optional[str]
    end_date: Optional[str]
    hsn: Optional[str]
    section: Optional[str]
    weight: Optional[str]


class AddLineItem(SharedLineItem):
    order: int
    description: str
    total: float


class UpdateLineItem(SharedLineItem):
    order: Optional[int]
    description: Optional[str]
    total: Optional[float]

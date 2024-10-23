from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    id: int
    name: str
    calories: int
    expiration_date: datetime
    price: float


@dataclass
class CartItem:
    product: Product
    quantity: int

    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity

from typing import Dict, List
from .entities import CartItem, Product


class Cart:
    def __init__(self, id: int, user_id: int):
        self.id = id
        self.user_id = user_id
        self.items: Dict[int, CartItem] = {}

    def add_item(self, product: Product, quantity: int) -> None:
        if product.id in self.items:
            self.items[product.id].quantity += quantity
        else:
            self.items[product.id] = CartItem(product, quantity)

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]

    def update_quantity(self, product_id: int, quantity: int) -> None:
        if product_id in self.items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                self.items[product_id].quantity = quantity

    @property
    def total(self) -> float:
        if not self.items:
            return 0.0
        return sum(item.total_price for item in self.items.values())

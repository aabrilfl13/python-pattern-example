from abc import ABC, abstractmethod
from typing import Optional
from cart.domain.aggregates import Cart
from cart.domain.entities import Product
from typing import List


class CartRepository(ABC):
    @abstractmethod
    def get(self, cart_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def save(self, cart: Cart) -> None:
        pass


class ProductRepository(ABC):
    @abstractmethod
    def get(self, product_id: int) -> Optional[Product]:
        """Get a single product by ID"""
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        """Get all products"""
        pass

    @abstractmethod
    def list_available(self) -> List[Product]:
        """Get all non-expired products"""
        pass

    @abstractmethod
    def list_by_ids(self, product_ids: List[int]) -> List[Product]:
        """Get multiple products by their IDs"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[Product]:
        """Search products by name"""
        pass

    @abstractmethod
    def get_expired_products(self) -> List[Product]:
        """Get all expired products"""
        pass

from cart.interfaces.repositories import CartRepository, ProductRepository
from cart.domain.aggregates import Cart
from common.uow import UnitOfWork


class CartService:
    def __init__(
        self, cart_repository: CartRepository, product_repository: ProductRepository
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def add_to_cart(self, cart_id: int, product_id: int, quantity: int) -> None:
        with UnitOfWork(self.cart_repository) as uow:
            cart = self.cart_repository.get(cart_id)
            product = self.product_repository.get(product_id)

            if not cart or not product:
                raise ValueError("Cart or product not found")

            cart.add_item(product, quantity)
            self.cart_repository.save(cart)

    def update_quantity(self, cart_id: int, product_id: int, quantity: int) -> None:
        with UnitOfWork(self.cart_repository) as uow:
            cart = self.cart_repository.get(cart_id)
            if not cart:
                raise ValueError("Cart not found")

            cart.update_quantity(product_id, quantity)
            self.cart_repository.save(cart)

    def remove_from_cart(self, cart_id: int, product_id: int) -> None:
        with UnitOfWork(self.cart_repository) as uow:
            cart = self.cart_repository.get(cart_id)
            if not cart:
                raise ValueError("Cart not found")

            cart.remove_item(product_id)
            self.cart_repository.save(cart)
